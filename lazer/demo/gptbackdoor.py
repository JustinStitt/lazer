import asyncio
import openai
import os
from lazer import Lazer, LazerConversation

openai.api_key = os.getenv("OPENAI_API_KEY")


backdoor = Lazer()


@backdoor.use
def ls() -> str:
    """List files in current directory"""
    files = os.listdir(".")
    return "\n".join(files)


@backdoor.use
def cat(filename: str) -> str:
    """Read a file"""
    with open(filename) as f:
        return f.read()


async def main():
    convo = LazerConversation(backdoor, {"model": "gpt-3.5-turbo-0613"})

    while True:
        content = input("> ")
        message = await convo.talk(content)
        print("< " + message["content"], flush=True)
        print()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
