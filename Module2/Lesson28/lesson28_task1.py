"""Lesson28 Task1: Using Metaclasses."""


class AttrLoggingMeta(type):
    """
    A metaclass that logs access to class attributes and methods.
    """

    def __new__(mcs, name, bases, class_dict):
        def wrap_method(name, method):
            def wrapped(self, *args, **kwargs):
                mcs.log_access(name, args)
                return method(self, *args, **kwargs)

            return wrapped

        def wrap_attribute(name, value):
            # Use property to log reads and writes
            private_name = f"_{name}"

            def getter(self):
                mcs.log_read(name, value, self)
                return getattr(self, private_name, value)

            def setter(self, new_value):
                mcs.log_write(name, new_value, self)
                setattr(self, private_name, new_value)

            return property(getter, setter)

        # Process all class attributes
        for attr_name, attr_value in class_dict.items():
            if callable(attr_value):
                class_dict[attr_name] = wrap_method(attr_name, attr_value)
            elif not (attr_name.startswith("__") and attr_name.endswith("__")):
                class_dict[attr_name] = wrap_attribute(attr_name, attr_value)

        return super().__new__(mcs, name, bases, class_dict)

    @staticmethod
    def log_access(name, value):
        """
        General logging method for access.
        """
        print(f"Calling method {name}")

    @staticmethod
    def log_read(name, value, instance):
        """
        Logs attribute read access.
        """
        print(f"Reading attribute {name}")

    @staticmethod
    def log_write(name, value, instance):
        """
        Logs attribute write access.
        """
        print(f"Writing attribute {name} with value {value}")


class LoggedClass(metaclass=AttrLoggingMeta):
    """
    A class that uses a metaclass for logging.
    """

    custom_method = 42

    def other_custom_method(self, x=None):
        """
        A method does something.
        """
        return f"Hello {x}!"


if __name__ == "__main__":
    instance = LoggedClass()
    print(instance.custom_method)
    instance.custom_method = 78
    instance.other_custom_method("John")
