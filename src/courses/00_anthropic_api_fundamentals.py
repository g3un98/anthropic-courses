import base64
import os

from dotenv import load_dotenv
from anthropic import Anthropic, AsyncAnthropic

BLUE = "\033[94m"
GREEN = "\033[92m"
RESET = "\033[0m"

def new_client() -> Anthropic:
    load_dotenv()
    my_api_key = os.getenv("ANTHROPIC_API_KEY")

    return Anthropic(api_key=my_api_key)

def new_async_client() -> AsyncAnthropic:
    load_dotenv()
    my_api_key = os.getenv("ANTHROPIC_API_KEY")

    return AsyncAnthropic(api_key=my_api_key)

def translate(word: str, language: str):
    client = new_client()

    our_first_message = client.messages.create(
        model = "claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"Please translate '{word}' into {language} in short"}
        ]
    )

    print(our_first_message.content[0].text)

def haiku():
    client = new_client()

    our_first_message = client.messages.create(
        model = "claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "Generate a beautiful haiku"},
            {"role": "assistant", "content": "calming mountain air"},
        ]
    )

    print(our_first_message.content[0].text)

def generate_questions(topic: str, num_questions: int):
    client = new_client()

    resp = client.messages.create(
        model = "claude-3-5-haiku-latest",
        max_tokens=1000,
        system=f"You are an expert on {topic}. Generate thought-provoking questions about {topic}.",
        messages=[
            {"role": "user", "content": f"Generate {num_questions} questions about {topic} as a numbered list."}
        ],
        stop_sequences=[f"{num_questions+1}."]
    )

    print(resp.content[0].text)

async def chat():
    print("Type 'quit' to exit the chat.")
    client = new_async_client()

    conversation = []

    while True:
        user_input = input(f"{BLUE}You: {RESET}")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        conversation.append({"role": "user", "content": user_input})

        print(f"{GREEN}Claude: {RESET}", end="", flush=True)

        assistant_response = ""
        async with client.messages.stream(
            model="claude-3-5-haiku-latest",
            max_tokens=1024,
            messages=conversation,
        ) as stream:
            async for message in stream.text_stream:
                print(f"{GREEN}{message}{RESET}", end="", flush=True)
                assistant_response += message

        print()
        conversation.append({"role": "assistant", "content": assistant_response})

async def image():
    client = new_async_client()

    with open("assets/d3083d3f40bb2b6f477901cc9a240738d3dd1371-2401x1000.webp", "rb") as f:
        data = f.read()
        data = base64.b64encode(data)
        data = data.decode("utf-8")

    async with client.messages.stream(
        model="claude-3-5-sonnet-latest",
        max_tokens=1024,
        messages=[{"role": "user", "content": [{
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/webp",
                "data": data
            }
            }]
        }],
    ) as stream:
        async for message in stream.text_stream:
            print(f"{message}", end="", flush=True)

async def main():
    await image()
    # await chat()
    # generate_questions("free will", 3)
    # translate("hello", "Spanish")
    # translate("chicken", "Italian")
    # haiku()

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
