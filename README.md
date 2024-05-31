# easy_fnc

The `easy_fnc` package provides a framework for generating responses using AI models and executing user-defined functions. It allows users to define their own functions and integrate them with AI models to create interactive and customizable applications.

## Installation

To install the `easy_fnc` package, run the following command:

```
pip install easy_fnc
```

## Usage

### Defining User Functions

User-defined functions can be provided to the package in two ways:

1. **Function File**: Create a Python file (e.g., `functions.py`) and define your functions there. The package will automatically import the functions from the specified file.

2. **List of Functions**: Pass a list of function objects directly to the `get_user_defined_functions` function.

Example:

```python
from easy_fnc.functions import get_user_defined_functions

# Using a function file
user_functions = get_user_defined_functions("path/to/functions.py")

# Using a list of functions
def func1():
    pass

def func2():
    pass

user_functions = get_user_defined_functions([func1, func2])
```

### Core Utility Functions

The package provides a set of core utility functions that can be used in conjunction with user-defined functions. These functions are defined in the `core_utils.py` file and can be accessed using the `get_core_utils` function.

Example:

```python
from easy_fnc.core_utils import get_core_utils

core_utils = get_core_utils()
```

### Models

The package provides an abstract base class `EasyFNCModel` in the `model.py` file. This class defines the interface for implementing AI models that can generate responses based on user input and execute function calls.

To create a custom model, subclass `EasyFNCModel` and implement the required methods:

- `generate(self, user_input: str) -> dict`: Generate a response based on the user input.
- `get_function_calls(self, user_input: str, verbose: bool = False) -> list[dict]`: Extract function calls from the model output.

Example:

```python
from easy_fnc.models.model import EasyFNCModel

class CustomModel(EasyFNCModel):
    def generate(self, user_input: str) -> dict:
        # Implement response generation logic
        pass

    def get_function_calls(self, user_input: str, verbose: bool = False) -> list[dict]:
        # Implement function call extraction logic
        pass
```

### Ollama Model

The package includes an implementation of the `EasyFNCModel` using the Ollama model. The `OllamaModel` class is defined in the `ollama.py` file.

To use the Ollama model:
1. Pull the model from Ollama using the `ollama pull` command. For example:
```bash
ollama pull adrienbrault/nous-hermes2pro-llama3-8b:f16
```
2. Then, the usage is as follows if you're using the `nous-hermes2pro-llama3-8b` model:

```python
from easy_fnc.models.ollama import OllamaModel

model = OllamaModel(model_name="model_name", functions=[...])
response = model.generate(user_input="user input")
function_calls = model.get_function_calls(user_input="user input", verbose=True)
```

## Templates

The `easy_fnc` package uses JSON templates to format user input and model responses. The `OllamaModel` class accepts both a string and a dictionary as parameters for the template.

To use a custom template, you have two options:

1. Provide the name of a JSON template file located in the `easy_fnc/models/templates/` directory. The `OllamaModel` will automatically load the template using the `load_template` method.

```python
model = OllamaModel(model_name="model_name", functions=[...], template="custom_template")
```

2. Provide a dictionary containing the template structure directly.

```python
custom_template = {
    "function_call_prompt": {
        "beginning": "...",
        "system_prompt_end": "...",
        "prompt_end": "..."
    },
    "function_response_prompt": {
        "beginning": "...",
        "middle": "...",
        "end": "..."
    }
}

model = OllamaModel(model_name="model_name", functions=[...], template=custom_template)
```

The `load_template` method in `utils.py` can be used to load a template from a JSON file and convert it to a dictionary format that can be passed to the `OllamaModel`.

```python
from easy_fnc.utils import load_template

template_dict = load_template("path/to/custom_template.json")
model = OllamaModel(model_name="model_name", functions=[...], template=template_dict)
```

Users have the flexibility to use either a predefined template from the `easy_fnc/models/templates/` directory or create their own custom template and provide it as a dictionary or load it from a JSON file using the `load_template` method.

## Contributing

Contributions to the `easy_fnc` package are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the package's GitHub repository.

## License

The `easy_fnc` package is open-source and released under the [MIT License](https://opensource.org/licenses/MIT).

---

This documentation provides an overview of how to use the `easy_fnc` package based on the provided files. It covers the key components, including user-defined functions, core utility functions, models, configuration, and templates. Users can refer to this documentation to understand how to integrate their own functions, create custom models, and utilize the package effectively in their applications.