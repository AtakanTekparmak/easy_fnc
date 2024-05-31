import ollama

import json
from typing import Union

from easy_fnc.models.model import EasyFNCModel

class OllamaModel(EasyFNCModel):
    """
    A class to generate responses using the Ollama model.
    """
    def __init__(
            self, 
            model_name: str, 
            functions: list[dict[str, str]],
            template: Union[str, dict]
        ) -> None:
        super().__init__(functions)
        self.model_name = model_name
        if isinstance(template, str):
            self.template = self.load_template(template_name=model_name.split("/")[1])
        elif isinstance(template, dict):
            self.template = template
        else:
            raise ValueError("Invalid template format. Expected a template name or a dictionary.")
    
    def format_user_input(self, user_input: str) -> str:
        """ Format the user input. """
        # Create the system prompt
        prompt_beginning = self.template["function_call_prompt"]["beginning"]
        system_prompt_end = self.template["function_call_prompt"]["system_prompt_end"]
        system_prompt = prompt_beginning + json.dumps(self.functions, indent=4) + system_prompt_end

        return system_prompt + user_input + self.template["function_call_prompt"]["prompt_end"]

    def format_output(self, output: any, original_prompt: str) -> str:
        """ Format the output. """
        prompt = self.template["function_response_prompt"]["beginning"] + original_prompt
        prompt += self.template["function_response_prompt"]["middle"]
        prompt += json.dumps(output, indent=4)
        prompt += self.template["function_response_prompt"]["end"]

        return prompt
    
    def generate(
            self, 
            user_input: str,
            first_message: bool = True,
            response_message : bool = False,
            original_prompt: str = ""
            ) -> dict:
        """
        Generate a response based on the user input.
        """
        if first_message:
            user_input = self.format_user_input(user_input)
        elif response_message:
            user_input = self.format_output(user_input, original_prompt)

        # Get the model response and extract the content
        model_response = ollama.chat(
            model=self.model_name,
            messages=[{'role': 'user', 'content': user_input}]
        )

        content = model_response["message"]["content"].strip().replace("\'", "\"")

        return content

    
    def get_function_calls(
            self, 
            user_input: str,
            verbose: bool = False
        ) -> list[dict[str, str]]:
        def extract_thoughts (content: str) -> str:
            """
            Extract the thoughts from the user input.
            """
            if "<|end_thoughts|>" in content:
                # Remove <|end_thoughts|> from the end
                thoughts = content.split("<|end_thoughts|>")[0]
                if "<|thoughts|>" in thoughts:
                    # Remove <|thoughts|> from the beginning
                    thoughts = thoughts.split("<|thoughts|>")[1]
            else :
                thoughts = content

            return thoughts
        """
        Get the function calls from the user input.
        """
        content = self.generate(user_input)
        
        if verbose:
            thoughts = extract_thoughts(content)
            print ("- Model Thoughts:")
            print(thoughts)

        # Extract the function calls 
        if "<|end_function_calls|>" in content: 
            # Remove <|end_function_calls|> from the end
            function_calls = content.split("<|end_function_calls|>")[0]
            if "<|function_calls|>" in function_calls:
                # Remove <|function_calls|> from the beginning
                function_calls = function_calls.split("<|function_calls|>")[1]
        else :
            function_calls = content

        # Read function calls as json
        try:
            function_calls_parsed: list[dict[str, str]] = json.loads(function_calls)
        except json.JSONDecodeError as e:
            print(e)
            function_calls_parsed = []
            print ("Model response not in desired JSON format")
        finally:
            if verbose and len(function_calls_parsed) > 0:
                print("- Function calls:")
                print(function_calls_parsed)
                print("")

        return function_calls_parsed

