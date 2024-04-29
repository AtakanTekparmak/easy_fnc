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
Right now there's only Ollama support and the model code is all over the place, but this is a framework that is very reliable, getting consistent results even in quantized models used in Ollama. I can not emphasize how much **YOU SHOULD NOT PROVIDE THE MODEL WITH DELETE FUNCTIONS IN THE CURRENT STAGE**, as there's no input sanitizing at all and the code is very much in alpha stage. Choose your functions with discretion and check your function calls.

To use the framework, simply add your functions to `easy_fnc/functions.py`, configure your model in main.py and then:

```bash
python main.py
```

## TO-DO

- [ ] Clean up the model code (especially the extraction)
- [ ] Add better templating (either YAML, JSON or Jinja)
- [ ] Refine the prompt
- [ ] Clean up the repo structure and maybe move some stuff to easy_fnc.core?