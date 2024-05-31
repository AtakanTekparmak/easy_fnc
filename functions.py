import random
import importlib
import ast

from easy_fnc.models.ollama import OllamaModel

def get_user_defined_functions(filename: str) -> dict[str, callable]:
    """Retrieves the user defined functions from a file"""
    # Parse the file
    with open(filename, 'r') as file:
        tree = ast.parse(file.read())

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

def get_tweets(
        hashtag: str,
        limit: int = 10
    ) -> list[str]:
    """Retrieves tweets for a given hashtag and an  optional limit on the number of tweets"""
    # Check if OLLAMA_MODEL is instantiated, if not, instantiate it
    
    MODEL_NAME = "llama3:8b-instruct-fp16"
    OLLAMA_MODEL = OllamaModel(
        model_name= MODEL_NAME,
        functions=[{"", ""}]
    )

    # Define lambda function to generate tweets from hastag using the OLLAMA model
    generate_tweets = lambda hashtag: OLLAMA_MODEL.generate(
        user_input=f"Generate {str(limit)} tweets about {hashtag}. Provide user name and tweet content. Separate each tweet with a line of ~ characters.",
        first_message=False,
        response_message=False
    )

    # Generate tweets
    tweets = generate_tweets(hashtag)

    # Split the tweets
    tweets = tweets.split("~")

    return tweets
