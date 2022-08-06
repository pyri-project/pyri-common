from ast import arg
from pyri.plugins.blockly import PyriBlocklyPluginFactory, PyriBlocklyBlock, PyriBlocklyCategory, add_blockly_block, \
    PyriBlocklyBlockArgument, PyriBlocklyBlockFunctionSelector
from pyri.plugins.blockly import PyriBlocklyBlockArgumentInterpretation as argtype
from typing import List, Dict, NamedTuple, TYPE_CHECKING
from ..sandbox_functions import sandbox_functions

def _get_blocks() -> Dict[str,PyriBlocklyBlock]:
    blocks = {}
    
    add_blockly_block(blocks,
        category = "Time",
        blockly_json = {
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
                "previousStatement": None,
                "nextStatement": None,
                "colour": 65,
                "tooltip": "Wait a specified number of seconds",
                "helpUrl": ""
                },

        sandbox_function=(sandbox_functions.time_wait,"WAIT_TIME")
    )

    add_blockly_block(blocks,
        category = "Time",
        blockly_json = {
                "type": "time_wait_for_completion",
                "message0": "wait for device %1 action to complete with %2 second timeout",
                "args0": [
                    {
                    "type": "field_input",
                    "name": "DEVICE_NAME",
                    "text": "robot"
                    },
                    {
                    "type": "field_number",
                    "name": "TIMEOUT",
                    "value": 15,
                    "min": 0,
                    "max": 3600
                    }
                ],
                "previousStatement": None,
                "nextStatement": None,
                "colour": 65,
                "tooltip": "Wait for device action to complete with timeout specified in seconds",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.time_wait_for_completion, "DEVICE_NAME", "TIMEOUT")
    )

    add_blockly_block(blocks,
        category = "Time",
        blockly_json = {
                "type": "time_wait_for_completion_all",
                "message0": "wait for device actions to complete with %1 second timeout",
                "args0": [
                    {
                    "type": "field_number",
                    "name": "TIMEOUT",
                    "value": 15,
                    "min": 0,
                    "max": 3600
                    }
                ],
                "previousStatement": None,
                "nextStatement": None,
                "colour": 65,
                "tooltip": "Wait for all device actions to complete with timeout specified in seconds",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.time_wait_for_completion_all, "TIMEOUT")
    )

    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
                "type": "linalg_vector",
                "message0": "new vector [ %1 ]",
                "args0": [
                    {
                    "type": "field_input",
                    "name": "VECTOR",
                    "text": ""
                    }
                ],
                "output": None,
                "colour": 230,
                "tooltip": "Create a new vector",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.linalg_vector, "VECTOR"),
        sandbox_function_arguments = [
            PyriBlocklyBlockArgument(
                blockly_arg_name="VECTOR",
                sandbox_function_arg_name= "vector",
                arg_interpretation=argtype.QUOTE
            )
        ]
        
    )
    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
                "type": "linalg_matrix",
                "message0": "new matrix %1 ",
                "args0": [
                    {
                    "type": "field_input",
                    "name": "MATRIX",
                    "text": ""
                    }
                ],
                "output": None,
                "colour": 230,
                "tooltip": "Create a new matrix",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.linalg_matrix, "MATRIX"),
        sandbox_function_arguments = [
            PyriBlocklyBlockArgument(
                blockly_arg_name="MATRIX",
                sandbox_function_arg_name= "string_matrix",
                arg_interpretation=argtype.QUOTE
            )
        ]
        
    )
    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
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
                "output": None,
                "colour": 230,
                "tooltip": "Create vector with length m and fill with value",
                "helpUrl": ""
                },
        sandbox_function=(sandbox_functions.linalg_fill_vector,"M","VALUE")
        
    )
    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
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
                "output": None,
                "colour": 230,
                "tooltip": "Create matrix with size m,n and fill with value",
                "helpUrl": ""
                },
        sandbox_function=(sandbox_functions.linalg_fill_matrix,"M","N","VALUE")
    )
    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
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
                        "determinant",
                        "DETERMINANT"
                        ],
                        [
                        "conjugate",
                        "CONJUGATE"
                        ],
                        [
                        "eigenvalues",
                        "EIGENVALUES"
                        ],
                        [
                        "eigenvectors",
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
                        "trace",
                        "TRACE"
                        ],
                        [
                        "diag",
                        "DIAG"
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
                        "multiply",
                        "MULTIPLY"
                        ]
                    ]
                    },
                    {
                    "type": "input_value",
                    "name": "INPUT"
                    }
                ],
                "output": None,
                "colour": 230,
                "tooltip": "Linear algebra unary op",
                "helpUrl": ""
                },
        sandbox_function_name_selector = PyriBlocklyBlockFunctionSelector(
            selector_field = "OP",
            sandbox_function_names = {
                "TRANSPOSE": "linalg_mat_transpose",
                "INVERSE": "linalg_mat_inv",
                "NEGATIVE": "linalg_negative",
                "DETERMINANT": "linalg_mat_det",
                "CONJUGATE": "linalg_mat_conj",
                "EIGENVALUES": "linalg_mat_eigenvalues",
                "EIGENVECTORS": "linalg_mat_eigenvectors",
                "MIN": "linalg_min",
                "MAX": "linalg_man",
                "ARGMIN": "linalg_argmin",
                "ARGMAX": "linalg_argmax",
                "PINV": "linalg_mat_pinv",
                "TRACE": "linalg_mat_trace",
                "DIAG": "linalg_mat_diag",
                "HAT": "linalg_hat",
                "SUM": "linalg_sum",
                "MULTIPLY": "linalg_multiply",

            }
        ),
        sandbox_function_arguments=[
            PyriBlocklyBlockArgument(blockly_arg_name="INPUT", sandbox_function_arg_name="input", 
                arg_interpretation=argtype.CODE)
        ]
    )

    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
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
                        "MATRIXADD"
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
                        ]
                    ]
                    },
                    {
                    "type": "input_value",
                    "name": "B"
                    },
                    {
                    "type": "input_dummy"
                    }
                ],
                "output": None,
                "colour": 230,
                "tooltip": "Linear algebra binary op",
                "helpUrl": ""
                },
        sandbox_function_name_selector = PyriBlocklyBlockFunctionSelector(
            selector_field = "OP",
            sandbox_function_names = {
                "MATRIXADD": "linalg_mat_add",
                "MATRIXSUB": "linalg_mat_subtract",
                "MATRIXMULT": "linalg_mat_multiply",
                "ELEMENTADD": "linalg_elem_add",
                "ELEMENTSUB": "linalg_elem_subtract",
                "ELEMENTMULT": "linalg_elem_multiply",
                "ELEMENTDIV": "linalg_elem_divide",
                "DOT": "linalg_dot",
                "CROSS": "linalg_cross",
                "MATRIXSOLVE": "linalg_mat_solve"
            }
        ),
        sandbox_function_arguments=[
            PyriBlocklyBlockArgument(blockly_arg_name="A", sandbox_function_arg_name="a", 
                arg_interpretation=argtype.CODE),
            PyriBlocklyBlockArgument(blockly_arg_name="B", sandbox_function_arg_name="b", 
                arg_interpretation=argtype.CODE)
        ]
    )

    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
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
                "output": None,
                "colour": 230,
                "tooltip": "Get vector element m",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.linalg_vector_get_elem,"VECTOR","M")
    )

    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
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
                "output": None,
                "colour": 230,
                "tooltip": "Set vector element m",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.linalg_vector_set_elem,"VECTOR","M","VALUE")        
    )

    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
                "type": "linalg_vector_length",
                "message0": "length of vector %1",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "VECTOR"
                    }
                ],
                "output": None,
                "colour": 230,
                "tooltip": "Get length of vector",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.linalg_vector_len,"VECTOR")
    )

    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
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
                "output": None,
                "colour": 230,
                "tooltip": "Get matrix element m x n",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.linalg_matrix_get_elem,"MATRIX","M","N")
    )

    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
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
            "output": None,
            "colour": 230,
            "tooltip": "Set matrix element m x n",
            "helpUrl": ""
            },
        sandbox_function = (sandbox_functions.linalg_matrix_set_elem,"MATRIX","M","N","VALUE")
    )    
    
    add_blockly_block(blocks,
        category = "Linalg",
        blockly_json = {
                "type": "linalg_matrix_size",
                "message0": "size of matrix %1",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "MATRIX"
                    }
                ],
                "output": None,
                "colour": 230,
                "tooltip": "Size of matrix",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.linalg_matrix_size,"MATRIX")
    )

    add_blockly_block(blocks,
        category = "Globals",
        blockly_json = {
                "type": "global_variable_get",
                "message0": "global %1",
                "args0": [
                    {
                    "type": "field_input",
                    "name": "NAME",
                    "text": "global_name"
                    }
                ],
                "output": None,
                "colour": 330,
                "tooltip": "Get a global variable",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.global_variable_get, "NAME")  
    )

    add_blockly_block(blocks,
        category = "Globals",
        blockly_json = {
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
                "previousStatement": None,
                "nextStatement": None,
                "colour": 330,
                "tooltip": "Set a global variable value",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.global_variable_set,"NAME","VALUE")
    )

    add_blockly_block(blocks,
        category = "Globals",
        blockly_json = {
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
                        "array",
                        "ARRAY"
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
                "previousStatement": None,
                "nextStatement": None,
                "colour": 330,
                "tooltip": "Add a global variable",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.global_variable_add,"NAME","TYPE","VALUE","PERS","RESET_VALUE")      
    )

    add_blockly_block(blocks,
        category = "Globals",
        blockly_json = {
                "type": "global_variable_delete",
                "message0": "delete global %1",
                "args0": [
                    {
                    "type": "field_input",
                    "name": "NAME",
                    "text": "global_name"
                    }
                ],
                "previousStatement": None,
                "nextStatement": None,
                "colour": 330,
                "tooltip": "Delete a global variable",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.global_variable_delete,"NAME")       
    )

    add_blockly_block(blocks,
        category = "Geometry",
        blockly_json = {
                "type": "geometry_pose_new",
                "message0": "new pose    x %1 y %2 z %3 R %4 P %5 Y %6",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "X",
                    "check": "Number"
                    },
                    {
                    "type": "input_value",
                    "name": "Y",
                    "check": "Number",
                    "align": "RIGHT"
                    },
                    {
                    "type": "input_value",
                    "name": "Z",
                    "check": "Number",
                    "align": "RIGHT"
                    },
                    {
                    "type": "input_value",
                    "name": "R_X",
                    "check": "Number",
                    "align": "RIGHT"
                    },
                    {
                    "type": "input_value",
                    "name": "R_P",
                    "check": "Number",
                    "align": "RIGHT"
                    },
                    {
                    "type": "input_value",
                    "name": "R_Y",
                    "check": "Number",
                    "align": "RIGHT"
                    }
                ],
                "output": None,
                "colour": 230,
                "tooltip": "Create a new pose",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.geometry_pose_new,"X","Y","Z","R_X","R_P","R_Y")
    )

    add_blockly_block(blocks,
        category = "Geometry",
        blockly_json = {
                "type": "geometry_pose_component_get",
                "message0": "get pose component %1 %2",
                "args0": [
                    {
                    "type": "field_dropdown",
                    "name": "COMPONENT",
                    "options": [
                        [
                        "x",
                        "X"
                        ],
                        [
                        "y",
                        "Y"
                        ],
                        [
                        "z",
                        "Z"
                        ],
                        [
                        "R",
                        "R_R"
                        ],
                        [
                        "P",
                        "R_P"
                        ],
                        [
                        "Y",
                        "R_Y"
                        ]
                    ]
                    },
                    {
                    "type": "input_value",
                    "name": "POSE"
                    }
                ],
                "output": None,
                "colour": 230,
                "tooltip": "Get component of a pose",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.geometry_pose_component_get,"POSE","COMPONENT")
    )

    add_blockly_block(blocks,
        category = "Geometry",
        blockly_json = {
            "type": "geometry_pose_component_set",
            "message0": "set pose %1 component %2 %3",
            "args0": [
                {
                "type": "input_value",
                "name": "POSE"
                },
                {
                "type": "field_dropdown",
                "name": "COMPONENT",
                "options": [
                    [
                    "x",
                    "X"
                    ],
                    [
                    "y",
                    "Y"
                    ],
                    [
                    "z",
                    "Z"
                    ],
                    [
                    "R",
                    "R_R"
                    ],
                    [
                    "P",
                    "R_P"
                    ],
                    [
                    "Y",
                    "R_Y"
                    ]
                ]
                },
                {
                "type": "input_value",
                "name": "VALUE"
                }
            ],
            "output": None,
            "colour": 230,
            "tooltip": "Set component of a pose",
            "helpUrl": ""
            },
        sandbox_function = (sandbox_functions.geometry_pose_component_set,"POSE","COMPONENT","VALUE")
    )

    add_blockly_block(blocks,
        category = "Geometry",
        blockly_json = {
                "type": "geometry_pose_multiply",
                "message0": "pose multiply %1 times %2 %3",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "A"
                    },
                    {
                    "type": "input_value",
                    "name": "B"
                    },
                    {
                    "type": "input_dummy"
                    }
                ],
                "output": None,
                "colour": 230,
                "tooltip": "Set component of a pose",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.geometry_pose_multiply,"A","B")
        )

    add_blockly_block(blocks,
        category = "Geometry",
        blockly_json = {
                "type": "geometry_pose_inv",
                "message0": "pose inv %1",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "A"
                    }
                ],
                "output": None,
                "colour": 230,
                "tooltip": "Get inverse of pose",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.geometry_pose_inv,"A")
        )

    add_blockly_block(blocks,
            category = "Util",
            blockly_json = {
                    "type": "util_copy",
                    "message0": "copy value %1",
                    "args0": [
                        {
                        "type": "input_value",
                        "name": "VALUE"
                        }
                    ],
                    "output": None,
                    "colour": 330,
                    "tooltip": "Copy a value",
                    "helpUrl": ""
                    },
            sandbox_function = (sandbox_functions.util_copy,"VALUE")
        )

    add_blockly_block(blocks,
        category = "Util",
        blockly_json = {
                "type": "proc_result_get",
                "message0": "procedure result",
                "output": None,
                "colour": 330,
                "tooltip": "Get the current procedure result",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.proc_result_get,)     
    )

    add_blockly_block(blocks,
        category = "Util",
        blockly_json = {
                "type": "proc_result_set",
                "message0": "procedure result %1",
                "args0": [
                    {
                    "type": "input_value",
                    "name": "VALUE"
                    }
                ],
                "previousStatement": None,
                "nextStatement": None,
                "colour": 330,
                "tooltip": "Set a global variable value",
                "helpUrl": ""
                },
        sandbox_function = (sandbox_functions.proc_result_set,"VALUE")      
    )

    return blocks

def _get_categories() -> Dict[str,PyriBlocklyCategory]:
    categories = {}
    categories["Util"] = PyriBlocklyCategory(
        name = "Util",
        json = '{"kind": "category", "name": "Util", "colour": 330 }'
    )
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

    categories["Geometry"] = PyriBlocklyCategory(
        name = "Geometry",
        json = '{"kind": "category", "name": "Geometry", "colour": 230}'
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