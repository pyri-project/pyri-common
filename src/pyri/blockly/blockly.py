from pyri.plugins.blockly import PyriBlocklyPluginFactory, PyriBlocklyBlock, PyriBlocklyCategory
from typing import List, Dict, NamedTuple, TYPE_CHECKING

def _get_blocks() -> Dict[str,PyriBlocklyBlock]:
    blocks = {}

    blocks["time_wait"] = PyriBlocklyBlock(
        name = "time_wait",
        category = "Time",
        doc = "Wait a specified number of seconds",
        json = """{
                "type": "time_wait",
                "message0": "Wait %1 seconds",
                "args0": [
                    {
                    "type": "field_number",
                    "name": "WAIT_TIME",
                    "value": 1,
                    "min": 0
                    }
                ],
                "previousStatement": null,
                "nextStatement": null,
                "colour": 65,
                "tooltip": "",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['time_wait'] = function(block) {
                            var number_wait_time = block.getFieldValue('WAIT_TIME');
                            
                            var code = 'time_wait(' + number_wait_time+ ')\\n';
                            return code;
                            };
                            """
        
    )
    blocks["linalg_vector"] = PyriBlocklyBlock(
        name = "linalg_vector",
        category = "Linalg",
        doc = "Create a new vector",
        json = """{
                "type": "linalg_vector",
                "message0": "[ %1 ]",
                "args0": [
                    {
                    "type": "field_input",
                    "name": "VECTOR",
                    "text": ""
                    }
                ],
                "output": null,
                "colour": 230,
                "tooltip": "Create a new vector",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['linalg_vector'] = function(block) {
                            var text_vector = block.getFieldValue('VECTOR');                            
                            var code = 'linalg_vector(\\\"' + text_vector + '\\\")';                          
                            return [code, Blockly.Python.ORDER_NONE];
                            };
                            """
        
    )



    return blocks

def _get_categories() -> Dict[str,PyriBlocklyCategory]:
    categories = {}
    categories["Time"] = PyriBlocklyCategory(
        name = "Time",
        json = '{"kind": "category", "name": "Time", "colour": 65 }'
    )

    categories["Linalg"] = PyriBlocklyCategory(
        name ="Linalg",
        json = '{"kind": "category", "name": "Linalg", "colour": 230 }'
    )

    return categories


class PyriCommonBlocklyPluginFactory(PyriBlocklyPluginFactory):
    def get_plugin_name(self):
        return "pyri-common"

    def get_category_names(self) -> List[str]:
        return ["Time", "Linalg"]

    def get_categories(self) -> List[PyriBlocklyCategory]:
        return _get_categories()

    def get_block_names(self) -> List[str]:
        return list(_get_blocks().keys())

    def get_block(self,name) -> PyriBlocklyBlock:
        return _get_blocks()[name]

    def get_all_blocks(self) -> Dict[str,PyriBlocklyBlock]:
        return _get_blocks()

def get_blockly_factory():
    return PyriCommonBlocklyPluginFactory()