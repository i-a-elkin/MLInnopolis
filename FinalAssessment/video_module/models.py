"""Functions to get the model and convert it to ONNX format."""

import torch
from torch import nn
from torchvision.models.video import swin3d_b  # type: ignore

import onnx
from onnxconverter_common import float16  # type: ignore # pylint: disable=import-error

from .utils import get_obj_names


def get_model(model_type="swin3d_b", obj_names="obj.names", checkpoint=None):
    """
    Returns a video recognition model based on the specified type.
    """
    num_classes = len(get_obj_names(obj_names))

    if model_type == "swin3d_b":
        model = swin3d_b(weights="KINETICS400_V1")
        model.head = nn.Linear(model.head.in_features, num_classes)

    if checkpoint:
        model.load_state_dict(torch.load(checkpoint))
    return model


def convert_to_onnx(
    model_type="swin3d_b", obj_names="obj.names", checkpoint="best_swin_model.pth"
):
    """
    Converts the specified model to ONNX format.
    """
    model = get_model(model_type=model_type, obj_names=obj_names, checkpoint=checkpoint)
    model.eval()

    dummy_input = torch.randn(1, 3, 32, 224, 224)
    torch.onnx.export(
        model,
        dummy_input,
        f"{checkpoint.replace('.pth', '').replace('.pt', '')}.onnx",
        input_names=["input"],
        output_names=["output"],
    )
    print("Model is converted to ONNX!")


def convert_onnx_fp16(checkpoint):
    """
    Converts an ONNX model to FP16 format.
    """
    model = onnx.load(f"{checkpoint.replace('.pth', '').replace('.pt', '')}.onnx")
    model_fp16 = float16.convert_float_to_float16(model)
    onnx.save(model_fp16, f"{checkpoint.replace('.pth', '').replace('.pt', '')}_fp16.onnx")
    print("Model ONNX is converted to fp16!")
