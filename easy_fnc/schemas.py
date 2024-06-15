from pydantic import BaseModel, Field

import json

from easy_fnc.utils import extract_thoughts_and_function_calls

class FunctionCall(BaseModel):
    """
    Pydantic model for the function call.
    """
    name: str = Field(..., description="The name of the function to be called")
    kwargs: dict = Field({}, description="The keyword arguments for the function to be called")
    returns: list[str] = Field([], description="The return values of the function that is called")

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a FunctionCall object from a dictionary.
        """
        return cls(**data)

class ModelResponse(BaseModel):
    """
    Pydantic model for the model response.
    """
    thoughts: str = Field(..., description="The thoughts of the model")
    function_calls: list[FunctionCall] = Field([], description="The function calls made by the model")

    @classmethod
    def from_raw_response(
        cls, 
        raw_response: str,
        extraction_function: callable = extract_thoughts_and_function_calls
    ):
        """
        Create a ModelResponse object from the raw response.

        Args:
        - raw_response (str): 
            The raw response from the model.
        - extraction_function (callable): 
            The function to extract the thoughts and function calls from the raw 
            response. Should return a tuple of thoughts and function calls string.
        """
        # Extract the thoughts and function calls
        thoughts, function_calls_str = extraction_function(raw_response)

        if len(thoughts) < 1 and len(function_calls_str) < 1:
            raise ValueError("No thoughts or function calls found in the raw response")
    
        # Parse the function calls
        try:
            function_calls_loaded = json.loads(function_calls_str)
        except json.JSONDecodeError:
            raise ValueError("Error parsing function calls from the raw response")
        
        function_calls = [FunctionCall.from_dict(data) for data in function_calls_loaded]
        
        return cls(thoughts=thoughts, function_calls=function_calls)
    
    def __str__(self):
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