import os
from typing import Dict
from typing import Optional

import chainlit as cl
from chainlit.input_widget import Select, TextInput
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from utils import get_current_user
from vectordb import get_vectordb

openai_settings = {
    "model": "gpt-4o",
    "temperature": 1.0,
    "max_tokens": 4000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "api_key": os.environ["OPENAI_API_KEY"],
    "streaming": True,

}

deepseek_settings = {
    "model": "deepseek-chat",
    # "temperature": 1.0,
    "max_tokens": 4500,
    "top_p": 1,
    # "frequency_penalty": 0,
    # "presence_penalty": 0,
    "base_url": "https://api.deepseek.com",
    "api_key": os.environ["DEEPSEEK_API_KEY"],
    "streaming": True,
}

gemini_settings = {
    "model": "gemini-1.5-pro",
    "temperature": 0.7,
    "max_tokens": 10000,
    "top_p": 1,
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
    "api_key": os.environ["GEMINI_API_KEY"],
    "streaming": True,

}

# initalize RAG
vectordb = get_vectordb()

# initialize model clients
openai_model = ChatOpenAI(**openai_settings)
deepseek_model = ChatOpenAI(**deepseek_settings)
gemini_model = ChatOpenAI(**gemini_settings)

model_selector = {
    "Deepseek v3": deepseek_model,
    "gpt-4": openai_model,
    "gemini-1.5-pro": gemini_model,
}

# default model
model = openai_model

# TODO: Load the abbreviations doc into the system prompt
template = """
you are a peer-like virtual assistant that has reference and database of knowledge to assist providers and staff in answering clinical questions. Respond in a concise, text-style manner that mirrors the user's tone and style, but lean towards technical and medical language.

Provide clinical guidance and support to help staff make educated decisions regarding patient cases and answer questions they or their patients may have.
Prioritize research and objective data found in uploaded knowledge documents over internet resources.
Use the abbreviations list provided in the Knowledge section to improve interpretation of the prompts and information in database.
Answer the question based on the following context:

{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


graph_builder = StateGraph(MessagesState)


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information to answer questions related to science"""
    retrieved_docs = vectordb.similarity_search(query, k=10)
    serialized = format_docs(retrieved_docs)
    sources = set()
    for d in retrieved_docs:
        source_page_pair = (d.metadata["source"], d.metadata["page"])
        sources.add(source_page_pair)

    return serialized, sources


def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or base response"""
    llm_with_tools = model.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


tools = ToolNode([retrieve])


def generate(state: MessagesState):
    """Generate answer."""
    # Get generated ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        f"{docs_content}"
    )
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
           or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = model.invoke(prompt)
    return {"messages": [response]}


graph_builder.add_node(query_or_respond)
graph_builder.add_node(tools)
graph_builder.add_node(generate)

graph_builder.set_entry_point("query_or_respond")
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: END, "tools": "tools"},
)

graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", END)

memory = MemorySaver()

graph = graph_builder.compile(checkpointer=memory)


@cl.header_auth_callback
def header_auth_callback(headers: Dict) -> Optional[cl.User]:
    # Add Authorisation to chainlit app
    auth_header = headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None  # No token, deny access
    try:
        payload = get_current_user(token=auth_header.split(" ")[1])
        username = payload.get("sub")
        return cl.User(identifier=username, metadata={"role": "admin", "provider": "header"})
        # return cl.User(identifier="admin", metadata={"role": "admin", "provider": "jwt"})
        # return cl.User(identifier=payload.get("sub"), metadata={"role": role, "provider": "jwt"})
    except Exception as e:
        print(e)
        return None


@cl.on_chat_start
async def start():
    await cl.ChatSettings(
        [
            Select(
                id="model",
                label="LLM Model",
                values=["gpt-4", "Deepseek v3", "gemini-1.5-pro"],
                initial_index=0,
            ),
            TextInput(id="instruction", label="Instruction"),
        ],
    ).send()

    await cl.Message(content="Connected to RejuvenAI!").send()


@cl.on_settings_update
async def setup_agent(settings):
    global model

    try:
        model_name = settings.get("model")
    except KeyError as e:
        print(e)

    print("new settings received", settings)
    model = model_selector.get(model_name)


@cl.on_message
async def on_message(msg: cl.Message):
    final_answer = cl.Message(content="")
    config = {"configurable": {"thread_id": cl.context.session.id}}
    sources = set()

    class PostMessageHandler(BaseCallbackHandler):
        """
        CallBackHandler to inspect the rewritten query
        """

        def __init__(self):
            BaseCallbackHandler.__init__(self, )
            BaseCallbackHandler.raise_error = False

        def on_tool_start(self, serialized: dict, input_str: str, *, run_id, parent_run_id=None, tags=None,
                          metadata=None, inputs=None, **kwargs, ):
            print(f"Executing retrieval with input: {input_str}")

    for step, metadata in graph.stream(
            {"messages": [{"role": "user", "content": msg.content}]},
            stream_mode="messages",
            config=RunnableConfig(callbacks=[PostMessageHandler()], **config),

    ):
        # step["messages"][-1].pretty_print()
        # get sources from the tool run
        if (
                step.content
                and metadata["langgraph_node"] == "tools"
        ):
            sources = step.artifact
            continue  # skip tool output (retrieval chunks)

        await final_answer.stream_token(step.content)

    if sources and len(sources):
        sources_text = "\n".join(
            [f"{source}#page={page}" for source, page in sources]
        )
        source_element = [cl.Text(name="Sources", content=sources_text, display="inline")]

        await cl.Message(
            content="",
            elements=source_element,
        ).send()

    await final_answer.send()
