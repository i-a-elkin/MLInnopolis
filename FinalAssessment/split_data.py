"""
Implementation of the script to split the dataset into train, val, and test sets.
"""

import argparse
import shutil
import random
from pathlib import Path
from tqdm import tqdm


def get_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Split dataset into train, val, and test sets"
    )

    parser.add_argument(
        "--input_dir",
        type=str,
        default="C:/Users/ivana/MLInnopolis/FinalAssessment/hmdb51_org",
        help="Path to the input directory containing class subdirectories with videos",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        default="C:/Users/ivana/MLInnopolis/FinalAssessment/hmdb51_data",
        help="Path to the output directory where the split datasets will be saved",
    )

    return parser.parse_args()


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


if __name__ == "__main__":
    args = get_args()

    INPUT_DIR = Path(args.input_dir)
    OUTPUT_DIR = Path(args.output_dir)

    split_and_copy(
        INPUT_DIR, OUTPUT_DIR, splits={"train": 0.7, "val": 0.2, "test": 0.1}
    )
