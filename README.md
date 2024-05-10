<h1 align="center">EasyFNC</h1>

This repository hopes to provide a modular and highly extendable interface to interact with LLMs via (multiple) function calling, easily. The main goal of this repository is to be able to `git pull` this repository, install Ollama & Ollama Python, add your functions to `easy_fnc/functions.py` and start using it with your LLMs asap. It only ships with [Ollama](https://github.com/ollama/ollama) support out of the box (so far).

The process is like so:

```
User Query-> Model -> Function Caller -> Model -> Response
```

The beauty here is the function calling format ***EasyFNC***, in which the functions are defined like this:
    
```json
[
    {
        "name": "function_name",
        "description": "function_description",
        "parameters": [
            {
                "name": "parameter_name",
                "type": "parameter_type"
            },
            ...
        ],
        "required": [ "required_parameter_name_1", ... ],
        "returns": [
            {
                "name": "output_name",
                "type": "output_type",
            },
            ...
        ]
    },
    ...
] 
```

And the model outputs them like so:

```json
[
    { "name": "function_name_1", "params": { "param_1": "value_1", "param_2": "value_2" }, "output": "output_1"},
    { "name": "function_name_2", "params": { "param_3": "value_3", "param_4": "output_1"}, "output": "output_2"},
    ...
]
```

This allows for both the model to call multiple functions by chaining them and the function caller (interpreter) to interpret the functions sequentially and do easy reference-resolution on the outputs when they're used as inputs by other functions.

## Requirements

* Python 3.10+
* [Ollama](https://ollama.com/download)

and well, that's it. 

## Installation

If the requirements are met, you can install the dependencies by running:

```bash
pip install -r requirements.txt
```
## Usage

####  **Disclaimer**
Right now there's only Ollama support, but this is a framework that is very reliable, getting consistent results even in quantized models used in Ollama. I can not emphasize how much **YOU SHOULD NOT PROVIDE THE MODEL WITH DELETE FUNCTIONS IN THE CURRENT STAGE**, as there's no input sanitizing at all and the code is very much in alpha stage. Choose your functions with discretion and check your function calls.

To use the framework, out of the box, first, pull the `nous-hermes2pro-llama3-8` model from ollama:

```bash
ollama pull adrienbrault/nous-hermes2pro-llama3-8b:f16
```
Then simply `cd` into the directory and run the main script:
```bash
cd EasyFNC
python main.py
```

You can look at `easy_fnc/models/ollama.py` and `easy_fnc/models/templates` to see how to set up your own Ollama model. Add your functions to `easy_fnc/functions.py` and you're good to go.

## Example

**Example User Query:**

```bash
"Can you get me a random city and the weather forecast for it?"
```

## Example Model Reply:

```
- Model Thoughts:

The user wants a random city and its weather forecast. To achieve this, I will first call "get_random_city" to retrieve a random city, and then use that city as an input parameter for the "get_weather_forecast" function.
1. get_random_city: Retrieve a random city
2. get_weather_forecast: Use the randomly selected city to get its weather forecast

- Function calls:
[{'name': 'get_random_city', 'output': '$random_city$'}, {'name': 'get_weather_forecast', 'params': {'location': '$random_city$'}, 'output': '$weather_forecast$'}]

- Model reply: 
Sure, here are the results: The random city I've selected for you is Enschede. The weather forecast for this city is showing snow, and the temperature is currently 0°C. Please let me know if there"s anything else I can help with!
```

## TO-DO

- [&#x2713;] Clean up the model code (especially the extraction)
- [&#x2713;] Add better templating (added JSON)
- [ ] Make the "map_func_to_list" work (recognize functions from the function call)
- [&#x2713;] Refine the prompt
- [ ] Clean up the repo structure and maybe move some stuff to easy_fnc.core?