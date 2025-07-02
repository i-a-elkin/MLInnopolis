"""Module for testing video recognition models."""

import json
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from .models import get_model
from .utils import get_obj_names
from .dataset import VideoDatasetSlidingWindow

# pylint: disable=consider-using-enumerate


class VideoTester:
    """
    Tester class for video recognitin tasks.
    """

    def __init__(
        self,
        test_dir,
        model_type="swin3d_b",
        checkpoint="swin3d_b.pth",
        obj_names="obj.names",
        batch_size=2,
        clip_len=32,
        step=16,
        img_size=224,
    ):
        self.checkpoint = checkpoint
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = get_model(
            model_type=model_type, obj_names=obj_names, checkpoint=checkpoint
        ).to(self.device)
        self.classes = get_obj_names(obj_names)

        self.test_dataset = VideoDatasetSlidingWindow(
            data_dir=test_dir,
            obj_names=obj_names,
            clip_len=clip_len,
            step=step,
            img_size=img_size,
        )
        self.test_loader = DataLoader(
            self.test_dataset, batch_size=batch_size, shuffle=False
        )

        self.results = {}

    def test(self):
        """
        Tests the model and savves the results.
        """
        self.model.eval()
        correct = 0
        total = 0

        class_correct = [0] * len(self.classes)
        class_total = [0] * len(self.classes)

        with torch.no_grad():
            for videos, labels in tqdm(self.test_loader, desc="Testing", leave=False):
                videos, labels = videos.to(self.device), labels.to(self.device)
                outputs = self.model(videos)

                _, preds = torch.max(outputs, 1)

                correct += (preds == labels).sum().item()
                total += labels.size(0)

                for i in range(len(labels)):
                    label = labels[i].item()
                    pred = preds[i].item()
                    class_total[label] += 1
                    if pred == label:
                        class_correct[label] += 1

        test_accuracy = correct / total
        self.results["average_accuracy"] = test_accuracy

        per_class_accuracy = {}
        for i in range(len(self.classes)):
            if class_total[i] > 0:
                acc = class_correct[i] / class_total[i]
            else:
                acc = 0
            per_class_accuracy[self.classes[i]] = acc
        self.results["per_class_accuracy"] = per_class_accuracy

        with open(
            f"{self.checkpoint.replace('.pth', '').replace('.pt', '')}_results.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(self.results, f, indent=4)
            print("Results are saved!")
        print(f"Average accuracy: {self.results['average_accuracy']:.4f}")
