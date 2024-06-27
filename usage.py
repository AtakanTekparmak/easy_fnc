from easy_fnc.function_caller import FunctionCallingEngine, create_functions_metadata
from easy_fnc.models import OllamaModel, GroqModel

# Declare the constants
MODEL_NAME = "adrienbrault/nous-hermes2pro-llama3-8b:f16"
VERBOSE = False

# Create a FunctionCallingEngine object
fnc_engine = FunctionCallingEngine()
fnc_engine.add_user_functions("easy_fnc/functions.py")
functions_metadata = create_functions_metadata(fnc_engine.functions)


# Create the Ollama model 

model = OllamaModel(
    MODEL_NAME, 
    functions_metadata
)
"""

# Create the Groq model
model = GroqModel(functions_metadata)
"""

# Generate the response
user_input = "Can you get me a random city and the weather forecast for it?"
response_raw = model.generate(user_input)

# Print the raw response and system prompt if VERBOSE is True
if VERBOSE: 
    print(f"System prompt:\n {model.generate_system_prompt()}")
    print(f"Raw response:\n {response_raw}")

# Parse the example response
parsed_response = fnc_engine.parse_model_response(raw_response=response_raw)

# Print the parsed response
print(parsed_response)

# Call the functions
outputs = fnc_engine.call_functions(parsed_response.function_calls)

# Print the outputs
print(outputs)