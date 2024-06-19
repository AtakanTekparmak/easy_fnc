import ollama

import json

from easy_fnc.models.model import EasyFNCModel
from easy_fnc.utils import get_template_path

class OllamaModel(EasyFNCModel):
    """
    A class to generate responses using the Ollama model.
    """
    def __init__(
            self, 
            model_name: str, 
            functions: list[dict[str, str]],
            template_path: str = get_template_path(),
            template_type: str = "toml"
        ) -> None:
        super().__init__(functions, template_path, template_type)
        self.model_name = model_name
        self.messages = [{"role": "system", "content": self.generate_system_prompt().replace("<|user_query|>", "")}]

    def format_output(self, output: any, original_prompt: str) -> str:
        """ Format the output. """
        prompt = self.template["function_response_prompt"]["beginning"] + original_prompt
        prompt += self.template["function_response_prompt"]["middle"]
        prompt += json.dumps(output, indent=4)
        prompt += self.template["function_response_prompt"]["end"]

        return prompt
    
    def generate(
            self, 
            user_input: str
            ) -> str:
        """
        Generate a response based on the user input.
        """
        # Get the model response and extract the content
        self.messages.append({"role": "user", "content": self.format_user_input(user_input)})
        model_response = ollama.chat(
            model=self.model_name,
            messages=self.messages
        )

        content = model_response["message"]["content"].strip().replace("\'", "\"")

        return content