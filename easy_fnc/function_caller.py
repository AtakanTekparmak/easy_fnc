import inspect
from ast import literal_eval

from easy_fnc.functions import get_user_defined_functions
from easy_fnc.core_utils import get_core_utils
from easy_fnc.schemas import FunctionCall, ModelResponse
from easy_fnc.utils import extract_thoughts_and_function_calls

class FunctionCallingEngine:
    """
    Function calling engine for EasyFNC.
    """
    def __init__(
            self,
            extraction_function: callable = extract_thoughts_and_function_calls,
        ):
        # Initialize the functions dictionary
        core_utils = get_core_utils()
        self.functions = {**core_utils}
        self.outputs = {}
        self.extraction_function = extraction_function

    def add_user_functions(self, file_path: str):
        """
        Add user-defined functions from the specified file path.
        """
        user_functions = get_user_defined_functions(file_path)
        self.functions.update(user_functions)

    def parse_model_response(self, raw_response: str) -> ModelResponse:
        """
        Parse the model response and return the ModelResponse object.
        """
        return ModelResponse.from_raw_response(raw_response, self.extraction_function)
    
    def call_functions(self, function_calls: list[FunctionCall]) -> dict:
        """
        Call the functions from the given input.
        """
        def map_previous_outputs(outputs_dict: dict, inputs_dict: dict) -> dict:
            """Map the previous outputs to the input."""
            for key, value in inputs_dict.items():
                if isinstance(value, str):
                    if value in outputs_dict:
                        inputs_dict[key] = outputs_dict[value]
                if isinstance(value, dict):
                    inputs_dict[key] = map_previous_outputs(value)

            return inputs_dict
        
        for function_call in function_calls:
            function_name = function_call.name
            function_input = function_call.kwargs

            # Check if the input is an output from a previous function
            function_input = map_previous_outputs(self.outputs, function_input)

            if function_call.returns:
                # Switch case for length of returns
                match len(function_call.returns):
                    case 0:
                        # Call the function with no returns
                        output = self.functions[function_name]()
                        self.outputs[function_call.returns[0]] = output
                    case 1:
                        # Call the function with one return
                        output = self.functions[function_name](**function_input)
                        self.outputs[function_call.returns[0]] = output
                    case _:
                        # Call the function with one or more returns
                        outputs_tuple = self.functions[function_name](**function_input) 
                        for i in range(len(function_call.returns)):
                            self.outputs[function_call.returns[i]] = outputs_tuple[i]

        return self.outputs if self.outputs else {}

def create_functions_metadata(functions: dict) -> list[dict]:
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
        for name, function in functions.items():
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