from abc import ABC, abstractmethod

import torch

__all__ = ['Block']


class Block(ABC, torch.nn.Module):

    @abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Perform a forward pass"""
