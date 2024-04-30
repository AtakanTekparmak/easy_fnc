from abc import ABC, abstractmethod
from json import load as load_json

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

    @abstractmethod
    def get_function_calls(
            self, 
            user_input: str, 
            verbose: bool = False
        ) -> list[dict]:
        """
        Get the function calls from the user input.
        """

    def load_template(
        self, 
        template_name: str,
        template_dir: str = "easy_fnc/models/templates/"
    ) -> dict:
        """
        Load a template from the template directory.
        """
        with open(f"{template_dir}{template_name}.json", "r") as file:
            return load_json(file)
    
