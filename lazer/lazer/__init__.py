import ast
import inspect
from icecream import ic
from typing import Callable

from pytojsonschema.functions import process_function_def
from pytojsonschema.common import init_schema_map, init_typing_namespace


_schema_map = init_schema_map()
_type_namespace = init_typing_namespace()


_functions = []
_previous_get_functions_result = None


def dispatch(function_name: str, function_args: dict):
    for func in _functions:  # FIX: slow linear search, use set
        name = func.__name__
        if function_name == name:
            return func(**function_args)

    return "can't find that function lol xd"


def get_functions() -> list[dict]:
    global _functions, _previous_get_functions_result
    if _previous_get_functions_result:
        return _previous_get_functions_result
    result = _functions_to_schemas(_functions)
    _previous_get_functions_result = result
    ic(_functions)
    return result


def lazer(func):
    global _functions
    _functions.append(func)

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def _fill_in_schema(name: str, doc: str, base_schema: dict) -> dict:
    """Take the schema generated from pytojsonschema and fill it out to fit OpenAI's format"""
    final_schema = {}
    final_schema["name"] = name
    final_schema["description"] = doc
    final_schema["parameters"] = base_schema
    # TODO: add in per-variable descriptions
    return final_schema


def _functions_to_schemas(functions: list[Callable]) -> list[dict]:
    global _schema_map, _type_namespace
    schemas: list[dict] = []

    for function in functions:
        name = function.__name__
        doc = function.__doc__ or "No Description"
        src = ast.parse(inspect.getsource(function)).body
        node = src[0]

        base_schema = process_function_def(node, _type_namespace, _schema_map)  # type: ignore
        del base_schema[
            "$schema"
        ]  # unsued for OpenAI's purposes, probably doesn't hurt to leave it though

        del base_schema["additionalProperties"]

        openai_compliant_schema = _fill_in_schema(name, doc, base_schema)
        schemas.append(openai_compliant_schema)
        ic(openai_compliant_schema)

    return schemas
