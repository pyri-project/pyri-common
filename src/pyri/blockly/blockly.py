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
                "message0": "new vector [ %1 ]",
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
    blocks["linalg_matrix"] = PyriBlocklyBlock(
        name = "linalg_matrix",
        category = "Linalg",
        doc = "Create a new matrix",
        json = """{
                "type": "linalg_matrix",
                "message0": "new matrix %1 ",
                "args0": [
                    {
                    "type": "field_input",
                    "name": "MATRIX",
                    "text": ""
                    }
                ],
                "output": null,
                "colour": 230,
                "tooltip": "Create a new matrix",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['linalg_matrix'] = function(block) {
                            var text_matrix = block.getFieldValue('MATRIX');                            
                            var code = 'linalg_matrix(\\\"' + text_matrix + '\\\")';                          
                            return [code, Blockly.Python.ORDER_NONE];
                            };
                            """
        
    )
    blocks["linalg_fill_vector"] = PyriBlocklyBlock(
        name = "linalg_fill_vector",
        category = "Linalg",
        doc = "Create a new zero vector with m elements filled with value",
        json = """{
                "type": "linalg_fill_vector",
                "message0": "fill vector length %1 with value %2 %3",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "M",
                    "check": "Number"
                    },
                    {
                    "type": "input_value",
                    "name": "VALUE",
                    "check": "Number"
                    },
                    {
                    "type": "input_dummy",
                    "align": "CENTRE"
                    }
                ],
                "output": null,
                "colour": 230,
                "tooltip": "Create vector with length m and fill with value",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['linalg_fill_vector'] = function(block) {
                            var number_m = block.getFieldValue('M');
                            var value_value = Blockly.Python.valueToCode(block, 'VALUE', Blockly.Python.ORDER_ATOMIC);
                            // TODO: Assemble Python into code variable.
                            var code = 'linalg_fill_vector(' + number_m + ',' + value_value + ')';
                            // TODO: Change ORDER_NONE to the correct strength.
                            return [code, Blockly.Python.ORDER_NONE];
                            };
                            """
        
    )
    blocks["linalg_fill_matrix"] = PyriBlocklyBlock(
        name = "linalg_fill_matrix",
        category = "Linalg",
        doc = "Create a new matrix with m x n elements and fill with value",
        json = """{
                "type": "linalg_fill_matrix",
                "message0": "fill matrix size %1 , %2 with value %3 %4",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "M",
                    "check": "Number"
                    },
                    {
                    "type": "input_value",
                    "name": "N",
                    "check": "Number"
                    },
                    {
                    "type": "input_value",
                    "name": "VALUE",
                    "check": "Number"
                    },
                    {
                    "type": "input_dummy",
                    "align": "CENTRE"
                    }
                ],
                "output": null,
                "colour": 230,
                "tooltip": "Create matrix with size m,n and fill with value",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['linalg_fill_matrix'] = function(block) {
                        var value_m = Blockly.Python.valueToCode(block, 'M', Blockly.Python.ORDER_ATOMIC);
                        var value_n = Blockly.Python.valueToCode(block, 'N', Blockly.Python.ORDER_ATOMIC);
                        var value_value = Blockly.Python.valueToCode(block, 'VALUE', Blockly.Python.ORDER_ATOMIC);
                        // TODO: Assemble Python into code variable.
                        var code = 'linalg_fill_matrix(' + number_m + ',' + number_n + ',' + value_value + ')';
                        // TODO: Change ORDER_NONE to the correct strength.
                        return [code, Blockly.Python.ORDER_NONE];
                        };
                            """
    )
    blocks["linalg_unary_op"] = PyriBlocklyBlock(
        name = "linalg_unary_op",
        category = "Linalg",
        doc = "Linear algebra unary op",
        json = """{
                "type": "linalg_unary_op",
                "message0": "%1 %2",
                "args0": [
                    {
                    "type": "field_dropdown",
                    "name": "OP",
                    "options": [
                        [
                        "transpose",
                        "TRANSPOSE"
                        ],
                        [
                        "inverse",
                        "INVERSE"
                        ],
                        [
                        "negative",
                        "NEGATIVE"
                        ],
                        [
                        "det",
                        "DETERMINATE"
                        ],
                        [
                        "conjugate",
                        "CONJUGATE"
                        ],
                        [
                        "adjoint",
                        "ADJOINT"
                        ],
                        [
                        "cofactor",
                        "COFACTOR"
                        ],
                        [
                        "eigen values",
                        "EIGENVALUES"
                        ],
                        [
                        "eigen vectors",
                        "EIGENVECTORS"
                        ],
                        [
                        "min",
                        "MIN"
                        ],
                        [
                        "max",
                        "MAX"
                        ],
                        [
                        "argmin",
                        "ARGMIN"
                        ],
                        [
                        "argmax",
                        "ARGMAX"
                        ],
                        [
                        "pinv",
                        "PINV"
                        ],
                        [
                        "hat",
                        "HAT"
                        ],
                        [
                        "sum",
                        "SUM"
                        ],
                        [
                        "prod",
                        "PROD"
                        ]
                    ]
                    },
                    {
                    "type": "input_value",
                    "name": "INPUT"
                    }
                ],
                "output": null,
                "colour": 230,
                "tooltip": "",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['linalg_unary_op'] = function(block) {
                            var dropdown_op = block.getFieldValue('OP');
                            var value_input = Blockly.Python.valueToCode(block, 'INPUT', Blockly.Python.ORDER_ATOMIC);
                            // TODO: Assemble Python into code variable.
                            var code = 'null';
                            // TODO: Change ORDER_NONE to the correct strength.
                            return [code, Blockly.Python.ORDER_NONE];
                            };
                            """
    )

    blocks["linalg_binary_op"] = PyriBlocklyBlock(
        name = "linalg_binary_op",
        category = "Linalg",
        doc = "Linear algebra binary op",
        json = """{
                "type": "linalg_binary_op",
                "message0": "%1 %2 %3 %4",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "A"
                    },
                    {
                    "type": "field_dropdown",
                    "name": "OP",
                    "options": [
                        [
                        "matrix add",
                        "MATRIXSUM"
                        ],
                        [
                        "matrix subtract",
                        "MATRIXSUB"
                        ],
                        [
                        "matrix multiply",
                        "MATRIXMULT"
                        ],
                        [
                        "element add",
                        "ELEMENTADD"
                        ],
                        [
                        "element subtract",
                        "ELEMENTSUB"
                        ],
                        [
                        "element multiply",
                        "ELEMENTMULT"
                        ],
                        [
                        "element divide",
                        "ELEMENTDIV"
                        ],
                        [
                        "dot",
                        "DOT"
                        ],
                        [
                        "cross",
                        "CROSS"
                        ],
                        [
                        "matrix solve",
                        "MATRIXSOLVE"
                        ],
                        [
                        "diag",
                        "DIAG"
                        ],
                        [
                        "trace",
                        "TRACE"
                        ]
                    ]
                    },
                    {
                    "type": "input_value",
                    "name": "NAME"
                    },
                    {
                    "type": "input_dummy"
                    }
                ],
                "output": null,
                "colour": 230,
                "tooltip": "",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['linalg_binary_op'] = function(block) {
                            var value_a = Blockly.Python.valueToCode(block, 'A', Blockly.Python.ORDER_ATOMIC);
                            var dropdown_op = block.getFieldValue('OP');
                            var value_name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_ATOMIC);
                            // TODO: Assemble Python into code variable.
                            var code = 'null';
                            // TODO: Change ORDER_NONE to the correct strength.
                            return [code, Blockly.Python.ORDER_NONE];
                            };
                            """
    )

    blocks["linalg_vector_get"] = PyriBlocklyBlock(
        name = "linalg_vector_get",
        category = "Linalg",
        doc = "Get vector element m",
        json = """{
                "type": "linalg_vector_get",
                "message0": "in vector %1 get element %2 %3",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "VECTOR"
                    },
                    {
                    "type": "input_value",
                    "name": "M",
                    "check": "Number"
                    },
                    {
                    "type": "input_dummy"
                    }
                ],
                "output": null,
                "colour": 230,
                "tooltip": "Get vector element m",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['linalg_vector_get'] = function(block) {
                            var value_vector = Blockly.Python.valueToCode(block, 'VECTOR', Blockly.Python.ORDER_ATOMIC);
                            var value_m = Blockly.Python.valueToCode(block, 'M', Blockly.Python.ORDER_ATOMIC);
                            // TODO: Assemble Python into code variable.
                            var code = 'null';
                            // TODO: Change ORDER_NONE to the correct strength.
                            return [code, Blockly.Python.ORDER_NONE];
                            };
                            """
        
    )

    blocks["linalg_vector_set"] = PyriBlocklyBlock(
        name = "linalg_vector_set",
        category = "Linalg",
        doc = "Set vector element m",
        json = """{
                "type": "linalg_vector_set",
                "message0": "in vector %1 set element %2 as %3 %4",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "VECTOR"
                    },
                    {
                    "type": "input_value",
                    "name": "M",
                    "check": "Number"
                    },
                    {
                    "type": "input_value",
                    "name": "VALUE",
                    "check": "Number"
                    },
                    {
                    "type": "input_dummy"
                    }
                ],
                "output": null,
                "colour": 230,
                "tooltip": "Set vector element m",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['linalg_vector_set'] = function(block) {
                            var value_vector = Blockly.Python.valueToCode(block, 'VECTOR', Blockly.Python.ORDER_ATOMIC);
                            var value_m = Blockly.Python.valueToCode(block, 'M', Blockly.Python.ORDER_ATOMIC);
                            var value_value = Blockly.Python.valueToCode(block, 'VALUE', Blockly.Python.ORDER_ATOMIC);
                            // TODO: Assemble Python into code variable.
                            var code = 'null';
                            // TODO: Change ORDER_NONE to the correct strength.
                            return [code, Blockly.Python.ORDER_NONE];
                            }
                            """
        
    )

    blocks["linalg_vector_length"] = PyriBlocklyBlock(
        name = "linalg_vector_length",
        category = "Linalg",
        doc = "Get vector length",
        json = """{
                "type": "linalg_vector_length",
                "message0": "length of vector %1",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "VECTOR"
                    }
                ],
                "output": null,
                "colour": 230,
                "tooltip": "Length of vector",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['linalg_vector_length'] = function(block) {
                            var value_vector = Blockly.Python.valueToCode(block, 'VECTOR', Blockly.Python.ORDER_ATOMIC);
                            // TODO: Assemble Python into code variable.
                            var code = 'null'
                            // TODO: Change ORDER_NONE to the correct strength.
                            return [code, Blockly.Python.ORDER_NONE];
                            };
                            """
        
    )

    blocks["linalg_matrix_get"] = PyriBlocklyBlock(
        name = "linalg_matrix_get",
        category = "Linalg",
        doc = "Get matrix element m x n",
        json = """{
                "type": "linalg_matrix_get",
                "message0": "in matrix %1 get element %2 , %3 %4",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "MATRIX"
                    },
                    {
                    "type": "input_value",
                    "name": "M",
                    "check": "Number"
                    },
                    {
                    "type": "input_value",
                    "name": "N",
                    "check": "Number"
                    },
                    {
                    "type": "input_dummy"
                    }
                ],
                "output": null,
                "colour": 230,
                "tooltip": "Get matrix element m x n",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['linalg_matrix_get'] = function(block) {
                            var value_matrix = Blockly.Python.valueToCode(block, 'MATRIX', Blockly.Python.ORDER_ATOMIC);
                            var value_m = Blockly.Python.valueToCode(block, 'M', Blockly.Python.ORDER_ATOMIC);
                            var value_n = Blockly.Python.valueToCode(block, 'N', Blockly.Python.ORDER_ATOMIC);
                            // TODO: Assemble Python into code variable.
                            var code = 'null';
                            // TODO: Change ORDER_NONE to the correct strength.
                            return [code, Blockly.Python.ORDER_NONE];
                            };
                            """
        
    )

    blocks["linalg_matrix_set"] = PyriBlocklyBlock(
        name = "linalg_matrix_set",
        category = "Linalg",
        doc = "Set matrix element m x n",
        json = """{
            "type": "linalg_matrix_set",
            "message0": "in matrix %1 set element %2 , %3 as %4 %5",
            "args0": [
                {
                "type": "input_value",
                "name": "MATRIX"
                },
                {
                "type": "input_value",
                "name": "M",
                "check": "Number"
                },
                {
                "type": "input_value",
                "name": "N",
                "check": "Number"
                },
                {
                "type": "input_value",
                "name": "VALUE",
                "check": "Number"
                },
                {
                "type": "input_dummy"
                }
            ],
            "output": null,
            "colour": 230,
            "tooltip": "Set matrix element m x n",
            "helpUrl": ""
            }""",
        python_generator = """Blockly.Python['linalg_matrix_set'] = function(block) {
            var value_matrix = Blockly.Python.valueToCode(block, 'MATRIX', Blockly.Python.ORDER_ATOMIC);
            var value_m = Blockly.Python.valueToCode(block, 'M', Blockly.Python.ORDER_ATOMIC);
            var value_n = Blockly.Python.valueToCode(block, 'N', Blockly.Python.ORDER_ATOMIC);
            var value_value = Blockly.Python.valueToCode(block, 'VALUE', Blockly.Python.ORDER_ATOMIC);
            // TODO: Assemble Python into code variable.
            var code = 'return null;';
            // TODO: Change ORDER_NONE to the correct strength.
            return [code, Blockly.Python.ORDER_NONE];
            };
            """
        
    )    
    
    blocks["linalg_matrix_size"] = PyriBlocklyBlock(
        name = "linalg_matrix_size",
        category = "Linalg",
        doc = "Get matrix_size",
        json = """{
                "type": "linalg_matrix_size",
                "message0": "size of matrix %1",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "MATRIX"
                    }
                ],
                "output": null,
                "colour": 230,
                "tooltip": "Size of matrix",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['linalg_matrix_size'] = function(block) {
                            var value_matrix = Blockly.Python.valueToCode(block, 'MATRIX', Blockly.Python.ORDER_ATOMIC);
                            // TODO: Assemble Python into code variable.
                            var code = 'null'
                            // TODO: Change ORDER_NONE to the correct strength.
                            return [code, Blockly.Python.ORDER_NONE];
                            };
                            """
        
    )

    blocks["global_variable_get"] = PyriBlocklyBlock(
        name = "global_variable_get",
        category = "Globals",
        doc = "Get a global variable value",
        json = """{
                "type": "global_variable_get",
                "message0": "global %1",
                "args0": [
                    {
                    "type": "field_input",
                    "name": "NAME",
                    "text": "global_name"
                    }
                ],
                "output": null,
                "colour": 330,
                "tooltip": "Get a global variable",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['global_variable_get'] = function(block) {
                            var text_name = block.getFieldValue('NAME');
                            // TODO: Assemble Python into code variable.
                            var code = 'global_variable_get(\\\"' + text_name + '\\\")';
                            // TODO: Change ORDER_NONE to the correct strength.
                            return [code, Blockly.Python.ORDER_NONE];
                            };
                            """        
    )

    blocks["global_variable_set"] = PyriBlocklyBlock(
        name = "global_variable_set",
        category = "Globals",
        doc = "Set a global variable value",
        json = """{
                "type": "global_variable_set",
                "message0": "global %1 %2",
                "args0": [
                    {
                    "type": "field_input",
                    "name": "NAME",
                    "text": "global_name"
                    },
                    {
                    "type": "input_value",
                    "name": "VALUE"
                    }
                ],
                "previousStatement": null,
                "nextStatement": null,
                "colour": 330,
                "tooltip": "Set a global variable value",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['global_variable_set'] = function(block) {
                            var text_name = block.getFieldValue('NAME');
                            var value_value = Blockly.Python.valueToCode(block, 'VALUE', Blockly.Python.ORDER_ATOMIC);
                            // TODO: Assemble Python into code variable.
                            var code = 'global_variable_set(\\\"' + text_name + '\\\",' + value_value + ')';
                            return code;
                            };
                            """        
    )

    blocks["global_variable_add"] = PyriBlocklyBlock(
        name = "global_variable_add",
        category = "Globals",
        doc = "Add a global variable",
        json = """{
                "type": "global_variable_add",
                "message0": "add global named %1 with type %2 with value %3 with persistence %4 with reset value %5",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "NAME",
                    "check": "String"
                    },
                    {
                    "type": "field_dropdown",
                    "name": "TYPE",
                    "options": [
                        [
                        "number",
                        "NUMBER"
                        ],
                        [
                        "vector",
                        "VECTOR"
                        ],
                        [
                        "matrix",
                        "MATRIX"
                        ],
                        [
                        "string",
                        "STRING"
                        ]
                    ]
                    },
                    {
                    "type": "input_value",
                    "name": "VALUE"
                    },
                    {
                    "type": "field_dropdown",
                    "name": "PERS",
                    "options": [
                        [
                        "normal",
                        "NORMAL"
                        ],
                        [
                        "temporary",
                        "TEMPORARY"
                        ],
                        [
                        "persistent",
                        "PERSISTENT"
                        ],
                        [
                        "constant",
                        "CONSTANT"
                        ]
                    ]
                    },
                    {
                    "type": "input_value",
                    "name": "RESET_VALUE"
                    }
                ],
                "previousStatement": null,
                "nextStatement": null,
                "colour": 330,
                "tooltip": "",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['global_variable_add'] = function(block) {
                            var value_name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_ATOMIC);
                            var dropdown_type = block.getFieldValue('TYPE');
                            var value_value = Blockly.Python.valueToCode(block, 'VALUE', Blockly.Python.ORDER_ATOMIC);
                            var dropdown_pers = block.getFieldValue('PERS');
                            var value_reset_value = Blockly.Python.valueToCode(block, 'RESET_VALUE', Blockly.Python.ORDER_ATOMIC);
                            // TODO: Assemble Python into code variable.
                            var code = '\\n';
                            return code;
                            };
                            """        
    )

    blocks["global_variable_delete"] = PyriBlocklyBlock(
        name = "global_variable_delete",
        category = "Globals",
        doc = "Delete a global variable",
        json = """{
                "type": "global_variable_delete",
                "message0": "delete global %1",
                "args0": [
                    {
                    "type": "field_input",
                    "name": "NAME",
                    "text": "global_name"
                    }
                ],
                "previousStatement": null,
                "nextStatement": null,
                "colour": 330,
                "tooltip": "",
                "helpUrl": ""
                }""",
        python_generator = """Blockly.Python['global_variable_delete'] = function(block) {
                            var text_name = block.getFieldValue('NAME');
                            // TODO: Assemble Python into code variable.
                            var code = '\\n';
                            return code;
                            };
                            """        
    )



    return blocks

def _get_categories() -> Dict[str,PyriBlocklyCategory]:
    categories = {}
    categories["Globals"] = PyriBlocklyCategory(
        name = "Globals",
        json = '{"kind": "category", "name": "Globals", "colour": 330 }'
    )
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
        return list(_get_categories().keys())

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