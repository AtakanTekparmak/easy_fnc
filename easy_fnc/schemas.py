from typing import List, Dict, Any, Callable
from pydantic import BaseModel, Field, validator
import json
import logging

from easy_fnc.utils import extract_thoughts_and_function_calls

logger = logging.getLogger(__name__)

class FunctionParameter(BaseModel):
    name: str
    type: str

class FunctionReturn(BaseModel):
    name: str
    type: str

class FunctionMetadata(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any] = Field(..., description="Function parameters")
    returns: List[FunctionReturn]

class FunctionCall(BaseModel):
    """
    Pydantic model for the function call.
    """
    name: str = Field(..., description="The name of the function to be called")
    kwargs: Dict[str, Any] = Field(default_factory=dict, description="The keyword arguments for the function to be called")
    returns: List[str] = Field(default_factory=list, description="The return values of the function that is called")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FunctionCall':
        """
        Create a FunctionCall object from a dictionary.
        """
        try:
            return cls(**data)
        except Exception as e:
            logger.error(f"Error creating FunctionCall from dict: {str(e)}")
            raise

class ModelResponse(BaseModel):
    """
    Pydantic model for the model response.
    """
    thoughts: str = Field(..., description="The thoughts of the model")
    function_calls: List[FunctionCall] = Field(default_factory=list, description="The function calls made by the model")

    @classmethod
    def from_raw_response(
        cls, 
        raw_response: str,
        extraction_function: Callable = extract_thoughts_and_function_calls
    ) -> 'ModelResponse':
        """
        Create a ModelResponse object from the raw response.

        Args:
        - raw_response (str): 
            The raw response from the model.
        - extraction_function (callable): 
            The function to extract the thoughts and function calls from the raw 
            response. Should return a tuple of thoughts and function calls string.
        """
        try:
            thoughts, function_calls_str = extraction_function(raw_response)

            if not thoughts and not function_calls_str:
                raise ValueError("No thoughts or function calls found in the raw response.")
        
            function_calls_loaded = json.loads(function_calls_str)
            function_calls = [FunctionCall.from_dict(data) for data in function_calls_loaded]
            
            return cls(thoughts=thoughts, function_calls=function_calls)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing function calls from the raw response: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error creating ModelResponse from raw response: {str(e)}")
            raise

    def __str__(self) -> str:
        """
        Return a string representation of the ModelResponse object.
        """
        output = "Thoughts:\n"
        output += self.thoughts.strip() + "\n\n"
        output += "Function Calls:\n"
        for function_call in self.function_calls:
            output += f"- {function_call.name}:\n"
            output += f"  - kwargs: {function_call.kwargs}\n"
            output += f"  - returns: {function_call.returns}\n"
        return output