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

from lupa import LuaRuntime


def extract_lua(var_name: str, lua_code: str) -> dict:
    """
    Extracts key-value pairs from a Lua table defined in the given Lua script.

    Args:
        var_name (str): The name of the Lua table to extract.
        lua_code (str): The Lua script containing the table definition.

    Returns:
        dict: A dictionary representing the key-value pairs extracted from the Lua table.
    """

    def lua_table_to_dict(lua_table):
        """
        Recursively converts a Lua table to a Python dictionary.
        """
        py_dict = {}
        for key, value in lua_table.items():
            if hasattr(value, "items"):  # Check if value is a nested Lua table
                py_dict[key] = lua_table_to_dict(value)  # Recursive conversion
            else:
                py_dict[key] = value.replace('"', "").replace("'", "")
                print(py_dict[key])  # Store simple values directly
        return py_dict

    lua = LuaRuntime(unpack_returned_tuples=True)  # Initialize Lua runtime
    lua.execute(lua_code)  # Execute the Lua script

    global_var = lua.globals()[var_name]  # Access the Lua table

    return lua_table_to_dict(global_var)


def generate_lua(var_name: str, kv_dict: dict) -> str:
    """
    Generates a Lua script defining a table from a given dictionary.

    Args:
        var_name (str): The name of the Lua table to create.
        kv_dict (dict): A dictionary containing key-value pairs to be converted into Lua format.

    Returns:
        str: A formatted Lua script defining the table with the given key-value pairs.
    """
    for k, v in kv_dict.items():
        header = '{var_name} = {{}}\n\n{var_name}["{key}"] = '.format(
            var_name=var_name, key=k
        )
        body = (
            "{"
            + "".join(
                '\n\t{i} = "{j}",'.format(i=i, j=j.replace("\n", "\\n"))
                for i, j in v.items()
            ).strip(",")
            + "}"
        )
    return header + body
