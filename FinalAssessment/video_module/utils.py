"""Implementation of utility functions for video recjgnition tasks."""

import os


def save_obj_names(data_dir, output_file="obj.names"):
    """
    Saves the names of object classes found in the specified directory to a file.
    """
    class_names = sorted(
        [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    )

    with open(output_file, "w", encoding="utf-8") as f:
        for name in class_names:
            f.write(name + "\n")


def get_obj_names(obj_names="obj.names"):
    """
    Retrieves the names of object classes from a specified file.
    """
    with open(obj_names, "r", encoding="utf-8") as f:
        class_names = [line.strip() for line in f.readlines()]
    return class_names
