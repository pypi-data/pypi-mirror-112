from abc import ABC

import torch
import torch.nn as nn
import torch.nn.functional as F

from useful_layers.layers.ABCLayer import Layer

__all__ = ['SpatialAttention2D', 'SpatialAttention3D']


class _SpatialAttention(Layer, ABC):

    def __init__(self):
        super(_SpatialAttention, self).__init__()
        self.spacial_conv = self.conv(in_channels=2,
                                      kernel_size=self.kernel_size,
                                      out_channels=1,
                                      stride=1,
                                      dilation=1,
                                      groups=1,
                                      bias=False,
                                      padding=(self.kernel_size - 1) // 2)
        if self.batch_norm:
            self.batch_norm = self.batch_norm(1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        avg_comp = torch.max(x, 1).values.unsqueeze(1)
        max_comp = torch.mean(x, 1).unsqueeze(1)
        conv_input = torch.cat((avg_comp, max_comp), dim=1)
        attention_map = self.spacial_conv(conv_input)
        if self.batch_norm:
            attention_map = self.batch_norm(attention_map)
        attention_map = F.sigmoid(attention_map)
        return attention_map


class SpatialAttention2D(_SpatialAttention):
    """Simple spatial attention layer

    Implementation based on: https://arxiv.org/abs/1807.06521v2
    """

    def __init__(self,
                 in_channels: int,
                 kernel_size: int = 7,
                 batch_norm: bool = True):
        """Create new SpatialAttention Layer

        Args:
            in_channels: Number of input channels
            kernel_size: Kernel size to use (integer or tuple of int)
            batch_norm: If true batch normalization is applied. Defaults to True.
        """
        self.in_channels = in_channels
        self.kernel_size = kernel_size
        if batch_norm:
            self.batch_norm = nn.BatchNorm2d
        self.conv = nn.Conv2d
        super(SpatialAttention2D, self).__init__()


class SpatialAttention3D(_SpatialAttention):
    """Simple spatial attention layer

    Implementation based on: https://arxiv.org/abs/1807.06521v2
    """

    def __init__(self,
                 in_channels: int,
                 kernel_size: int = 7,
                 batch_norm: bool = True):
        """Create a SpatialAttention3D layer

        Args:
            in_channels: Number of input channels
            kernel_size: Kernel size to use (integer or tuple of int)
            batch_norm: If true batch normalization is applied. Defaults to True.
        """
        self.in_channels = in_channels
        self.kernel_size = kernel_size
        if batch_norm:
            self.batch_norm = nn.BatchNorm3d
        self.conv = nn.Conv3d
        super(SpatialAttention3D, self).__init__()
