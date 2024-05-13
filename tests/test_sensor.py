import unittest
import numpy as np
import cv2
from PIL import Image
from unittest.mock import patch, MagicMock
from sensor import SensorInput
from exceptions import SensorError

class TestSensorInput(unittest.TestCase):
    def setUp(self):
        self.patcher_camera = patch('cv2.VideoCapture')
        self.mock_camera = self.patcher_camera.start()
        self.mock_camera_instance = MagicMock()
        self.mock_camera.return_value = self.mock_camera_instance
        self.mock_camera_instance.isOpened.return_value = True
        self.mock_camera_instance.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))

        self.sensor_input = SensorInput(camera_index=0, lidar_config={'port': '/dev/ttyUSB0'})
        self.addCleanup(self.patcher_camera.stop)

    def test_camera_data_retrieval_success(self):
        """Test successful camera data retrieval."""
        frame = self.sensor_input.get_camera_data()
        self.assertIsInstance(frame, Image.Image)

    def test_camera_data_retrieval_failure(self):
        """Test handling failure in camera data retrieval."""
        self.mock_camera_instance.read.return_value = (False, None)
        with self.assertRaises(SensorError):
            self.sensor_input.get_camera_data()

    def test_lidar_data_handling(self):
        """Test LiDAR data handling."""
        with patch('numpy.random.rand', return_value=np.random.rand(360) * 100):
            lidar_data = self.sensor_input.get_lidar_data()
            self.assertEqual(len(lidar_data), 360)

    def test_resource_management(self):
        """Ensure resources are properly released."""
        self.sensor_input.release_resources()
        self.mock_camera_instance.release.assert_called_once()

if __name__ == '__main__':
    unittest.main()
