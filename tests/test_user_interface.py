import unittest
import tkinter as tk
from tkinter import ttk, messagebox
from unittest import mock 
from user_interface import DroneControlPanel

class TestUserInterface(unittest.TestCase):
    def setUp(self):
        # Set up a real Tkinter root window, but keep it hidden
        self.root = tk.Tk()
        self.root.withdraw()  # Hides the Tkinter window
        self.ui = DroneControlPanel(self.root)

    def tearDown(self):
        # Ensure the Tkinter window is properly destroyed after each test
        self.root.destroy()

    def test_button_clicks(self):
        # Test response to button clicks
        self.ui.start_button.invoke()
        self.assertEqual(self.ui.status.get(), "Status: All Drones Started", "Start button should initiate all drones start")

        self.ui.stop_button.invoke()
        self.assertEqual(self.ui.status.get(), "Status: All Drones Stopped", "Stop button should halt all drones")

    def test_data_display(self):
        # Simulate log data and test display update
        test_message = "Test logging"
        self.ui.log_data(test_message)
        self.assertIn(test_message, self.ui.live_data_display.get('1.0', 'end'), "Log data should appear in live data display")

    def test_error_handling(self):
        # Test error handling dialog
        with mock.patch('tkinter.messagebox.askyesno', return_value=True):
            self.ui.emergency_override()
            self.assertIn("User has overridden the emergency protocol.", self.ui.live_data_display.get('1.0', 'end'))

    def test_ui_load(self):
        # Test UI performance under simulated high load
        for _ in range(1000):
            self.ui.log_data("Test message")
        self.assertNotEqual(self.ui.live_data_display.index('end-1c'), '1.0', "UI should remain responsive under load")

if __name__ == '__main__':
    unittest.main()
