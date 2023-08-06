import unittest

import torch

import useful_layers as ul


class SpatialAttention2DTest(unittest.TestCase):

    def test_spatial_attention_layer_shape(self):
        dummy_input = torch.randn(2, 3, 5, 5)
        layer = ul.layers.SpatialAttention2D(3, 3)

        output = layer(dummy_input).detach()
        self.assertListEqual([2, 1, 5, 5], list(output.shape))


class SpatialAttention3DTest(unittest.TestCase):

    def test_spatial_attention_layer_shape(self):
        dummy_input = torch.randn(2, 3, 5, 5, 5)
        layer = ul.layers.SpatialAttention3D(3, 3)

        output = layer(dummy_input).detach()
        self.assertListEqual([2, 1, 5, 5, 5], list(output.shape))


if __name__ == '__main__':
    unittest.main()
