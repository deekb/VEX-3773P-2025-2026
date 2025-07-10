def main(brain, robot_file):

    robot_module = __import__(robot_file)
    robot = robot_module.Robot(brain)

    robot.start()

    # del robot  # Delete the robot instance
    #
    # for module_name in sys.modules.keys():
    #     print("Wiping cached module: " + str(sys.modules[module_name]))
    #     del sys.modules[module_name]
    # if len(sys.modules) == 0:
    #     print("Successfully cleared all cached modules")
    # else:
    #     raise RuntimeError("Failed to clear all cached modules, remaining: " + str(sys.modules))
