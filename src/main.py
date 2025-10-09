import io
import sys
from logging import Logger

from vex import Brain


def main(brain, robot_file):
    error_log = Logger("logs/error", 0)
    error_log.info("Starting Robot")
    error_log.flush_logs()
    try:
        error_log.info("Importing Robot class from {}".format(robot_file))
        error_log.flush_logs()
        robot_module = __import__(robot_file)
        robot = robot_module.Robot(brain)

        robot.start()
    except Exception as e:
        error_log.error("Failed to import Robot class from {}".format(robot_file))
        error_log.flush_logs()
        exception_buffer = io.StringIO()
        sys.print_exception(e, exception_buffer)
        for log_entry in exception_buffer.getvalue().split("\n"):
            error_log.fatal(str(log_entry))
            brain.screen.print(str(log_entry))
            brain.screen.next_row()
        error_log.flush_logs()
        raise e

    # del robot  # Delete the robot instance
    #
    # for module_name in sys.modules.keys():
    #     print("Wiping cached module: " + str(sys.modules[module_name]))
    #     del sys.modules[module_name]
    # if len(sys.modules) == 0:
    #     print("Successfully cleared all cached modules")
    # else:
    #     raise RuntimeError("Failed to clear all cached modules, remaining: " + str(sys.modules))
