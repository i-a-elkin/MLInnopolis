"""Implementation of the test script for video recognition models."""

import argparse
from video_module.tester import VideoTester


def get_args():
    """
    Returns the command line arguments for testing.
    """
    parser = argparse.ArgumentParser(description="Test a video recognition model.")
    parser.add_argument(
        "--test_dir",
        type=str,
        default="hmdb51_data/test/",
        help="Path to test data directory.",
    )
    parser.add_argument(
        "--model_type",
        type=str,
        default="swin3d_b",
        help="Type of model to use.",
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        default="swin3d_b.pth",
        help="Path to the model checkpoint.",
    )
    parser.add_argument(
        "--obj_names",
        type=str,
        default="obj.names",
        help="File containing object names.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=2,
        help="Batch size for testing.",
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
        "--img_size",
        type=int,
        default=224,
        help="Size of input images.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    TEST_DIR = args.test_dir
    MODEL_TYPE = args.model_type
    CHECKPOINT = args.checkpoint
    OBJ_NAMES = args.obj_names
    BATCH_SIZE = args.batch_size
    CLIP_LEN = args.clip_len
    STEP = args.step
    IMG_SIZE = args.img_size

    VideoTester(
        test_dir=TEST_DIR,
        model_type=MODEL_TYPE,
        checkpoint=CHECKPOINT,
        obj_names=OBJ_NAMES,
        batch_size=BATCH_SIZE,
        clip_len=CLIP_LEN,
        step=STEP,
        img_size=IMG_SIZE,
    ).test()
