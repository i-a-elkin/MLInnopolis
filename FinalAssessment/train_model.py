"""Train a video recognition model with specified parameters."""

import argparse

from video_module.utils import save_obj_names
from video_module.trainer import train


def get_args():
    """
    Returns the command line arguments for training.
    """

    parser = argparse.ArgumentParser(description="Train a video recognition model.")
    parser.add_argument(
        "--train_dir",
        type=str,
        default="hmdb51_data/train/",
        help="Path to training data directory.",
    )
    parser.add_argument(
        "--val_dir",
        type=str,
        default="hmdb51_data/val/",
        help="Path to validation data directory.",
    )
    parser.add_argument(
        "--model_type",
        type=str,
        default="swin3d_b",
        help="Type of model to use.",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default="swin3d_b.pth",
        help="Path to save the trained model.",
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        default=None,
        help="Path to a checkpoint file.",
    )
    parser.add_argument(
        "--obj_names",
        type=str,
        default="obj.names",
        help="File containing object names.",
    )
    parser.add_argument(
        "--img_size",
        type=int,
        default=224,
        help="Size of input images.",
    )
    parser.add_argument(
        "--num_epochs",
        type=int,
        default=10,
        help="Number of training epochs.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=2,
        help="Batch size for training.",
    )
    parser.add_argument(
        "--clip_len",
        type=int,
        default=32,
        help="Length of video clips.",
    )
    parser.add_argument(
        "--step",
        type=int,
        default=16,
        help="Step size for sliding window.",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=1e-4,
        help="Learning rate for training.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    TRAIN_DIR = args.train_dir
    VAL_DIR = args.val_dir
    OBJ_NAMES = args.obj_names
    MODEL_TYPE = args.model_type
    CHECKPOINT = args.checkpoint
    SAVE_PATH = args.save_path
    IMG_SIZE = args.img_size
    NUM_EPOCHS = args.num_epochs
    BATCH_SIZE = args.batch_size
    CLIP_LEN = args.clip_len
    STEP = args.step
    LR = args.lr

    save_obj_names(
        TRAIN_DIR,
        output_file=OBJ_NAMES,
    )

    train(
        TRAIN_DIR,
        VAL_DIR,
        model_type=MODEL_TYPE,
        save_path=SAVE_PATH,
        checkpoint=CHECKPOINT,
        obj_names=OBJ_NAMES,
        img_size=IMG_SIZE,
        num_epochs=NUM_EPOCHS,
        batch_size=BATCH_SIZE,
        clip_len=CLIP_LEN,
        step=STEP,
        lr=LR,
    )
