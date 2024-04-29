import ollama
import json

from easy_fnc.models.model import EasyFNCModel

class OllamaModel(EasyFNCModel):
    """
    A class to generate responses using the Ollama model.
    """
    def __init__(self, model_name: str, functions: list[dict[str, str]]) -> None:
        super().__init__(functions)
        self.model_name = model_name
    
    def format_user_input(self, user_input: str) -> str:
        """ Format the user input. """
        # Create the system prompt
        prompt_beginning = """
<|start_header_id|>system<|end_header_id|>

You are an AI assistant that can help the user with a variety of tasks. You have access to the following functions:

        """
        system_prompt_end = """

When the user asks you a question, if you need to use functions, provide ONLY the function calls, and NOTHING ELSE, ONLY in the following format (DO NOT USE ANY OTHER FORMAT):

<|function_calls|>
    [
        { "name": "function_name_1", "params": { "param_1": "value_1", "param_2": "value_2" }, "output": "The output variable name, to be possibly used as input for another function},
        { "name": "function_name_2", "params": { "param_3": "value_3", "param_4": "output_1"}, "output": "The output variable name, to be possibly used as input for another function"},
        ...
    ]
<|end_function_calls|>

<|eot_id|><|start_header_id|>user<|end_header_id|>
        """
        prompt_end = """
DO NOT SAY ANTHING OTHER THAN THE FUNCTION CALLS. DO NOT PROVIDE ANY OTHER INFORMATION. ONLY PROVIDE THE FUNCTION CALLS IN THE FORMAT MENTIONED ABOVE. DO NOT USE A FUNCTION AS AN INPUT, USE IT IN ITS OWN FUNCTION CALL AND THEN USE ITS OUTPUT.
<|eot_id|><|start_header_id|>function_calls<|end_header_id|>
        """

        system_prompt = prompt_beginning + json.dumps(self.functions, indent=4) + system_prompt_end

        return system_prompt + user_input + prompt_end

    def format_output(self, output: any) -> str:
        """ Format the output. """
        prompt = """
Present the function responses below to the user, as an answer to their question. Act as if you're directly following up to their question, don't mention it. Start with stuff like, "Sure, here are the results:" or "Here's what I found:" or "Here's the anser to your question:" etc. 
<|function_responses|>
"""
        prompt += json.dumps(output, indent=4)
        prompt += """
<|end_function_responses|>
"""
        return prompt
    
    def generate(
            self, 
            user_input: str,
            first_message: bool = True
            ) -> dict:
        """
        Generate a response based on the user input.
        """
        if first_message:
            user_input = self.format_user_input(user_input)
        else:
            user_input = self.format_output(user_input)

        # Get the model response and extract the content
        model_response = ollama.chat(
            model=self.model_name,
            messages=[{'role': 'user', 'content': user_input}]
        )

        content = model_response["message"]["content"]

        return content

    
    def get_function_calls(
            self, 
            user_input: str,
            verbose: bool = False
        ) -> list[dict[str, str]]:
        """
        Get the function calls from the user input.
        """
        content = self.generate(user_input)

        # Extract the function calls 
        # They're in between <|function_calls|> and <|end_function_calls|> tags
        if "<|end_function_calls|>" in content: 
            # Remove <|end_function_calls|> from the end
            function_calls = content.split("<|end_function_calls|>")[0]
            if "<|function_calls|>" in function_calls:
                # Remove <|function_calls|> from the beginning
                function_calls = function_calls.split("<|function_calls|>")[1]

        elif "|end_function_calls|" in content:
            # Remove "|end_function_calls|" from the end
            function_calls = content.split("|end_function_calls|")[0]
        elif "|<end_function_calls>|" in content:
            # Remove "|<end_function_calls>|"
            function_calls = content.split("|<end_function_calls>|")[0]
        else :
            function_calls = content

        # Check if content starts and ends with a "|"
        if function_calls.startswith("|") and function_calls.endswith("|"):
            # Replace them with "[" and "]"
            function_calls = "[" + function_calls[1:-1] + "]"
        else:
            function_calls = function_calls

        # Check if function calls have doubled [[ and ]]
        if "[[" in function_calls and "]]" in function_calls:
            # Replace them with [ and ]
            function_calls = function_calls.replace("[[", "[").replace("]]", "]")

        #print(function_calls)
        # Read function calls as json
        try:
            function_calls_parsed: list[dict[str, str]] = json.loads(function_calls)
        except json.JSONDecodeError:
            function_calls_parsed = []
            print ("Model response not in desired JSON format")
        finally:
            if verbose:
                print("- Function calls:")
                print(function_calls_parsed)
                print("")

        return function_calls_parsed

