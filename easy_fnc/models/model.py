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

    def get_function_calls(
            self, 
            user_input: str, 
            verbose: bool = False
        ) -> list[dict]:
        """
        Get the function calls from the user input.
        """
        pass 
