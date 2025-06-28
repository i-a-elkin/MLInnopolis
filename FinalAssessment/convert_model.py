"""Converts a video recognition model to ONNX format."""

import argparse
from video_module.models import convert_to_onnx, convert_onnx_fp16


def get_args():
    """
    Returns the command line arguments for converting a model to ONNX format.
    """
    parser = argparse.ArgumentParser(
        description="Convert a video recognition model to ONNX format."
    )
    parser.add_argument(
        "--model_type",
        type=str,
        default="swin3d_b",
        help="Type of model to convert.",
    )
    parser.add_argument(
        "--obj_names",
        type=str,
        default="obj.names",
        help="File containing object names.",
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        default="swin3d_b.pth",
        help="Path to the model checkpoint.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    MODEL_TYPE = args.model_type
    OBJ_NAMES = args.obj_names
    CHECKPOINT = args.checkpoint

    convert_to_onnx(model_type=MODEL_TYPE, obj_names=OBJ_NAMES, checkpoint=CHECKPOINT)
    convert_onnx_fp16(CHECKPOINT)
