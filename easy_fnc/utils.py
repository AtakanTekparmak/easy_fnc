import json

def load_template(file_path: str) -> dict:
    """
    Load a template from a JSON file and return it as a dictionary.
    """
    with open(file_path, "r") as file:
        template = json.load(file)
    return template