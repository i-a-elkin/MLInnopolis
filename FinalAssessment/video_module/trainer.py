"""Trainer module for video recognition tasks."""

import json
import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.optim import Adam
from tqdm import tqdm

from .dataset import VideoDatasetSlidingWindow
from .models import get_model


class VideoTrainer:
    """
    Trainer class for video recognition tasks.
    """

    def __init__(
        self,
        model,
        train_loader,
        val_loader,
        criterion,
        optimizer,
        scheduler=None,
        num_epochs=20,
        device="cuda",
        save_path="best_model.pth",
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.num_epochs = num_epochs
        self.device = device
        self.save_path = save_path
        self.best_acc = 0.0

        self.history = {
            "train_loss": [],
            "val_loss": [],
            "train_accuracy": [],
            "val_accuracy": [],
        }

    def train(self):
        """
        Main training loop for the video recognition model.
        """
        for epoch in range(1, self.num_epochs + 1):
            print(f"\nEpoch {epoch}/{self.num_epochs}")
            self._train_one_epoch()
            val_acc = self._validate()
            if self.scheduler:
                self.scheduler.step()

            if val_acc > self.best_acc:
                print(
                    f"New best model is found! Accuracy: {val_acc:.4f} (was {self.best_acc:.4f})"
                )
                self.best_acc = val_acc
                torch.save(self.model.state_dict(), self.save_path)

            with open(
                f"{self.save_path.replace('.pth', '').replace('.pt', '')}_logs.json",
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(self.history, f, indent=4)
                print("Logs are saved!")

    def _train_one_epoch(self):
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        loop = tqdm(self.train_loader, desc="Training", leave=False)

        for videos, labels in loop:
            videos, labels = videos.to(self.device), labels.to(self.device)
            self.optimizer.zero_grad()
            outputs = self.model(videos)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()

            running_loss += loss.item() * videos.size(0)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
            loop.set_postfix(loss=loss.item())

        epoch_loss = running_loss / total
        accuracy = correct / total

        self.history["train_loss"].append(epoch_loss)
        self.history["train_accuracy"].append(accuracy)
        print(f"Train Loss: {epoch_loss:.4f}, Train Accuracy: {accuracy:.4f}")

    def _validate(self):
        self.model.eval()
        correct = 0
        total = 0
        running_loss = 0.0

        with torch.no_grad():
            for videos, labels in tqdm(self.val_loader, desc="Validating", leave=False):
                videos, labels = videos.to(self.device), labels.to(self.device)
                outputs = self.model(videos)
                loss = self.criterion(outputs, labels)

                running_loss += loss.item() * videos.size(0)
                _, preds = torch.max(outputs, 1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)

        val_loss = running_loss / total
        val_accuracy = correct / total

        self.history["val_loss"].append(val_loss)
        self.history["val_accuracy"].append(val_accuracy)
        print(
            f"Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_accuracy:.4f}"
        )
        return val_accuracy


def train(
    train_dir,
    val_dir,
    model_type="swin3d_b",
    save_path="swin3d_b.pth",
    checkpoint=None,
    obj_names="obj.names",
    img_size=224,
    num_epochs=20,
    batch_size=32,
    clip_len=32,
    step=2,
    lr=1e-4,
    scheduler=None,
):
    """
    Main function to train the video recognition model.
    """
    train_dataset = VideoDatasetSlidingWindow(
        data_dir=train_dir,
        obj_names=obj_names,
        clip_len=clip_len,
        step=step,
        img_size=img_size,
    )
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    val_dataset = VideoDatasetSlidingWindow(
        data_dir=val_dir,
        obj_names=obj_names,
        clip_len=clip_len,
        step=step,
        img_size=img_size,
    )
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    model = get_model(model_type=model_type, obj_names=obj_names, checkpoint=checkpoint)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    trainer = VideoTrainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=nn.CrossEntropyLoss(),
        optimizer=Adam(model.parameters(), lr=lr),
        scheduler=scheduler,
        num_epochs=num_epochs,
        device=device,
        save_path=save_path,
    )

    trainer.train()
