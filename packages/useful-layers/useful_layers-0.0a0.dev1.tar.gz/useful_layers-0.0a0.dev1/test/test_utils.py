import unittest
import torch.nn as nn

import useful_layers
from useful_layers.utils import reduction_network


class UtilsTest(unittest.TestCase):

    def test_reduction_network_2d(self):
        conv1, conv2 = reduction_network(3, 2, "2d")
        self.assertTrue(isinstance(conv1, nn.Conv2d), f"Expected 2D filter, got {conv1}")
        self.assertTrue(isinstance(conv2, nn.Conv2d), f"Expected 2D filter, got {conv2}")

    def test_reduction_network_3d(self):
        conv1, conv2 = reduction_network(3, 2, "3d")
        self.assertTrue(isinstance(conv1, nn.Conv3d), f"Expected 3D filter, got {conv1}")
        self.assertTrue(isinstance(conv2, nn.Conv3d), f"Expected 3D filter, got {conv1}")

    def test_reduction_fail(self):
        try:
            conv1, conv2 = reduction_network(3, 2, "asf")
            self.fail("Got filter for asf dimension")
        except ValueError:
            pass

        try:
            conv1, conv2 = reduction_network(3, 2, "4d")
            self.fail("Got filter for 4D")
        except ValueError:
            pass


if __name__ == '__main__':
    unittest.main()