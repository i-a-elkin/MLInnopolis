"""Implementation of functions to process video and perform inference."""

import os
from collections import deque
import onnxruntime as ort  # type: ignore
import cv2
import numpy as np

from .utils import get_obj_names

# pylint: disable=no-member


def preprocess(clip):
    """
    Preprocesses a video clip for model input.
    """
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    clip = clip.astype(np.float32) / 255.0
    clip = (clip - mean) / std
    clip = np.transpose(clip, (3, 0, 1, 2))  # (C, T, H, W)
    clip = np.expand_dims(clip, axis=0)  # (1, C, T, H, W)
    return clip.astype(np.float32)


def process_video_onnx(
    video_path,
    onnx_model_path,
    obj_names="obj.names",
    clip_len=32,
    skip_frames=0,
    img_size=224,
):
    """
    Processes a video using an ONNX model for action recognition.
    """
    ort.preload_dlls()
    session = ort.InferenceSession(
        onnx_model_path, providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
    )
    input_name = session.get_inputs()[0].name

    cap = cv2.VideoCapture(video_path)
    frame_buffer = deque(maxlen=clip_len)

    print(f"--- Processing: {os.path.basename(video_path)} ---")
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video stream or error reading frame.")
            break

        if skip_frames > 0 and frame_count < skip_frames:
            frame_count += 1
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame = cv2.resize(rgb_frame, (img_size, img_size))
        frame_buffer.append(rgb_frame)

        if len(frame_buffer) == clip_len:
            clip = np.stack(frame_buffer, axis=0)  # (T, H, W, C)
            input_tensor = preprocess(clip)  # (1, C, T, H, W)

            outputs = session.run(None, {input_name: input_tensor})
            pred_class = int(np.argmax(outputs[0]))

            label_text = f"Action: {get_obj_names(obj_names)[pred_class]}"
            cv2.putText(
                frame,
                label_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                frame.shape[0] / 240 * 0.6,
                (0, 0, 255),
                2,
            )
            cv2.imshow(f"{os.path.basename(video_path)}", frame)

        frame_count = 0
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
