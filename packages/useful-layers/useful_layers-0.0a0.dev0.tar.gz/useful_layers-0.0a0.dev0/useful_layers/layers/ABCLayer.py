from abc import ABC, abstractmethod

import torch


class Layer(ABC, torch.nn.Module):

    @abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Perform a forward pass"""
