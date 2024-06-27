Usage
=====

Here's a simple example of using easy_fnc with the Ollama backend:

.. code-block:: python

   from easy_fnc.function_caller import FunctionCallingEngine, create_functions_metadata
   from easy_fnc.models import OllamaModel

   # Initialize the function calling engine
   fnc_engine = FunctionCallingEngine()
   fnc_engine.add_user_functions("path/to/your_functions.py")
   functions_metadata = create_functions_metadata(fnc_engine.functions)

   # Create an Ollama model
   model = OllamaModel("model_name", functions_metadata)

   # Generate a response
   user_input = "Get me a random city and its weather forecast"
   response_raw = model.generate(user_input)

   # Parse the response and execute functions
   parsed_response = fnc_engine.parse_model_response(response_raw)
   outputs = fnc_engine.call_functions(parsed_response.function_calls)

   print(outputs)

For more detailed usage instructions, please refer to the API documentation.