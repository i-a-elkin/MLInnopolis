"""Real-time action recognition using ONNX Runtime and Gradio."""

from collections import deque
import argparse
import onnxruntime as ort  # type: ignore
import cv2
import numpy as np
import gradio as gr

ort.preload_dlls()
# pylint: disable=no-member


def get_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Action Recognition with ONNX Runtime and Gradio"
    )
    parser.add_argument(
        "--onnx_model_path",
        type=str,
        default="swin3d_b_fp16.onnx",
        help="Path to the ONNX model file.",
    )
    parser.add_argument(
        "--obj_names_path",
        type=str,
        default="obj.names",
        help="File containing object names.",
    )
    return parser.parse_args()


def get_obj_names(file_path):
    """
    Load object names from a file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]


def preprocess(clip):
    """
    Preprocesses a video clip for model input.
    """
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    clip = clip.astype(np.float16) / 255.0
    clip = (clip - mean) / std
    clip = np.transpose(clip, (3, 0, 1, 2))  # (C, T, H, W)
    return np.expand_dims(clip, axis=0).astype(np.float16)


def infer_realtime(video_file, skip_frames):
    """
    Perform real-time inference on a video file using an ONNX model.
    """
    args = get_args()

    session = ort.InferenceSession(
        args.onnx_model_path,
        providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
    )
    input_name = session.get_inputs()[0].name

    clip_len = 32
    labels = get_obj_names(args.obj_names_path)

    cap = cv2.VideoCapture(video_file.name)
    frame_buffer = deque(maxlen=clip_len)
    frame_count = 0
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if skip_frames > 0 and frame_count < skip_frames:
            frame_count += 1
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized_frame = cv2.resize(rgb_frame, (frame_width, frame_height))
        frame_buffer.append(resized_frame)

        if len(frame_buffer) == clip_len:
            clip = np.stack(frame_buffer, axis=0)
            resized_clip = np.array([cv2.resize(f, (224, 224)) for f in clip])
            input_tensor = preprocess(resized_clip)
            outputs = session.run(None, {input_name: input_tensor})
            pred_class = int(np.argmax(outputs[0]))
            label_text = f"{labels[pred_class]}"
        else:
            label_text = "buffer accumumulation..."

        annotated_frame = frame.copy()
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        frame_count = 0
        yield annotated_frame, label_text
    cap.release()


if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("## Демонстрация работы модели распознавания действий")

        with gr.Row():
            video_input = gr.File(
                label="Загрузите видеофайл (.mp4, .avi)", file_types=[".mp4", ".avi"]
            )
            skip_slider = gr.Slider(
                minimum=0, maximum=5, step=1, value=2, label="Пропуск кадров"
            )

        image_stream = gr.Image(label="Видео", type="numpy", streaming=True)
        label_output = gr.Textbox(label="Распознанное действие", interactive=False)
        status_text = gr.Markdown("")
        start_btn = gr.Button("Старт")

        start_btn.click(
            fn=lambda: ("", ""),
            inputs=None,
            outputs=[label_output, status_text],
            queue=False,
        )
        start_btn.click(
            fn=infer_realtime,
            inputs=[video_input, skip_slider],
            outputs=[image_stream, label_output],
        ).then(fn=lambda: "✅ Обработка завершена", inputs=None, outputs=status_text)
    demo.launch()
