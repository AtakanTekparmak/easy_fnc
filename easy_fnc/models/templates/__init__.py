import os

def get_template_path():
    """
    Return the path of the base.toml file.
    """
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Return the path of the base.toml file
    return os.path.join(current_dir, "base.toml")