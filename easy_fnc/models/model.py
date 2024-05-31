from abc import ABC, abstractmethod
from json import load as load_json
from typing import Optional

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
        template_dir: Optional[str] = None
        ) -> dict:
        """
        Load a template from the specified directory or the default template directory.
        """
        if template_dir is None:
            template_dir = "easy_fnc/models/templates/"
    
        with open(f"{template_dir}{template_name}.json", "r") as file:
            return load_json(file)
    
