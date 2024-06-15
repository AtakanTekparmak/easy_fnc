from setuptools import setup, find_packages

def read_readme():
    """Read the README.md file and return its contents."""
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

def main():
    setup(
        name='easy_fnc',
        version='0.1.9',
        description='This package hopes to provide a modular and highly extendable interface to interact with LLMs via (multiple) function calling, easily.',
        long_description=read_readme(),
        long_description_content_type="text/markdown",
        author='Atakan Tekparmak',
        author_email='atakantekerparmak@gmail.com',
        url="https://github.com/AtakanTekparmak/easy_fnc",
        packages=find_packages(),
        install_requires=[
            "ollama",
            "pydantic"
        ],
    )

if __name__ == "__main__":
    main()