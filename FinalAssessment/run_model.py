"""Inference script for processing a video using an ONNX model for action recognition."""

import argparse

from video_module.inference import process_video_onnx


def get_args():
    """
    Returns the command line arguments for processing a video with an ONNX model.
    """
    parser = argparse.ArgumentParser(
        description="Process a video using an ONNX model for action recognition."
    )
    parser.add_argument(
        "--video_path",
        type=str,
        default="brushing_hair.avi",
        help="Path to the video file.",
    )
    parser.add_argument(
        "--onnx_model_path",
        type=str,
        default="swin3d_b.onnx",
        help="Path to the ONNX model file.",
    )
    parser.add_argument(
        "--obj_names",
        type=str,
        default="obj.names",
        help="File containing object names.",
    )
    parser.add_argument(
        "--clip_len",
        type=int,
        default=32,
        help="Length of video clips.",
    )
    parser.add_argument(
        "--skip_frames",
        type=int,
        default=2,
        help="Number of frames to skip before processing.",
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

    VIDEO_PATH = args.video_path
    ONNX_MODEL_PATH = args.onnx_model_path
    OBJ_NAMES = args.obj_names
    CLIP_LEN = args.clip_len
    SKIP_FRAMES = args.skip_frames
    IMG_SIZE = args.img_size

    process_video_onnx(
        VIDEO_PATH,
        ONNX_MODEL_PATH,
        obj_names=OBJ_NAMES,
        clip_len=CLIP_LEN,
        skip_frames=SKIP_FRAMES,
        img_size=IMG_SIZE,
    )
