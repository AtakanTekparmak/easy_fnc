from abc import ABC, abstractmethod
import json
from typing import List

from easy_fnc.utils import load_template, get_template_path
from easy_fnc.schemas import FunctionMetadata


class EasyFNCModel(ABC):
    """
    Abstract class for EasyFNC models.
    """
    def __init__(
            self, 
            functions: List[FunctionMetadata],
            template_path: str = get_template_path(),
            template_type: str = "toml"
        ) -> None:
        self.functions = functions
        self.template = load_template(file_path=template_path, file_type=template_type)

    def generate_system_prompt(self) -> str:
        prompt_beginning = self.template["function_call_prompt"]["beginning"]
        system_prompt_end = self.template["function_call_prompt"]["system_prompt_end"]
        return prompt_beginning + json.dumps([f.model_dump() for f in self.functions], indent=4) + system_prompt_end
    
    def format_user_input(self, user_input: str) -> str:
        return "<|user_query|>" + user_input + "<|end_user_query|>"

    @abstractmethod
    def generate(self, user_input: str) -> str:
        pass