"""
a user's dummy app
i.e: how they *may* interact with Lazer
"""
import openai
import os
import json
from icecream import ic
from lazer import lazer, get_functions
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


@lazer
def qux(num1: int, name: str) -> str:
    """
    This function takes in an integer and a string as parameters and returns a string. The integer parameter represents a number, while the string parameter represents a name. The function returns a string that is the sum of the integer parameter and the length of the string parameter.

    :param num1: An integer representing a number.
    :type num1: int
    :param name: A string representing a name.
    :type name: str
    :return: A string that is the sum of the integer parameter and the length of the string parameter.
    :rtype: str
    :raises TypeError: If the num1 parameter is not an integer or the name parameter is not a string.
    """
    if not isinstance(num1, int):
        raise TypeError("num1 parameter must be an integer")
    if not isinstance(name, str):
        raise TypeError("name parameter must be a string")
    return str(num1 + len(name))


messages = []


def get_gpt_response(
    message: str, role: str = "user", function_name: str | None = None
) -> dict:
    global messages
    messages.append({"role": role, "content": message})

    if function_name:
        messages[-1].update({"name": function_name})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=get_functions(),
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
        if function_name == "qux":
            function_response = qux(**function_args)

        function_based_response = get_gpt_response(
            function_response, "function", function_name
        )
        print(f"🤖🔧> {function_based_response['content']}", flush=True)

    print("🤖> Thanks for chatting with me!\n", flush=True)


if __name__ == "__main__":
    main()
