import openai
import os
import json
from dotenv import load_dotenv
from icecream import ic
from .address import Address

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

from enum import Enum


class Scent(Enum):
    MAPLE = 0
    SWEET = 1
    CITRUS = 2
    FLORAL = 3
    EARTHY = 4
    SPICY = 5


def smelly_number(num: int, scent: Scent) -> str:
    """Convert a number (num) to a smelly number based on a given scent"""
    ic(num, scent)
    if scent == Scent.MAPLE:
        return str(num * 2)
    elif scent == Scent.SWEET:
        return str(num + 5)
    elif scent == Scent.CITRUS:
        return str(num - 7)
    elif scent == Scent.FLORAL:
        return str(num - 2)
    elif scent == Scent.EARTHY:
        return str(num + 3)
    elif scent == Scent.SPICY:
        return str(num - 5)

    return str(-1)


def main():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "user",
                "content": "What is the smelly number of 9 if I smell something spicy?",
            }
        ],
        functions=[
            {
                "name": "smelly_number",
                "description": "Convert a number (num) to a smelly number based on a given scent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "num": {
                            "type": "integer",
                            "description": "The number to make smelly",
                        },
                        "scent": {
                            "type": "string",
                            "enum": [
                                "MAPLE",
                                "SWEET",
                                "CITRUS",
                                "FLORAL",
                                "EARTHY",
                                "SPICY",
                            ],
                        },
                    },
                    "required": ["location"],
                },
            }
        ],
        function_call="auto",
    )

    message = response["choices"][0]["message"]  # type: ignore

    # Step 2, check if the model wants to call a function
    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        function_args = json.loads(message["function_call"]["arguments"])

        # Step 3, call the function
        # Note: the JSON response from the model may not be valid JSON
        function_response = smelly_number(
            num=function_args.get("num"), scent=Scent[function_args.get("scent")]
        )

        # Step 4, send model the info on the function call and function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {
                    "role": "user",
                    "content": "What is the smelly number of 9 if I smell something spicy?",
                },
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return second_response


def foo(num1: int, num2: str) -> float:
    return 3.14 + num1 + int(num2)


def bar(addr: Address) -> str:
    return f"That is a cool address located at {addr.zipcode}"


if __name__ == "__main__":
    result = main()
    print(result)
