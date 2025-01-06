import unittest
from unittest.mock import Mock

import vex
from VEXLib.Robot.NewTickBasedRobot import TickBasedRobot, DRIVER_CONTROL_ENABLED, AUTONOMOUS_CONTROL_ENABLED


class TestNewTickBasedRobot(unittest.TestCase):

    def test_callbacks_triggered(self):
        robot = TickBasedRobot(vex.Brain())

        # Mock callback functions
        driver_callback = Mock()
        auto_callback = Mock()


        robot._tick()

        # Assign mock callbacks to robot enable callbacks
        robot.on_driver_control = driver_callback
        robot.on_autonomous = auto_callback

        # Execute transitions
        robot.transition_to(DRIVER_CONTROL_ENABLED)
        robot._tick()
        robot.transition_to(AUTONOMOUS_CONTROL_ENABLED)
        robot._tick()
        robot._tick()

        # Assert the correct callbacks were triggered
        driver_callback.assert_called_once()
        # auto_callback.assert_called_once()
