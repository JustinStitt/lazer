import os
import pprint
import ast
import inspect
from icecream import ic
from typing import Callable

from pytojsonschema.functions import process_function_def
from pytojsonschema.common import init_schema_map, init_typing_namespace

# pprint.pprint(process_package(os.path.join("lazer")))


# @lazer
# def qaz(num: int) -> str:
#     """return num but as a string and increased by 1"""
#     return str(num + 1)


# if __name__ == "__main__":
#     fname_to_schema = functions_to_schemas(_functions)
#     ic(fname_to_schema)
