def main(brain):
    while True:
        from vex import Thread, wait, MSEC
        if not brain.sdcard.is_inserted():
            brain.screen.print("Please insert the SD card")
            print("Please insert the SD card")
            while not brain.sdcard.is_inserted():
                wait(50, MSEC)
            wait(1000, MSEC)  # Make sure that the SD card is well-situated
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
        # try:
        from Robot import Robot
        from VEXLib.Util import time as time
        from hash import test, md5sum, md5sum_file
        import sys
        # except (OSError, ImportError):
        #     brain.screen.print("Error loading modules, retrying...")
        #     wait(1000, MSEC)
        #     continue

        robot = Robot(brain)

        robot_thread = Thread(robot.start)

        while not robot.restart_requested:
            if robot.telemetry.serial.peek(True) == "UPLOAD":
                robot.telemetry.serial.receive(True)
                robot.telemetry.serial.send("OK")
                files = {}
                while not robot.telemetry.serial.peek(True) == "FILE_LIST_DONE":
                    if "FILE:" in robot.telemetry.serial.peek(True):
                        message = robot.telemetry.serial.receive(True)
                        file_name, file_hash = message.split(":")[-1].split("|")
                        files[file_name] = file_hash

                robot.telemetry.serial.send(str(files))

                robot.telemetry.serial.send("OK")
            time.sleep(0.05)
        print("Restarting robot")
        robot_thread.stop()
        robot.on_disable()
        robot.on_driver_control_disable()
        robot.on_autonomous_disable()
        del robot  # Delete the robot instance

        for module_name in sys.modules.keys():
            print("Wiping cached module: " + str(sys.modules[module_name]))
            del sys.modules[module_name]
        if len(sys.modules) == 0:
            print("Successfully cleared all cached modules")
        else:
            raise RuntimeError("Failed to clear all cached modules, remaining: " + str(sys.modules))
