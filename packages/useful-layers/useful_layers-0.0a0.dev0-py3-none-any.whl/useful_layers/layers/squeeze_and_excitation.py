import torch
from torch.nn import functional as F

from useful_layers.utils import reduction_network
from useful_layers.layers.ABCLayer import Layer

__all__ = ['SqueezeAndExcitation2D', 'SqueezeAndExcitation3D']


class _SqueezeAndExcitation(Layer):
    def __init__(self):
        super(_SqueezeAndExcitation, self).__init__()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        size = x.size()
        if isinstance(self, SqueezeAndExcitation2D):
            view = (size[0], size[1], 1, 1)
        elif isinstance(self, SqueezeAndExcitation3D):
            view = (size[0], size[1], 1, 1, 1)
        else:
            raise NotImplementedError(f'Expected to be SqueezeAndExcitation2D or -3D, got {self}')
        out = torch.mean(x.view(size[0], size[1], -1), dim=-1).view(*view)
        out = F.relu(self.conv1(out))
        out = self.conv2(out)
        return torch.sigmoid(out)


class SqueezeAndExcitation2D(_SqueezeAndExcitation):
    """SqueezeAndExcitation2D

        Simple squeeze and excitation layer.

        Inspired by https://github.com/iantsen/hecktor/blob/main/src/layers.py
    """

    def __init__(self,
                 in_channels: int,
                 reduction: int = 2) -> None:
        """Create SqueezeAndExcitation2D Layer

        Args:
            in_channels (int): Number of input channels
            reduction (int, optional): Degree of reduction. Defaults to 2.
        """
        super(SqueezeAndExcitation2D, self).__init__()
        self.conv1, self.conv2 = reduction_network(in_channels, reduction, "2d")


class SqueezeAndExcitation3D(_SqueezeAndExcitation):
    """SqueezeAndExcitation3D

        Simple squeeze and excitation layer.

        Inspired by https://github.com/iantsen/hecktor/blob/main/src/layers.py
    """

    def __init__(self,
                 in_channels: int,
                 reduction: int = 2) -> None:
        """Create SqueezeAndExcitation3D Layer

        Args:
            in_channels (int): Number of input channels
            reduction (int, optional): Degree of reduction. Defaults to 2.
        """
        super(SqueezeAndExcitation3D, self).__init__()
        self.conv1, self.conv2 = reduction_network(in_channels, reduction, "3d")
