import configparser
import os

BASENAME = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASENAME)

os.chdir(PROJECT_ROOT)

# Load constants from config
config = configparser.ConfigParser()
config.read("deploy_config.ini")


SRC_DIRECTORY = os.path.abspath(config.get("Paths", "SRC_DIRECTORY"))
DEPLOY_DIRECTORY = os.path.abspath(config.get("Paths", "DEPLOY_DIRECTORY"))
VEXLIB_DIRECTORY = os.path.abspath(config.get("Paths", "VEXLIB_DIRECTORY"))
MAIN_PROGRAM = os.path.abspath(config.get("Paths", "MAIN_PROGRAM_PATH"))
POSIX_MOUNT_POINT_DIR = eval(config.get("Paths", "POSIX_MOUNT_POINT_DIR"))
DRIVE_IDENTIFIER_STRING = config.get("Drive", "DRIVE_IDENTIFIER_STRING")
FIND_VEX_DISK_MAX_ATTEMPTS = config.getint("Drive", "FIND_VEX_DISK_MAX_ATTEMPTS")
FIND_VEX_DISK_TIME_BETWEEN_ATTEMPTS = config.getfloat("Drive", "FIND_VEX_DISK_TIME_BETWEEN_ATTEMPTS")
VEX_BUILTIN_MODULES = config.get("Deploy", "VEX_BUILTIN_MODULES")
DEPLOY_EXCLUDE_REGEX = config.get("Deploy", "DEPLOY_EXCLUDE_REGEX")

ASCII_ART = r"""
 __     ______ ____  ____    ____             _                                  _     _____           _ 
 \ \   / / ___/ ___||  _ \  |  _ \  ___ _ __ | | ___  _   _ _ __ ___   ___ _ __ | |_  |_   _|__   ___ | |
  \ \ / /|___ \___ \| | | | | | | |/ _ \ '_ \| |/ _ \| | | | '_ ` _ \ / _ \ '_ \| __|   | |/ _ \ / _ \| |
   \ V /  ___) |__) | |_| | | |_| |  __/ |_) | | (_) | |_| | | | | | |  __/ | | | |_    | | (_) | (_) | |
    \_/  |____/____/|____/  |____/ \___| .__/|_|\___/ \__, |_| |_| |_|\___|_| |_|\__|   |_|\___/ \___/|_|
                                       |_|            |___/                                              
"""