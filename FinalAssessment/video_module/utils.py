"""Implementation of utility functions for video recjgnition tasks."""

import os
import shutil
import random
from tqdm import tqdm


def split_and_copy(input_dir, output_dir, splits, seed=777):
    """
    Split the dataset into train, val, and test sets and copy files to the output direscoty.
    """
    random.seed(seed)

    for class_dir in tqdm(
        [d for d in input_dir.iterdir() if d.is_dir()], desc="Splitting"
    ):
        class_name = class_dir.name
        videos = list(class_dir.glob("*.avi"))
        random.shuffle(videos)

        n_train = int(len(videos) * splits["train"])
        n_val = int(len(videos) * splits["val"])

        split_map = {
            "train": videos[:n_train],
            "val": videos[n_train : n_train + n_val],
            "test": videos[n_train + n_val :],
        }

        for split_name, video_list in split_map.items():
            target_class_dir = output_dir / split_name / class_name
            target_class_dir.mkdir(parents=True, exist_ok=True)

            for video_path in video_list:
                dst_path = target_class_dir / video_path.name
                shutil.copy2(video_path, dst_path)

    print("Data splitting is done!")


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
