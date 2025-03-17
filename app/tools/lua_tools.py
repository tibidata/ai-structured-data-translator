"""
Module: lua_utils

This module provides utility functions for extracting key-value pairs from a Lua table
and generating a Lua script from a given dictionary.

Functions:
    extract_lua(var_name: str, lua_code: str) -> dict:
        Extracts key-value pairs from a Lua table defined in the given Lua script.

    generate_lua(var_name: str, kv_dict: dict) -> str:
        Generates a Lua script defining a table from a given dictionary.
"""

import logging

from lupa import LuaRuntime, LuaError


def extract_lua(var_name: str, lua_code: str) -> dict:
    """
    Extracts key-value pairs from a Lua table defined in the given Lua script.

    Args:
        var_name (str): The name of the Lua table to extract.
        lua_code (str): The Lua script containing the table definition.

    Returns:
        dict: A dictionary representing the key-value pairs extracted from the Lua table.
    """

    def lua_to_dict(lua_table):
        """
        Recursively converts a Lua table to a Python dictionary.
        """
        py_dict = {}
        for key, value in lua_table.items():
            if hasattr(value, "items"):  # Check if value is a nested Lua table
                py_dict[key] = lua_to_dict(value)  # Recursive conversion
            else:
                py_dict[key] = value.replace('"', "").replace(
                    "'", ""
                )  # Store simple values directly
        return py_dict

    lua = LuaRuntime(unpack_returned_tuples=True)

    try:
        lua.execute(lua_code)

    except LuaError as e:
        if "nil" in e.__str__():
            logging.info("Fixing lua code")
            lua_code = "{var_name} = {{}} \n".format(var_name=var_name) + lua_code
        else:
            logging.exception(e)
            raise e
    except Exception as e:
        logging.exception(e)
        raise e

    # Initialize Lua runtime
    lua.execute(lua_code)  # Execute the Lua script

    global_var = lua.globals()[var_name]  # Access the Lua table

    return lua_to_dict(global_var)


def generate_lua(var_name: str, kv_dict: dict, key_type: str) -> str:
    """
    Generates a Lua script defining a table from a given dictionary, handling nested dictionaries.

    Args:
        var_name (str): The name of the Lua table to create.
        kv_dict (dict): A dictionary containing key-value pairs to be converted into Lua format.

    Returns:
        str: A formatted Lua script defining the table with the given key-value pairs.
    """

    def get_key(k):
        nonlocal key_type

        if key_type == "bracket":
            return f'["{k}"]'
        return k

    def dict_to_lua(d, indent=1):
        lua_str = "{\n"
        for k, v in d.items():
            if isinstance(v, dict):

                lua_str += (
                    "{indent}{key} = ".format(indent="    " * indent, key=k)
                    + dict_to_lua(v, indent + 1)
                    + ",\n"
                )
            else:
                lua_str += '{indent}{key} = "{value}",\n'.format(
                    indent="    " * indent,
                    key=get_key(k),
                    value=str(v).replace("\n", "\\n"),
                )
        lua_str += "    " * (indent - 1) + "}"
        return lua_str

    return '{var_name}={{}}\n\n{var_name}["{key}"] = '.format(
        var_name=var_name, key=list(kv_dict.keys())[0]
    ) + dict_to_lua(list(kv_dict.values())[0])
