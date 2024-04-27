from abc import ABC, abstractmethod

class EasyFNCModel(ABC):
    """
    Abstract class for EasyFNC models.
    """
    def __init__(self, functions: list[dict[str, str]]) -> None:
        self.functions = functions

    @abstractmethod
    def generate(self, user_input: str) -> dict:
        """
        Generate a response based on the user input.
        """
        pass

    def get_function_calls(self, user_input: str) -> list[dict]:
        """
        Get the function calls from the user input.
        """
        # Get the model response and extract the content
        model_response = self.generate(user_input)
        content = model_response["message"]["content"]

        # Extract the function calls 
        # They're in between <|function_calls|> and <|end_function_calls|> tags
        function_calls = content.split("<|function_calls|>")[1].split("<|end_function_calls|>")[0].strip()

        pass
