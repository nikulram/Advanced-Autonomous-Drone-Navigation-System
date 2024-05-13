import torch
import torch.nn as nn
import torch.nn.functional as F

class DecisionNet(nn.Module):
    """
    A neural network that integrates image and sensor data for enhanced decision making.
    This network is designed for image recognition tasks where additional sensor data
    is also available and relevant for making decisions.
    """

    def __init__(self):
        super(DecisionNet, self).__init__()
        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)  # First convolutional layer, 3 input channels, 16 output channels
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)  # Second convolutional layer, 16 input channels, 32 output channels

        # Calculate the exact output size after convolutions and pooling to connect to fully connected layer
        self.fc1_input_size = self.calculate_fc1_input_size(64)  # input images are 64x64 pixels
        self.fc1 = nn.Linear(self.fc1_input_size + 10, 120)  # Fully connected layer that also considers 10 additional sensor data points
        self.fc2 = nn.Linear(120, 6)  # Output layer with 6 outputs (e.g : classes or actions)
    
    def forward(self, x, sensors):
        """
        Defines the forward pass of the model with image and sensor data.
        
        Args:
            x (tensor): Input image data.
            sensors (tensor): Sensor data relevant to decision-making.

        Returns:
            tensor: Output predictions from the network.
        """
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)  # Apply ReLU activation followed by a 2x2 max pooling to the first convolution output
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)  # Apply ReLU activation followed by a 2x2 max pooling to the second convolution output
        x = torch.flatten(x, 1)  # Flatten the output to feed into the fully connected layer
        x = torch.cat((x, sensors), dim=1)  # Concatenate the flattened image features with sensor data
        x = F.relu(self.fc1(x))  # Apply ReLU activation to the output of the first fully connected layer
        x = self.fc2(x)  # Output layer that provides the final predictions
        return x

    def calculate_fc1_input_size(self, input_size):
        """
        Calculate the size of the tensor entering the first fully connected layer (fc1) after convolutions and pooling.

        Args:
            input_size (int): The size of one side of the square input image (assuming a square image).

        Returns:
            int: The calculated input size to fc1.
        """
        size_after_conv = input_size // 2 // 2  # Calculate the size after two 2x2 max pooling layers
        return size_after_conv * size_after_conv * 32  # Multiply by the number of output channels from the last Conv layer
