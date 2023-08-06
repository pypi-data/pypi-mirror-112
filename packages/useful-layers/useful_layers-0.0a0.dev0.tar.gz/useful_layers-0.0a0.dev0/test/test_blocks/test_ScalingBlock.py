import unittest

import torch

import useful_layers as ul


class ScalingBlockTest(unittest.TestCase):

    def test_se_block(self):
        layer = ul.layers.SqueezeAndExcitation2D(3)
        block = ul.blocks.ScalingBlock(layer)

        dummy_input = torch.rand(2, 3, 4, 4)  # b, c, h, w
        block_output = block(dummy_input).detach()

        layer_output = layer(dummy_input)
        expected_output = (dummy_input * layer_output).detach()

        self.assertTrue(torch.equal(block_output, expected_output))

    def test_channel_attention_block(self):
        layer = ul.layers.ChannelAttention2D(3)
        block = ul.blocks.ScalingBlock(layer)

        dummy_input = torch.rand(2, 3, 4, 4)  # b, c, h, w
        block_output = block(dummy_input).detach()

        layer_output = layer(dummy_input)
        expected_output = (dummy_input * layer_output).detach()

        self.assertTrue(torch.equal(block_output, expected_output))

    def test_nonexisting_layer(self):
        try:
            ul.blocks.ScalingBlock(None)
            self.fail("Block accepted None layer")
        except ValueError:
            pass

        try:
            ul.blocks.ScalingBlock(ul.blocks.ScalingBlock)
            self.fail("Block accepted block")
        except ValueError:
            pass


if __name__ == '__main__':
    unittest.main()
