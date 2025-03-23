import os
from openai import AsyncOpenAI
import chainlit as cl
from chainlit.input_widget import Select, TextInput

openai_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

deepseek_client = AsyncOpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

gemini_client = AsyncOpenAI(api_key=os.environ["GEMINI_API_KEY"], base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

openai_settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

deepseek_settings = {
    "model": "deepseek-reasoner",
    "temperature": 0.5,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

gemini_settings = {
    "model": "gemini-1.5-pro",
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 1,
}

models = {
        "Deepseek R1": {"client": deepseek_client, "settings": deepseek_settings},
        "gpt-3.5-turbo": {"client": openai_client, "settings": openai_settings},
        "gemini-1.5-pro": {"client": gemini_client, "settings": gemini_settings},
}


#defaults 
client = openai_client
model_settings = openai_settings
default_instruction = "You are a helpful assistant"

@cl.step(type="retrieval")
def get_docs(query: str) -> list[str]: 
    """
        Retrieve relevant text chunks from the vdb
    """
    return [""]

@cl.on_chat_start
async def start():
    await cl.ChatSettings(
            [
            Select(
                id="model",
                label="LLM Model",
                values=["gpt-3.5-turbo", "Deepseek R1", "gemini-1.5-pro"],
                initial_index=0,
            ),
            TextInput(id="instruction",label="Instruction")]).send()


    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": default_instruction}],
    )
    await cl.Message(content="Connected to RejuvenAI!").send()


@cl.on_settings_update
async def setup_agent(settings):
  
    global client, model_settings

    try: 
        model_name = settings.get("model")
        instruction = settings.get("instruction")
    except KeyError as e: 
        print(e)

    if instruction: 
        message_history=cl.user_session.get("message_history")
        print(f"updating base instruction to: {instruction}")
        message_history[0]["content"] = instruction

        cl.user_session.set("message_history",message_history)

    client = models.get(model_name).get("client")
    model_settings = models.get(model_name).get("settings")

    print("new settings received", settings)


@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **model_settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
