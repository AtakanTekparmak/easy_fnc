import inspect
from ast import literal_eval

from easy_fnc.functions import get_user_defined_functions
from easy_fnc.core_utils import get_core_utils

class FunctionCaller:
    """
    A class to call functions from user-defined functions and core utilities.
    """

    def __init__(self):
        # Initialize the functions dictionary
        core_utils = get_core_utils()
        self.functions = {**core_utils}
        self.outputs = {}

    def add_user_functions(self, file_path: str):
        """
        Add user-defined functions from the specified file path.
        """
        user_functions = get_user_defined_functions(file_path)
        self.functions.update(user_functions)

    def create_functions_metadata(self) -> list[dict]:
        """Creates the functions metadata for the prompt. """
        def format_type(p_type: str) -> str:
            """Format the type of the parameter."""
            # If p_type begins with "<class", then it is a class type
            if p_type.startswith("<class"):
                # Get the class name from the type
                p_type = p_type.split("'")[1]
            
            return p_type
            
        functions_metadata = []
        i = 0
        for name, function in self.functions.items():
            i += 1
            descriptions = function.__doc__.split("\n")
            functions_metadata.append({
                "name": name,
                "description": descriptions[0],
                "parameters": {
                    "properties": [ # Get the parameters for the function
                        {   
                            "name": param_name,
                            "type": format_type(str(param_type)),
                        }
                        # Remove the return type from the parameters
                        for param_name, param_type in function.__annotations__.items() if param_name != "return"
                    ],
                    
                    "required": [param_name for param_name in function.__annotations__ if param_name != "return"],
                } if function.__annotations__ else {},
                "returns": [
                    {
                        "name": name + "_output",
                        "type": {param_name: format_type(str(param_type)) for param_name, param_type in function.__annotations__.items() if param_name == "return"}["return"]
                    }
                ]
            })

        return functions_metadata

    def call_function(self, function):
        """
        Call the function from the given input.

        Args:
            function (dict): A dictionary containing the function details.
        """
    
        def check_if_input_is_output(input: dict) -> dict:
            """Check if the input is an output from a previous function."""
            for key, value in input.items():
                if value in self.outputs:
                    input[key] = self.outputs[value]
                # Check if value is a string encased by dollar signs
                if value.startswith("$") and value.endswith("$") and not key.lower() == "key":
                    input[key] = self.outputs[value[1:-1]]
            return input
        
        def check_if_input_is_function(input: dict) -> dict:
            """Check if the input is a function."""
            # Currently experimental, not working as expected
            for key, value in input.items():
                if value in self.functions.keys():
                    input[key] = self.functions[value]
            return input
        
        def format_input(input: dict) -> dict:
            """Format the input for the function."""
            for key, value in input.items():
                if not isinstance(value, str):
                    input[key] = str(value)
                    if input[key].startswith("$") and input[key].endswith("$") and not key.lower() == "key":
                        input[key] = input[key][1:-1]
                        if input[key] in self.outputs:
                            input[key] = self.outputs[value]
                if isinstance(value, int):
                    input[key] = value
                # If a value is encased by "{" and "}", then it is a variable
                if "{" in value and "}" in value:
                    # Get the variable name
                    variable_name = value.split("{")[1].split("}")[0]
                    # Get the value from the outputs
                    input[key] = variable_name 
            
            return input
        
        def infer_input_type(input: dict) -> dict:
            """Infer the input type for the function."""
            for key, value in input.items():
                # If the value is a string, then check if it is a number
                if isinstance(value, str):
                    # Check if the value is an integer
                    if value.isdigit():
                        input[key] = int(value)
                    elif value.startswith("$") and value.endswith("$") and not key.lower() == "key":
                        input[key] = self.outputs[value[1:-1]]
                    # Check if the value is a float
                    elif "." in value and value.replace(".", "").isdigit():
                        input[key] = float(value)
                    # Check if the value is a boolean
                    elif value.lower() in ["true", "false"]:
                        input[key] = value.lower() == "true"
                    # Check if the value is a list
                    elif value.startswith("[") and value.endswith("]"):
                        input[key] = literal_eval(value)
                    # Check if the value is a dictionary
                    elif value.startswith("{") and value.endswith("}"):
                        input[key] = literal_eval(value)
            
            return input
        
        def remove_the_dollarsign(input: dict) -> dict:
            """Removes the dollarsign from the input."""
            for key, value in input.items():
                if isinstance(value, str):
                    if value.startswith("$") and value.endswith("$") and not key.lower() == "key":
                        input[key] = value[1:-1]
                        input[key] = self.outputs[input[key]]
                if isinstance(value, dict):
                    input[key] = remove_the_dollarsign(value)
            return input

        # Get the function name from the function dictionary
        function_name = function["name"]
        
        # Get the function params from the function dictionary
        function_input = function["params"] if "params" in function else None
        function_input = format_input(function_input) if function_input else None
        function_input = check_if_input_is_output(function_input) if function_input else None
        function_input = check_if_input_is_function(function_input) if function_input else None
        function_input = infer_input_type(function_input) if function_input else None
        function_input = remove_the_dollarsign(function_input) if function_input else None
    
        # Call the function from tools.py with the given input
        # pass all the arguments to the function from the function_input
        output = self.functions[function_name](**function_input) if function_input else self.functions[function_name]()
        # Check if output is enclosed by dollar signs
        if isinstance(output, str):
            if output.startswith("$") and output.endswith("$"):
                output = output[1:-1]
        # Check if function["output"] is a string encased by dollar signs
        if function["output"].startswith("$") and function["output"].endswith("$"):
            function_output = function["output"][1:-1]
        else:
            function_output = function["output"]
        self.outputs[function_output] = output if output else None
        return output if output else None

    