from easy_fnc.function_caller import FunctionCaller
from easy_fnc.models.ollama import OllamaModel

def main():
    # Set constants
    MODEL_NAME = "llama3" # using llama3 model for testing
    VERBOSE = False

    # Create a FunctionCaller object
    function_caller = FunctionCaller()

    # Create the functions metadata
    functions_metadata = function_caller.create_functions_metadata()

    # Create the Ollama model 
    ollama_model = OllamaModel(MODEL_NAME, functions_metadata)

    # Get the function calls from the user input
    user_input = "Can you get me the weather forecast of a random city?"
    print(f"-User Input: \n{user_input}\n")
    function_calls = ollama_model.get_function_calls(user_input, verbose=True)

    # Call the functions
    output = ""
    for function in function_calls:
        output = function_caller.call_function(function)
        if VERBOSE:
            print(f"Function Output: {function_caller.call_function(function)}")

    # Call the model with the output
    response = ollama_model.generate(output, first_message=False)

    # Print the response
    print(f"-Model reply: \n{response}")




if __name__ == "__main__":
    main()