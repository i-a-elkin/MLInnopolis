"""Implementation of a video dataset with sliding window sampling."""

import os
from glob import glob
import cv2
import torch
from torch.utils.data import Dataset
import albumentations as A  # type: ignore
from albumentations.pytorch import ToTensorV2  # type: ignore
import numpy as np
from tqdm import tqdm

from .utils import get_obj_names

# pylint: disable=no-member


class VideoDatasetSlidingWindow(Dataset):
    """
    Dataset class for video recognition tasks with sliding window sampling.
    """

    def __init__(
        self,
        data_dir,
        obj_names="obj.names",
        clip_len=32,
        step=16,
        img_size=224,
    ):
        self.clip_len = clip_len
        self.step = step
        self.img_size = img_size
        self.video_paths, self.labels, self.class_to_idx = (
            self.get_video_paths_and_labels(data_dir, obj_names)
        )
        self.samples = []  # [(video_path, clip_indices, label)]

        self.transforms = A.ReplayCompose(
            [
                A.RandomResizedCrop(
                    size=(self.img_size, self.img_size), scale=(0.8, 1.0), p=1
                ),
                A.Rotate(limit=10, p=0.5),
                A.HorizontalFlip(p=0.5),
                A.ColorJitter(
                    brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1, p=0.5
                ),
                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
                ToTensorV2(),
            ]
        )

        for video_path, label in tqdm(
            zip(self.video_paths, self.labels), desc="Dataset Initialisation"
        ):
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            clip_indices_list = self.sample_clip_indices_sliding_window(
                total_frames, clip_len, step
            )
            for clip_indices in clip_indices_list:
                self.samples.append((video_path, clip_indices, label))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        video_path, frame_indices, label = self.samples[idx]
        frames = []

        cap = cv2.VideoCapture(video_path)
        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()

            if not ret:
                if frames:
                    frames.append(frames[-1])
                    continue
                else:
                    frame = np.zeros((self.img_size, self.img_size, 3), dtype=np.uint8)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
        cap.release()

        # Apply the same augmentation to all frames in clip
        first_aug = self.transforms(image=frames[0])
        replay = first_aug["replay"]
        aug_frames = [first_aug["image"]]

        for frame in frames[1:]:
            aug = A.ReplayCompose.replay(replay, image=frame)
            aug_frames.append(aug["image"])

        clip_tensor = torch.stack(aug_frames, dim=1)  # Shape: (C, T, H, W)
        return clip_tensor, label

    @staticmethod
    def get_video_paths_and_labels(data_dir, obj_names):
        """
        Retrieves video paths and labels from the dataset directory.
        """
        class_names = get_obj_names(obj_names)
        class_to_idx = {cls_name: idx for idx, cls_name in enumerate(class_names)}

        video_paths = []
        labels = []

        for cls_name in class_names:
            cls_dir = os.path.join(data_dir, cls_name)
            for path in glob(os.path.join(cls_dir, "*.avi")):
                video_paths.append(path)
                labels.append(class_to_idx[cls_name])

        return video_paths, labels, class_to_idx

    @staticmethod
    def sample_clip_indices_sliding_window(total_frames, clip_len, step):
        """
        Samples clip indices using a sliding window approach.
        """
        indices = []

        if total_frames <= clip_len:
            last_idx = max(0, total_frames - 1)
            padded = list(range(total_frames)) + [last_idx] * (clip_len - total_frames)
            return [padded]

        for start in range(0, total_frames - clip_len + 1, step):
            indices.append(list(range(start, start + clip_len)))

        last_start = total_frames - clip_len
        if not indices or indices[-1][0] < last_start:
            indices.append(list(range(last_start, last_start + clip_len)))
        return indices


def get_label_distribution(
    data_dir, obj_names="obj.names", clip_len=32, step=16, normalize=True
):
    """
    Computes the distribution of labels in the dataset.
    """
    dataset = VideoDatasetSlidingWindow(
        data_dir=data_dir, obj_names=obj_names, clip_len=clip_len, step=step
    )
    obj_names = get_obj_names(obj_names=obj_names)

    data = {name: 0 for name in obj_names}
    total = 0
    for item in dataset.samples:
        label = item[-1]
        data[obj_names[label]] += 1
        total += 1

    if normalize:
        return {key: round(value / total, 3) if total > 0 else 0 for key, value in data.items()}
    return data
