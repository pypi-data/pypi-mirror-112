import unittest
import torch

import useful_layers as ul


class SqueezeAndExcitation2DTest(unittest.TestCase):

    def test_squeeze_and_excitation_layer_shape(self):
        se_layer = ul.layers.SqueezeAndExcitation2D(3)

        dummy_input = torch.randn(2, 3, 15, 15)  # b, c, h, w
        output = se_layer(dummy_input)

        dummy_input = dummy_input.detach()
        output = output.detach()

        self.assertFalse(torch.equal(dummy_input, dummy_input * output),
                         'The dummy input should be changed by the layer')
        self.assertListEqual([dummy_input.shape[0], dummy_input.shape[1], 1, 1], list(output.shape))


class SqueezeAndExcitation3DTest(unittest.TestCase):

    def test_squeeze_and_excitation_layer_shape(self):
        se_layer = ul.layers.SqueezeAndExcitation3D(3)

        dummy_input = torch.randn(2, 3, 15, 15, 15)  # b, c, d, h, w
        output = se_layer(dummy_input).detach()

        dummy_input = dummy_input.detach()

        self.assertFalse(torch.equal(dummy_input, dummy_input * output),
                         'The dummy input should be changed by the layer')
        self.assertListEqual([dummy_input.shape[0], dummy_input.shape[1], 1, 1, 1], list(output.shape),
                             'The shape of input and output should match')


class UnknownSqueezeAndExcitationTest(unittest.TestCase):

    def test_unknown_squeeze_and_excitation(self):
        from useful_layers.layers.squeeze_and_excitation import _SqueezeAndExcitation

        class DummySE(_SqueezeAndExcitation):
            self.conv1 = torch.nn.Conv2d(5, 1, 1)
            self.conv2 = torch.nn.Conv2d(1, 1, 1)

        try:
            dummy_input = torch.randn(2, 5, 3, 3)
            se = DummySE()
            se(dummy_input)
            self.fail("Unknown SqueezeAndExcitation layer passed")
        except NotImplementedError:
            pass


if __name__ == '__main__':
    unittest.main()
