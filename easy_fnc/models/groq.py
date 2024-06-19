import os

from groq import Groq

from easy_fnc.utils import get_template_path
from easy_fnc.models.model import EasyFNCModel

class GroqModel(EasyFNCModel):
    """A class to interact with the Groq API and chat with the model"""
    def __init__(
            self, 
            functions: list[dict[str, str]],
            model_name: str = os.environ.get("GROQ_MODEL"),
            template_path: str = get_template_path(),
            template_type: str = "toml"
        ):
        super().__init__(functions, template_path, template_type)
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = model_name
        self.messages = [{"role": "system", "content": self.generate_system_prompt().replace("<|user_query|>", "")}]

        if os.environ.get("GROQ_MODEL") is None:
            print("No GROQ_MODEL environment variable found. Using: llama3-70b-8192.")
            self.model_name = "llama3-8b-8192"
        else: 
            self.model_name = os.environ.get("GROQ_MODEL")

        if os.environ.get("GROQ_API_KEY") is None:
            print("No GROQ_API_KEY environment variable found. Please set it to your Groq API key.")

    def generate(self, user_message: str) -> str:
        """Chat with the model and return the response"""
        # Create a message object for the user input
        self.messages.append({"role": "user", "content": self.format_user_input(user_message)})

        # Get the chat completion from the model
        return self._get_chat_completion(self.messages)

    def _get_chat_completion(self, messages) -> str:
        """Get the chat completion from the model"""
        model_response = self.client.chat.completions.create(messages=messages, model=self.model_name).choices[0].message.content

        # Add the model response to the messages
        self.messages.append({"role": "assistant", "content": model_response})

        return model_response