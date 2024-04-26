from easy_fnc.function_caller import FunctionCaller

def main():
    # Create a FunctionCaller object
    function_caller = FunctionCaller()

    # Create the functions metadata
    functions_metadata = function_caller.create_functions_metadata()
    print("Functions metadata:")
    print(functions_metadata)

if __name__ == "__main__":
    main()