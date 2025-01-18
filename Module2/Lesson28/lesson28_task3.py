"""Lesson28 Task3: Code Generation."""


def generate_complex_function(function_name, parameters, function_body):
    """
    The function dynamically generates Python code using `exec`.
    It creates a function with the specified name, list of parameters,
    and body within the local scope, then returns the created function.
    """
    # Form the function definition as a string
    function_code = f"def {function_name}({', '.join(parameters)}):\n"

    # Split the function body line by line to add proper indentation
    for line in function_body.split("\n"):
        if line.strip():
            function_code += f"    {line}\n"
        else:
            function_code += "\n"

    local_vars = {}
    # pylint: disable-next=exec-used
    exec(function_code, {}, local_vars)

    return local_vars[function_name]


if __name__ == "__main__":
    FUNCTION_NAME = "complex_function"
    PARAMETERS = ["x", "y"]
    FUNCTION_BODY = """
if x > y:
    return x - y
else:
    return y - x
"""
    complex_func = generate_complex_function(FUNCTION_NAME, PARAMETERS, FUNCTION_BODY)

    print(complex_func(10, 5))
    print(complex_func(5, 10))
