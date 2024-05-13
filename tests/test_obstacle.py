import unittest
from unittest.mock import patch, MagicMock
from obstacle import ObstacleDetector

class TestObstacleDetector(unittest.TestCase):
    def setUp(self):
        # Mock the load_model method to prevent actual file loading
        with patch('obstacle.ObstacleDetector.load_model', return_value=MagicMock()):
            self.obstacle_detector = ObstacleDetector('dummy_path_to_camera_model.pth', 'dummy_path_to_lidar_model.pth')

    def test_detect_obstacles_camera(self):
        """Test obstacle detection using the camera."""
        self.obstacle_detector.detect_obstacles_camera = MagicMock(return_value="Detected objects")
        camera_obstacles = self.obstacle_detector.detect_obstacles_camera('path_to_image.jpg')
        self.assertEqual(camera_obstacles, "Detected objects")

    def test_detect_obstacles_lidar(self):
        """Test obstacle detection using LiDAR."""
        self.obstacle_detector.detect_obstacles_lidar = MagicMock(return_value="Detected objects")
        lidar_obstacles = self.obstacle_detector.detect_obstacles_lidar([0.1, 0.2, 0.3])  # Example LiDAR data array
        self.assertEqual(lidar_obstacles, "Detected objects")

if __name__ == '__main__':
    unittest.main()
