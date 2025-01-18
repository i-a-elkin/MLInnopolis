"""Lesson28 Task2: Dynamic Class Creation."""


def create_class_with_methods(class_name, attributes, methods):
    """
    Creates a dynamic class with the specified name,
    attributes, and methods.
    """
    class_dict = {**attributes, **methods}

    return type(class_name, (object,), class_dict)


if __name__ == "__main__":
    my_attributes = {"species": "Human", "age": 25}
    my_methods = {
        "greet": lambda self: f"Hello, I am a {self.species} and I am {self.age} years old."
    }
    DynamicClass = create_class_with_methods("DynamicClass", my_attributes, my_methods)
    instance = DynamicClass()

    print(instance.greet())
