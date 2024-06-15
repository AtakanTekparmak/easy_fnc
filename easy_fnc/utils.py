import json
import tomllib
import re

from easy_fnc.models.templates import get_template_path

# Define constants
TEMPLATE_FILE_TYPES = ["json", "toml"]

def load_template(
        file_path: str = get_template_path(),
        file_type: str = "toml"
    ) -> dict:
    """
    Load a template from a JSON file and return it as a dictionary.
    """
    if file_type not in TEMPLATE_FILE_TYPES:
        raise ValueError(f"Invalid file type. Expected one of {TEMPLATE_FILE_TYPES}")
    if file_type == "json":
        return load_json(file_path)
    elif file_type == "toml":
        return load_toml(file_path)
    

def load_json(file_path: str) -> dict:
    """
    Load a JSON file and return it as a dictionary.
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found")
    return data

def load_toml(file_path: str) -> dict:
    """
    Load a TOML file and return it as a dictionary.
    """
    try:
        with open(file_path, "rb") as file:
            data = tomllib.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found")
    except tomllib.TOMLDecodeError:
        raise tomllib.TOMLDecodeError(f"Error decoding TOML file {file_path}")
    return data

def extract_thoughts_and_function_calls(raw_response: str) -> tuple[str, str]:
    """
    Extract the thoughts and function calls from the raw model response.
    """
    pattern = r'<\|thoughts\|>(.*?)<\|end_thoughts\|>\s*<\|function_calls\|>(.*?)<\|end_function_calls\|>'
    match = re.search(pattern, raw_response, re.DOTALL)
    
    if match:
        thoughts = match.group(1).strip()
        function_calls = match.group(2).strip()
        return thoughts, function_calls
    else:
        return "", ""