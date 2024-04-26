import inspect
from easy_fnc.functions import get_user_defined_functions

class FunctionCaller:
    """
    A class to call functions from tools.py.
    """

    def __init__(self):
        # Initialize the functions dictionary
        self.functions = get_user_defined_functions("easy_fnc/functions.py")
        self.outputs = {}

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
            return input

        # Get the function name from the function dictionary
        function_name = function["name"]
        
        # Get the function params from the function dictionary
        function_input = function["params"] if "params" in function else None
        function_input = check_if_input_is_output(function_input) if function_input else None
    
        # Call the function from tools.py with the given input
        # pass all the arguments to the function from the function_input
        output = self.functions[function_name](**function_input) if function_input else self.functions[function_name]()
        self.outputs[function["output"]] = output
        return output

    