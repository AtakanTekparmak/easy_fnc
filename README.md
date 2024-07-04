# easy_fnc

<p align="center">
    <a><img src="https://img.shields.io/badge/Version-0.2.1-green.svg" alt="Version"></a>
    <a><img src="https://img.shields.io/badge/Python-3.9.13-blue.svg" alt="Python"></a>
    <a href="https://groq.com/"><img src="https://img.shields.io/badge/Groq-red" alt="Groq"></a>
    <a href="https://ollama.com/"><img src="https://img.shields.io/badge/Ollama-white" alt="Ollama"></a>
<p>

The `easy_fnc` package provides a framework for generating responses using LLMs and executing user-defined functions. It allows users to define their own functions and integrate them with LLMs to create interactive and customizable applications. The package has optional dependencies for different LLM backends, such as Ollama and Groq, to provide flexibility in choosing the model that best suits the user's needs.

Beware that the package is still in development and may have breaking changes, as we have yet to release a stable version, `easy_fnc 1.0.0`.

# Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Explanation of Different Modules](#explanation-of-different-modules)
  - [Defining User Functions](#defining-user-functions)
  - [Core Utility Functions](#core-utility-functions)
  - [Models](#models)
    - [Ollama Model](#ollama-model)
    - [Groq Model](#groq-model)
  - [Templates](#templates)

## Installation

To install the `easy_fnc` package, run the following command:

```
pip install easy_fnc
```

## Usage

The full usage with Ollama is as follows (an example can also be found in `usage.py` in the root directory of the package):

```python
from easy_fnc.function_caller import FunctionCallingEngine, create_functions_metadata
from easy_fnc.models import OllamaModel

# Declare the constants
MODEL_NAME = "adrienbrault/nous-hermes2pro-llama3-8b:f16"
VERBOSE = True

# Create a FunctionCallingEngine object
fnc_engine = FunctionCallingEngine()
fnc_engine.add_user_functions("easy_fnc/functions.py")
functions_metadata = create_functions_metadata(fnc_engine.functions)

# Create the Ollama model 

model = OllamaModel(
    MODEL_NAME, 
    functions_metadata
)

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
```

Which would output, with the function call results displayed on the bottom of the output:



```
Thoughts:
The user wants to get a random city and its weather forecast. To do that, I will call the following functions:
1. get_random_city: This function retrieves a random city from a list.
2. get_weather_forecast: This function retrieves the weather forecast for a given location.

Function Calls:
- get_random_city:
  - kwargs: {}
  - returns: ['random_city']
- get_weather_forecast:
  - kwargs: {'location': 'random_city'}
  - returns: ['weather_forecast']

{'random_city': 'Rio de Janeiro', 'weather_forecast': {'location': 'Rio de Janeiro', 'forecast': 'rainy', 'temperature': '25°C'}}
```

## Explanation of Different Modules

### Defining User Functions

User-defined functions can be provided to the package as a `.py` file with the functions in it. A `FunctionCallingEngine` class is provided to facilitate the import and execution of user-defined functions, as well as the extraction of function calls from the model output.

Example:

```python
# Create a FunctionCallingEngine object
fnc_engine = FunctionCallingEngine()
fnc_engine.add_user_functions("path/to/functions.py")
functions_metadata = create_functions_metadata(fnc_engine.functions)
```

### Core Utility Functions

The package provides a set of core utility functions that can be used in conjunction with user-defined functions. These functions are defined in the `easy_fnc/core_utils.py` file and can be accessed using the `get_core_utils` function.

Example:

```python
from easy_fnc.core_utils import get_core_utils

core_utils = get_core_utils()
```

### Models

The package provides an abstract base class `EasyFNCModel` in the `model.py` file. This class defines the interface for implementing LLM interfaces that can generate responses based on user input and execute function calls.

To create a custom model, subclass `EasyFNCModel` and implement the following abstract method:

- `generate(self, user_input: str) -> str`: Generate a response based on the user input.

Example:

```python
from easy_fnc.models.model import EasyFNCModel

class CustomModel(EasyFNCModel):
    def generate(self, user_input: str) -> str:
        # Implement response generation logic
        pass
```

####  Ollama Model

The package includes an implementation of the `EasyFNCModel` using the Ollama model. The `OllamaModel` class is defined in the `easy_fnc/models/ollama.py` file.

To use the Ollama model:
1. Pull the model from Ollama using the `ollama pull` command. For example:
```bash
ollama pull adrienbrault/nous-hermes2pro-llama3-8b:f16
```
2. Then, the usage is as follows if you're using the `nous-hermes2pro-llama3-8b` model:

```python
from easy_fnc.models.ollama import OllamaModel
from easy_fnc.utils import load_template

# Create a FunctionCallingEngine object
fnc_engine = FunctionCallingEngine()
fnc_engine.add_user_functions("path/to/functions.py")
functions_metadata = create_functions_metadata(fnc_engine.functions)

# Create the Ollama model
MODEL_NAME = "adrienbrault/nous-hermes2pro-llama3-8b:f16"
ollama_model = OllamaModel(
    MODEL_NAME, 
    functions_metadata,
    template=load_template(file_type="toml")
)
```

#### Groq Model

The package also includes an implementation of the `EasyFNCModel` using the Groq model. The `GroqModel` class is defined in the `easy_fnc/models/groq.py` file.

To use the Groq model:
1. Add the environment variable `GROQ_API_KEY` with your Groq API key.
2. (Optional) Add the environment variable `GROQ_MODEL` with the model name you want to use. The default model is `llama-3-70b-8192`.
3. Then, the usage is as follows:

```python
from easy_fnc.models import GroqModel

# Create a FunctionCallingEngine object
fnc_engine = FunctionCallingEngine()
fnc_engine.add_user_functions("path/to/functions.py")

# Two ways to create the functions metadata
# 1. Pass the functions directly
#functions_metadata = create_functions_metadata(functions=fnc_engine.functions)

# 2. Pass the file path that contains the python functions
functions_metadata = create_functions_metadata(file_path="path/to/functions.py")

# Create the Groq model
model = GroqModel(functions_metadata)
```
## Templates

The `easy_fnc` package uses JSON and TOML templates to format user input and model responses. The `OllamaModel` class accepts both a string and a dictionary as parameters for the template. The default template is defined in the `easy_fnc/models/templates/base.toml` file.

To use a custom template, you have two options:

1. Provide the template as a JSON file path using the `load_template` method:

```python
from easy_fnc.utils import load_template

template = load_template(file_path="path/to/template.json", file_type="json")
```

2. Provide the template as a TOML file path using the `load_template` method:

```python
from easy_fnc.utils import load_template

template = load_template(file_path="path/to/template.toml", file_type="toml")
```

Users have the flexibility to use either the default template or provide their own custom template to format the user input and model responses.

## Contributing

Contributions to the `easy_fnc` package are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the package's GitHub repository.

## License

The `easy_fnc` package is open-source and released under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

---

This documentation provides an overview of how to use the `easy_fnc` package based on the provided files. It covers the key components, including user-defined functions, core utility functions, models, configuration, and templates. Users can refer to this documentation to understand how to integrate their own functions, create custom models, and utilize the package effectively in their applications.
