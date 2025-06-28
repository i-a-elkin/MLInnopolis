"""Calculate label distribution for video datasets and save to a JSON file."""

import json
import argparse
from video_module.utils import save_obj_names
from video_module.dataset import get_label_distribution


def get_args():
    """
    Parse command line arguments for calculating label distribution.
    """
    parser = argparse.ArgumentParser(
        description="Calculate label distribution for video datasets."
    )
    parser.add_argument(
        "--data_dir",
        type=str,
        default="hmdb51_data/train",
        help="Path to the directory containing the dataset.",
    )
    parser.add_argument(
        "--save_to",
        type=str,
        default="label_distribution_train.json",
        help="File to save the label distribution data.",
    )
    parser.add_argument(
        "--obj_names",
        type=str,
        default="obj.names",
        help="File containing object names. If None, will generate from data_dir.",
    )
    parser.add_argument(
        "--clip_len",
        type=int,
        default=32,
        help="Length of video clips in frames.",
    )
    parser.add_argument(
        "--step",
        type=int,
        default=16,
        help="Step size for sampling frames.",
    )
    parser.add_argument(
        "--normalize",
        type=bool,
        default=True,
        help="Whether to normalize the label distribution.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    DATA_DIR = args.data_dir
    SAVE_TO = args.save_to
    OBJ_NAMES = args.obj_names
    CLIP_LEN = args.clip_len
    STEP = args.step
    NORMALIZE = args.normalize

    if OBJ_NAMES is None:
        OBJ_NAMES = "obj.names"
        save_obj_names(DATA_DIR, output_file=OBJ_NAMES)

    data = get_label_distribution(
        DATA_DIR,
        obj_names=OBJ_NAMES,
        clip_len=CLIP_LEN,
        step=STEP,
        normalize=NORMALIZE,
    )

    with open(SAVE_TO, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
