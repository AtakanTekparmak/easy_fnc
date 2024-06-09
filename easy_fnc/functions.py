import random
import importlib
import ast

def get_user_defined_functions(filename: str) -> dict[str, callable]:
    """Retrieves the user defined functions from a file"""
    # Parse the file
    try:
        with open(filename, 'r') as file:
            tree = ast.parse(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} not found")

    # Get the user defined functions
    functions: dict[str, callable] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Import function by name
            module = importlib.import_module(filename.split(".")[0].replace("/", "."))
            function = getattr(module, node.name)

            # Append the function to the list (exclude the get_user_defined_functions function)
            if node.name != "get_user_defined_functions":
                functions[node.name] = function

    return functions

# Example functions
def get_weather_forecast(location: str) -> dict[str, str]:
    """Retrieves the weather forecast for a given location"""
    forecasts = ["sunny", "cloudy", "rainy", "snowy", "windy"]
    return {
        "location": location,
        "forecast": random.choice(forecasts),
        "temperature": f"{random.randint(-10, 40)}°C"
    }

def get_random_city() -> str:
    """Retrieves a random city from a list of cities"""
    cities = ["Groningen", "Enschede", "Amsterdam", "Istanbul", "Baghdad", "Rio de Janeiro", "Tokyo", "Kampala"]
    return random.choice(cities)

def get_random_number(low: int, high: int) -> int:
    """Retrieves a random number between low and high"""
    return random.randint(low, high)
