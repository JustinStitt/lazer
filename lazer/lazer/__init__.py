import ast
import inspect
from icecream import ic
from typing import Callable

from pytojsonschema.functions import process_function_def
from pytojsonschema.common import init_schema_map, init_typing_namespace


class Lazer:
    def __init__(self):
        self._schema_map = init_schema_map()
        self._type_namespace = init_typing_namespace()
        self._functions = []
        self._name_to_func = {}
        self._previous_get_functions_result = None

    def dispatch(self, function_name: str, function_args: dict):
        f = self._name_to_func.get(function_name, lambda: "Couldn't find that function")
        return f(**function_args)

    def get_functions(self) -> list[dict]:
        if self._previous_get_functions_result:
            return self._previous_get_functions_result
        result = self._functions_to_schemas(self._functions)
        self._previous_get_functions_result = result
        return result

    def use(self, func):
        self._functions.append(func)
        self._name_to_func[func.__name__] = func

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    def _fill_in_schema(self, name: str, doc: str, base_schema: dict) -> dict:
        """Take the schema generated from pytojsonschema and fill it out to fit OpenAI's format"""
        final_schema = {}
        final_schema["name"] = name
        final_schema["description"] = doc
        final_schema["parameters"] = base_schema
        # TODO: add in per-variable descriptions
        return final_schema

    def _functions_to_schemas(self, functions: list[Callable]) -> list[dict]:
        schemas: list[dict] = []

        for function in functions:
            name = function.__name__
            doc = function.__doc__ or "No Description"
            src = ast.parse(inspect.getsource(function)).body
            node = src[0]

            base_schema = process_function_def(node, self._type_namespace, self._schema_map)  # type: ignore
            del base_schema[
                "$schema"
            ]  # unsued for OpenAI's purposes, probably doesn't hurt to leave it though

            del base_schema["additionalProperties"]

            openai_compliant_schema = self._fill_in_schema(name, doc, base_schema)
            schemas.append(openai_compliant_schema)

        return schemas
