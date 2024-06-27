import inspect
from typing import Dict, List, Callable, Any
import logging

from easy_fnc.functions import get_user_defined_functions
from easy_fnc.core_utils import get_core_utils
from easy_fnc.schemas import FunctionCall, ModelResponse, FunctionMetadata, FunctionReturn
from easy_fnc.utils import extract_thoughts_and_function_calls

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FunctionCallingEngine:
    """
    Function calling engine for EasyFNC.
    """
    def __init__(
            self,
            extraction_function: Callable = extract_thoughts_and_function_calls,
            auto_load_core_utils: bool = True
        ):
        self.functions: Dict[str, Callable] = {**get_core_utils()} if auto_load_core_utils else {}
        self.outputs: Dict[str, Any] = {}
        self.extraction_function: Callable = extraction_function
        logger.info("FunctionCallingEngine initialized")

    def add_user_functions(self, file_path: str) -> None:
        """
        Add user-defined functions from the specified file path.
        """
        try:
            user_functions = get_user_defined_functions(file_path)
            self.functions.update(user_functions)
            logger.info(f"Added user functions from {file_path}")
        except Exception as e:
            logger.error(f"Error adding user functions: {str(e)}")
            raise

    def parse_model_response(self, raw_response: str) -> ModelResponse:
        """
        Parse the model response and return the ModelResponse object.
        """
        try:
            return ModelResponse.from_raw_response(raw_response, self.extraction_function)
        except Exception as e:
            logger.error(f"Error parsing model response: {str(e)}")
            raise
    
    def call_functions(self, function_calls: List[FunctionCall]) -> Dict[str, Any]:
        """
        Call the functions from the given input.
        """
        def map_previous_outputs(outputs_dict: Dict[str, Any], inputs_dict: Dict[str, Any]) -> Dict[str, Any]:
            """Map the previous outputs to the input."""
            for key, value in inputs_dict.items():
                if isinstance(value, str) and value in outputs_dict:
                    inputs_dict[key] = outputs_dict[value]
                elif isinstance(value, dict):
                    inputs_dict[key] = map_previous_outputs(outputs_dict, value)
            return inputs_dict
        
        for function_call in function_calls:
            function_name = function_call.name
            function_input = function_call.kwargs

            try:
                function_input = map_previous_outputs(self.outputs, function_input)
                
                if function_name not in self.functions:
                    raise ValueError(f"Function '{function_name}' not found")

                function = self.functions[function_name]
                output = function(**function_input)

                if function_call.returns:
                    if len(function_call.returns) == 1:
                        self.outputs[function_call.returns[0]] = output
                    else:
                        for i, return_value in enumerate(function_call.returns):
                            self.outputs[return_value] = output[i]
                
                logger.info(f"Successfully called function: {function_name}")
            except Exception as e:
                logger.error(f"Error calling function {function_name}: {str(e)}")
                raise

        return self.outputs

def create_functions_metadata(functions: Dict[str, Callable]) -> List[FunctionMetadata]:
    """Creates the functions metadata for the prompt."""
    functions_metadata = []
    for name, function in functions.items():
        try:
            annotations = function.__annotations__
            parameters = {
                param: annotations.get(param, Any).__name__
                for param in inspect.signature(function).parameters
                if param != 'return'
            }
            returns = [FunctionReturn(name=f"{name}_output", type=annotations.get('return', Any).__name__)]
            
            metadata = FunctionMetadata(
                name=name,
                description=function.__doc__ or "No description provided",
                parameters={"properties": parameters, "required": list(parameters.keys())},
                returns=returns
            )
            functions_metadata.append(metadata)
        except Exception as e:
            logger.error(f"Error creating metadata for function {name}: {str(e)}")
            raise

    return functions_metadata