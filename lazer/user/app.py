"""
a user's dummy app
i.e: how they *may* interact with Lazer
"""
import openai
import os
import json
from icecream import ic

from lazer import Lazer
from dotenv import load_dotenv

lazer = Lazer()

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


@lazer.use
def qux(num1: int, name: str) -> str:
    """
    Takes a number from the user as well as a name and computes the qux of them both.
    """
    if not isinstance(num1, int):
        raise TypeError("num1 parameter must be an integer")
    if not isinstance(name, str):
        raise TypeError("name parameter must be a string")
    return str(num1 + len(name))


@lazer.use
def getSmellinessOfNumber(num: int) -> str:
    """
    Takes a number from the user and computes the smelliness of it.
    """
    if num == 3:
        return "ROTTEN"

    if num > 7:
        return "SWEET"

    return "BREEZY"


messages = []


def get_gpt_response(
    message: str, role: str = "user", function_name: str | None = None
) -> dict:
    global messages
    messages.append({"role": role, "content": message})

    if function_name:  # HACK: only do this if func was invoked
        messages[-1].update({"name": function_name})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=lazer.get_functions(),
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]  # type: ignore
    messages.append(response_message)

    return response_message


def main():
    while 1:
        user_inp = input("🤔> ")

        if user_inp.lower() in ("exit", "quit", "q", "exit()", "quit()"):
            break

        message = get_gpt_response(user_inp)

        if not message.get("function_call"):
            print(f"🤖> {message['content']}", flush=True)
            continue

        function_name = message["function_call"]["name"]
        function_args = json.loads(message["function_call"]["arguments"])

        function_response = "No response from function call"

        function_response = lazer.dispatch(function_name, function_args)

        function_based_response = get_gpt_response(
            function_response, "function", function_name
        )
        print(f"🤖🔧> {function_based_response['content']}", flush=True)

    print("🤖> Thanks for chatting with me!\n", flush=True)


if __name__ == "__main__":
    main()
