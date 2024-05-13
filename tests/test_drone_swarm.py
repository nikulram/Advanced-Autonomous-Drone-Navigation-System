import unittest
from unittest.mock import MagicMock
from drone_swarm import DroneSwarm

class TestDroneSwarm(unittest.TestCase):
    def setUp(self):
        self.drone_ids = ['drone1', 'drone2', 'drone3']
        self.control_station_callback = MagicMock()
        self.swarm = DroneSwarm(self.drone_ids, self.control_station_callback)

    def test_task_assignment(self):
        """Test that tasks are assigned correctly to ready drones."""
        task = 'photography'
        self.swarm.assign_task('drone1', task)
        self.assertEqual(self.swarm.drones['drone1']['task'], task)
        self.assertEqual(self.swarm.drones['drone1']['status'], 'busy')

    def test_emergency_landing(self):
        """Test emergency landing procedure for a drone."""
        self.swarm.emergency_landing('drone2')
        self.assertEqual(self.swarm.drones['drone2']['status'], 'emergency')
        self.control_station_callback.assert_called_with('emergency_landing', {'drone_id': 'drone2'})

    def test_user_override(self):
        """Test user override functionality."""
        self.swarm.assign_task('drone3', 'surveillance')
        self.swarm.user_override('drone3', 'cancel_task')
        self.assertEqual(self.swarm.drones['drone3']['status'], 'ready')
        self.assertIsNone(self.swarm.drones['drone3']['task'])

    def test_task_completion(self):
        """Test handling of task completion."""
        self.swarm.assign_task('drone1', 'delivery')
        self.swarm.drones['drone1']['status'] = 'ready'  # Simulate task completion
        self.swarm.drones['drone1']['task'] = None
        self.assertEqual(self.swarm.drones['drone1']['status'], 'ready')
        self.assertIsNone(self.swarm.drones['drone1']['task'])

if __name__ == '__main__':
    unittest.main()
