import copy
import inspect
from typing import List, Dict, NamedTuple, Union, TYPE_CHECKING
from enum import Enum
from importlib.metadata import entry_points
import re
import warnings

import typedload
from . import util as plugin_util
import json

class PyriBlocklyCategory(NamedTuple):
    name: str
    blockly_json: dict

class PyriBlocklyBlockArgumentInterpretation:
    DEFAULT = "default"
    CODE = "code"
    INT = "int"
    FLOAT = "float"
    QUOTE = "quote"
    BOOL = "bool"

class PyriBlocklyBlockArgument(NamedTuple):
    blockly_arg_name: str
    sandbox_function_arg_name: str
    arg_interpretation: str = None

_blockly_arguments_default_interpretation = {
    "field_input": PyriBlocklyBlockArgumentInterpretation.QUOTE,
    "field_dropdown": PyriBlocklyBlockArgumentInterpretation.QUOTE,
    "field_checkbox": PyriBlocklyBlockArgumentInterpretation.BOOL,
    "field_colour": PyriBlocklyBlockArgumentInterpretation.INT,
    "field_number": PyriBlocklyBlockArgumentInterpretation.FLOAT,
    "field_angle": PyriBlocklyBlockArgumentInterpretation.FLOAT,
    "field_variable": PyriBlocklyBlockArgumentInterpretation.CODE,
    "input_value": PyriBlocklyBlockArgumentInterpretation.CODE
}

class PyriBlocklyBlockFunctionSelector(NamedTuple):
    selector_field: str
    sandbox_function_names: Dict[str,str]

class PyriBlocklyBlock(NamedTuple):
    name: str
    category: str
    docstring: str
    blockly_json: dict
    python_generator: str
    sandbox_function_name: str = None
    sandbox_function_arguments: List[PyriBlocklyBlockArgument] = None
    sandbox_function_name_selector: PyriBlocklyBlockFunctionSelector = None

    
def add_blockly_block(blockly_blocks: Dict[str,"PyriBlocklyBlock"],
    name: str = None, category: str = None, docstring: str = "", blockly_json: Union[str,Dict] = None,
    python_generator : str = None, sandbox_function_name : str = None, 
    sandbox_function_arguments : List[PyriBlocklyBlockArgument] = None, 
    sandbox_function_name_selector: PyriBlocklyBlockFunctionSelector = None,
    sandbox_function = None):

    assert blockly_json, f"blockly_json must not be None for block {name}"

    if not isinstance(blockly_json,dict):
        blockly_json_dict = json.loads(blockly_json)
    else:
        blockly_json_dict = blockly_json

    if name is None:
        name = blockly_json_dict["type"]

    assert category is not None and len(category) > 0, f"category must not be empty for block {name}"

    if not any([python_generator, sandbox_function_name, sandbox_function_name_selector]):
        if sandbox_function:
            sandbox_function_name = sandbox_function[0].__name__
        else:
            sandbox_function_name = name

    assert sum([a is not None for a in [python_generator, sandbox_function_name, sandbox_function_name_selector]]) ==1, \
        "exactly one of python_generator, sandbox_function_name, or sandbox_function_name_selector must be specified" \
        f" in block {name}"

    if sandbox_function_name or sandbox_function_name_selector:
        if not sandbox_function_arguments and sandbox_function:
            sandbox_function_arguments = []
            py_args = inspect.signature(sandbox_function[0]).parameters
            py_arg_info = []
            for py_arg in py_args.values():
                py_arg_interp = None
                if py_arg.annotation == float:
                    py_arg_interp = PyriBlocklyBlockArgumentInterpretation.FLOAT
                elif py_arg.annotation == int:
                    py_arg_interp = PyriBlocklyBlockArgumentInterpretation.INT
                elif py_arg.annotation == str:
                    py_arg_interp = PyriBlocklyBlockArgumentInterpretation.QUOTE
                py_arg_info.append((py_arg.name,py_arg_interp))
            for i in range(0,len(sandbox_function)-1):
                sandbox_function_arguments.append(PyriBlocklyBlockArgument( 
                    blockly_arg_name= sandbox_function[i+1],
                    sandbox_function_arg_name = py_arg_info[i][0],
                    arg_interpretation=py_arg_info[i][1]
                ))
        else:
            sandbox_function_arguments = copy.deepcopy(sandbox_function_arguments)
        blockly_args = blockly_json_dict.get("args0",[])
        if not sandbox_function_arguments:
            if len(blockly_args) == 0:
                sandbox_function_arguments = []
            else:
                assert sandbox_function_arguments, "sandbox_function_arguments must not be None when "\
                    f"sandbox_function_name or sandbox_function_name_selector is used in block {name}"
    
        used_sandbox_args = set()
        used_blockly_args = set()
        selector_field_arg = None
        for blockly_arg in blockly_args:
            
            if blockly_arg["type"] == "field_label" or blockly_arg["type"] == "input_dummy":
                continue

            assert blockly_arg["type"] in _blockly_arguments_default_interpretation, "unsupported block argument "\
                f"type {blockly_arg['type']} used in block {name}. Use Python generator function instead of "\
                "sandbox_function_name or sandbox_function_name_selector"

            assert blockly_arg["name"] not in used_blockly_args, f"blockly duplicate arg name {blockly_arg['name']} "\
                f"in block {name}"
            used_blockly_args.add(blockly_arg["name"])

            sandbox_arg_ind = -1
            sandbox_arg_val = None
            for j in range(len(sandbox_function_arguments)):
                sandbox_arg_val = sandbox_function_arguments[j]
                if blockly_arg["name"] == sandbox_arg_val.blockly_arg_name:
                    sandbox_arg_ind = j
                    break
            
            if sandbox_arg_ind < 0 and sandbox_function_name_selector:
                if blockly_arg["name"] == sandbox_function_name_selector.selector_field:
                    selector_field_arg = blockly_arg
                    continue

            assert sandbox_arg_ind >= 0, f"blockly argument {blockly_arg['name']} sandbox function mapping not "\
                f"found for block {name}"
            
            assert sandbox_arg_val.sandbox_function_arg_name not in used_sandbox_args, f"sandbox_function duplicate arg name " \
                f"{sandbox_arg_val.sandbox_function_arg_name} in block {name}"
            used_sandbox_args.add(sandbox_arg_val.sandbox_function_arg_name)

            if not sandbox_arg_val.arg_interpretation:
                sandbox_arg_val = PyriBlocklyBlockArgument(sandbox_arg_val.blockly_arg_name, 
                    sandbox_arg_val.sandbox_function_arg_name,
                    _blockly_arguments_default_interpretation[blockly_arg["type"]])
                sandbox_function_arguments[sandbox_arg_ind] = sandbox_arg_val

        assert used_sandbox_args == set(x.sandbox_function_arg_name for x in sandbox_function_arguments), "argument mismatch in "\
            f"block {name}"

        if sandbox_function_name_selector:
            assert selector_field_arg, f"blockly selector_field named {sandbox_function_name_selector.selector_field} "\
                f"not found in block {name}"
            
            assert len(selector_field_arg["options"]) == len(sandbox_function_name_selector.sandbox_function_names), \
                f"sandbox_function selector mismatch in block {name}"
            
            blockly_selector_names = set(x[1] for x in selector_field_arg["options"])
            name_blockly_selector_names = set(x for x in sandbox_function_name_selector.sandbox_function_names.keys())

            assert len(selector_field_arg["options"]) == len(blockly_selector_names), \
                f"sandbox_function selector name repeats in block {name}"

            assert blockly_selector_names == name_blockly_selector_names, "sandbox_function selector mismatch " \
                f"in block {name}"

            assert "" not in blockly_selector_names

    if docstring is None or len(docstring)==0:
        tooltip = blockly_json_dict.get("tooltip",None)
        if tooltip is not None and len(tooltip) > 0:
            docstring = tooltip
            
    blockdef = PyriBlocklyBlock(
        name = name,
        category = category,
        docstring = docstring,
        blockly_json = blockly_json_dict,
        python_generator= python_generator,
        sandbox_function_name=sandbox_function_name,
        sandbox_function_arguments=sandbox_function_arguments,
        sandbox_function_name_selector=sandbox_function_name_selector
    )

    if blockly_blocks is not None:
        blockly_blocks[name] = blockdef
    return blockdef

def blockly_block_to_json(pyri_blockly_block):
    return typedload.dump(pyri_blockly_block)

def blockly_block_from_json(block_json):
    return typedload.load(block_json, PyriBlocklyBlock)

def add_blockly_category(blockly_categories: Dict[str,"PyriBlocklyCategory"], name: str = None, colour: int = None, blockly_json: dict = None):
    assert blockly_json or name, "Both name and blockly_json cannot be null"
    if not blockly_json:
        blockly_json = {"kind": "category", "name": name}
        if colour:
            blockly_json["colour"] = colour
    else:
        name = blockly_json["name"]

    catdef = PyriBlocklyCategory(name = name, blockly_json = blockly_json)
    if blockly_categories is not None:
        blockly_categories[name] = catdef
    return catdef

def blockly_category_to_json(pyri_blockly_category):
    return typedload.dump(pyri_blockly_category)

def blockly_block_from_json(category_json):
    return typedload.load(category_json, PyriBlocklyCategory)



class PyriBlocklyPluginFactory:
    def __init__(self):
        super().__init__()

    def get_plugin_name(self):
        return ""

    def get_category_names(self) -> List[str]:
        return []

    def get_categories(self) -> List[PyriBlocklyCategory]:
        return []

    def get_block_names(self) -> List[str]:
        return []

    def get_block(self,name) -> PyriBlocklyBlock:
        return None

    def get_all_blocks(self) -> Dict[str,PyriBlocklyBlock]:
        return []

def get_all_robdef_blockly_factories() -> List[PyriBlocklyPluginFactory]:
    return plugin_util.get_plugin_factories("pyri.plugins.blockly")

def get_all_blockly_blocks() -> Dict[str,PyriBlocklyBlock]:
    factories = get_all_robdef_blockly_factories()
    ret = dict()
    for f in factories:
        ret.update(f.get_all_blocks())
    return ret

def get_all_blockly_categories() -> Dict[str,PyriBlocklyCategory]:
    factories = get_all_robdef_blockly_factories()
    ret = dict()
    for f in factories:
        ret.update(f.get_categories())
    return ret