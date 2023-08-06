import unittest
import torch
import torch.nn as nn

import useful_layers as ul


class ChannelAttention2DTest(unittest.TestCase):

    def test_channel_attention_layer_shape(self):
        se_layer = ul.layers.ChannelAttention2D(3)

        dummy_input = torch.randn(2, 3, 15, 15)  # b, c, h, w
        output = se_layer(dummy_input)

        dummy_input = dummy_input.detach()
        output = output.detach()

        self.assertFalse(torch.equal(dummy_input, dummy_input * output),
                         'The dummy input should be changed by the layer')
        self.assertListEqual([dummy_input.shape[0], dummy_input.shape[1], 1, 1], list(output.shape))


class ChannelAttention3DTest(unittest.TestCase):

    def test_channel_attention_layer_shape(self):
        se_layer = ul.layers.ChannelAttention3D(3)

        dummy_input = torch.randn(2, 3, 15, 15, 15)  # b, c, d, h, w
        output = se_layer(dummy_input).detach()

        dummy_input = dummy_input.detach()

        self.assertFalse(torch.equal(dummy_input, dummy_input * output),
                         'The dummy input should be changed by the layer')
        self.assertListEqual([dummy_input.shape[0], dummy_input.shape[1], 1, 1, 1], list(output.shape),
                             'The shape of input and output should match')


class UnknownChannelAttentionTest(unittest.TestCase):

    def test_unknown_channel_attention(self):
        from useful_layers.layers.channel_attention import _ChannelAttention

        class DummyAttention(_ChannelAttention):
            def __init__(self):
                super(DummyAttention, self).__init__()
                self.conv1 = nn.Conv2d(5, 1, 7)
                self.conv2 = nn.Conv2d(5, 1, 7)

        try:
            dummy_input = torch.randn(1, 5, 3, 3)
            da = DummyAttention()
            da(dummy_input)
            self.fail("DummyAttention forward() call passed")
        except NotImplementedError:
            pass


if __name__ == '__main__':
    unittest.main()
