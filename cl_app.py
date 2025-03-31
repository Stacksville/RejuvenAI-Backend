import os
import chainlit as cl
from chainlit.input_widget import Select, TextInput
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableConfig, RunnablePassthrough
from langchain.callbacks.base import BaseCallbackHandler
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
    "model": "deepseek-reasoner",
    #"temperature": 1.0,
    "max_tokens": 4500,
    "top_p": 1,
    #"frequency_penalty": 0,
    #"presence_penalty": 0,
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



#initalize RAG
vectordb = get_vectordb()

#initialize model clients
openai_model = ChatOpenAI(**openai_settings)
deepseek_model = ChatOpenAI(**deepseek_settings)
gemini_model = ChatOpenAI(**gemini_settings)

model_selector = {
        "Deepseek R1": deepseek_model,
        "gpt-4": openai_model,
        "gemini-1.5-pro": gemini_model,
}

#default model
model = openai_model

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

retriever = vectordb.as_retriever(search_kwargs = {"k":10})

@cl.on_chat_start
async def start():

    await cl.ChatSettings(
            [
            Select(
                id="model",
                label="LLM Model",
                values=["gpt-4", "Deepseek R1", "gemini-1.5-pro"],
                initial_index=0,
            ),
            TextInput(id="instruction",label="Instruction"),
        ],
    ).send()

    runnable_sequence = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt 
        | model
        | StrOutputParser()

    )

    cl.user_session.set("runnable", runnable_sequence)

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
    
    print("setting new model")

    rs = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt 
        | model
        | StrOutputParser()

    )

    cl.user_session.set("runnable", rs)
    print("set the new runnable seq successfully")
    


@cl.on_message
async def on_message(message: cl.Message):

    runnable = cl.user_session.get("runnable")

    msg = cl.Message(content="")

    class PostMessageHandler(BaseCallbackHandler):
        """
        Callback handler for handling the retriever and LLM processes.
        Used to post the sources of the retrieved documents as a Chainlit element.
        """

        def __init__(self, msg: cl.Message):
            BaseCallbackHandler.__init__(self)
            self.msg = msg
            self.sources = set()  # To store unique pairs

        def on_retriever_end(self, documents, *, run_id, parent_run_id, **kwargs):
            for d in documents:
                source_page_pair = (d.metadata["source"], d.metadata["page"])
                self.sources.add(source_page_pair)  # Add unique pairs to the set

        def on_llm_end(self, response, *, run_id, parent_run_id, **kwargs):
            if len(self.sources):
                sources_text = "\n".join(
                    [f"{source}#page={page}" for source, page in self.sources]
                )
                self.msg.elements.append(
                    cl.Text(name="Sources", content=sources_text, display="inline")
                )

    async for chunk in runnable.astream(
        message.content,
        config=RunnableConfig(
            callbacks=[cl.LangchainCallbackHandler(), PostMessageHandler(msg)]
        ),
    ):
        await msg.stream_token(chunk)

    await msg.send()
