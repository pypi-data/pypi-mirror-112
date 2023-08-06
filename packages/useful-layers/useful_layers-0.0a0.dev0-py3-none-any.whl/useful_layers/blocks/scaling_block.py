import torch

from useful_layers.layers.ABCLayer import Layer
from useful_layers.blocks.ABCBlock import Block

__all__ = ['ScalingBlock']


class ScalingBlock(Block):
    """Simple scaling block implementation"""

    def __init__(self,
                 layer: Layer) -> None:
        """Create a new scaling block

        Args:
            layer: useful_layers layer to use as base layer

        Raises:
            ValueError: If the layer is not a child of useful_layers.Layer
        """
        super(ScalingBlock, self).__init__()
        if not isinstance(layer, Layer):
            raise ValueError(f'Expected useful_layers.Layer but got {layer}')
        self.layer = layer

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Scaling block forward pass

        Args:
            x: input tensor

        Returns:
            torch.Tensor: fused input and activation map.
        """
        activation_map = self.layer(x)
        return x * activation_map
