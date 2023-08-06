import torch
from torch.nn import functional as F

from useful_layers.utils import reduction_network
from useful_layers.layers.ABCLayer import Layer

__all__ = ['ChannelAttention2D', 'ChannelAttention3D']


class _ChannelAttention(Layer):
    def __init__(self):
        super(_ChannelAttention, self).__init__()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        size = x.size()
        if isinstance(self, ChannelAttention2D):
            view = (size[0], size[1], 1, 1)
        elif isinstance(self, ChannelAttention3D):
            view = (size[0], size[1], 1, 1, 1)
        else:
            raise NotImplementedError(f'Expected to be ChannelAttention2D or -3D, got {self}')
        avg_comp = torch.mean(x.view(size[0], size[1], -1), dim=-1).view(*view)
        max_comp = torch.max(x.view(size[0], size[1], -1), dim=-1).values.view(*view)
        avg_comp = self.conv2(F.relu(self.conv1(avg_comp)))
        max_comp = self.conv2(F.relu(self.conv1(max_comp)))
        return F.sigmoid(avg_comp + max_comp)


class ChannelAttention2D(_ChannelAttention):
    """ChannelAttention2D

    Channel attention layer as presented in
    https://arxiv.org/pdf/1807.06521v2.pdf.
    """

    def __init__(self,
                 in_channels: int,
                 reduction: int = 2):
        """Create ChannelAttention2D Layer

        Args:
            in_channels (int): Number of input channels
            reduction (int, optional): Degree of reduction. Defaults to 2.
        """
        super(ChannelAttention2D, self).__init__()
        self.conv1, self.conv2 = reduction_network(in_channels, reduction, "2d")


class ChannelAttention3D(_ChannelAttention):
    """ChannelAttention3D

    Channel attention layer as presented in
    https://arxiv.org/pdf/1807.06521v2.pdf.
    """

    def __init__(self,
                 in_channels: int,
                 reduction: int = 2):
        """Create ChannelAttention3D Layer

        Args:
            in_channels (int): Number of input channels
            reduction (int, optional): Degree of reduction. Defaults to 2.
        """
        super(ChannelAttention3D, self).__init__()
        self.conv1, self.conv2 = reduction_network(in_channels, reduction, "3d")
