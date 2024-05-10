from easy_fnc.function_caller import FunctionCaller
from easy_fnc.models.ollama import OllamaModel

def main():
    # Set constants
    MODEL_NAME = "adrienbrault/nous-hermes2pro-llama3-8b:f16" # using llama3 model for testing
    VERBOSE = False
    SHOW_FUNCTION_CALLS = True

    # Create a FunctionCaller object
    function_caller = FunctionCaller()

    # Create the functions metadata
    functions_metadata = function_caller.create_functions_metadata()

    # Create the Ollama model 
    ollama_model = OllamaModel(MODEL_NAME, functions_metadata)

    # Get the function calls from the user input
    user_input = "Can you get me a random city and the weather forecast for it?"
    print(f"-User Input: \n{user_input}\n")
    function_calls = ollama_model.get_function_calls(user_input, verbose=SHOW_FUNCTION_CALLS)

    # Call the functions
    output = ""
    for function in function_calls:
        output = function_caller.call_function(function)
        if VERBOSE:
            print(f"Function Output: {function_caller.call_function(function)}")

    # Call the model with the output
    response = ollama_model.generate(output, first_message=False, response_message=True, original_prompt=user_input) if output else "Function output is empty"

    # Print the response
    print(f"- Model reply: \n{response}")




if __name__ == "__main__":
    main()