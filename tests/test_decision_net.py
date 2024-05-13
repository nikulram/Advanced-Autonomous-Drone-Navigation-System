import torch
import unittest
from decision_net import DecisionNet

class TestDecisionNet(unittest.TestCase):
    def setUp(self):
        self.net = DecisionNet()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net.to(self.device)

    def test_initialization(self):
        """Test that the network initializes without errors and outputs the correct layer sizes."""
        self.assertIsInstance(self.net, DecisionNet)
        self.assertTrue(hasattr(self.net, 'conv1'))
        self.assertTrue(hasattr(self.net, 'conv2'))
        self.assertTrue(hasattr(self.net, 'fc1'))
        self.assertTrue(hasattr(self.net, 'fc2'))

    def test_forward_pass(self):
        """Test the forward pass with mock data to ensure output sizes are correct."""
        # Create a mock image tensor and sensor data
        image_size = 64  # suppose 64x64 input images
        image = torch.rand(1, 3, image_size, image_size).to(self.device)  # Batch size of 1
        sensors = torch.rand(1, 10).to(self.device)  # 10 sensor inputs

        # Perform a forward pass
        outputs = self.net(image, sensors)
        
        # Check the output size
        self.assertEqual(outputs.shape, (1, 6))  # suppose the output layer has 6 classes

    def test_model_loads_proper_state_dict(self):
        """Test loading the model state dict (simulated)."""
        # Adjusted to the correct computation of fc1 input size
        output_size = (64 // 2 // 2) * (64 // 2 // 2) * 32  # Adjust the calculation according to actual pooling and convolution layers
        state_dict = {
            'conv1.weight': torch.rand(16, 3, 3, 3),
            'conv1.bias': torch.rand(16),
            'conv2.weight': torch.rand(32, 16, 3, 3),
            'conv2.bias': torch.rand(32),
            'fc1.weight': torch.rand(120, output_size + 10),
            'fc1.bias': torch.rand(120),
            'fc2.weight': torch.rand(6, 120),
            'fc2.bias': torch.rand(6)
        }
        self.net.load_state_dict(state_dict)
        for name, param in self.net.named_parameters():
            self.assertTrue(torch.all(torch.eq(param, state_dict[name])))

if __name__ == '__main__':
    unittest.main()
