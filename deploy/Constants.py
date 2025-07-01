import configparser
import os

BASENAME = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASENAME)

# Load constants from config
config = configparser.ConfigParser()
config.read(os.path.join(BASENAME, "config.ini"))


SRC_DIRECTORY = os.path.abspath(config.get("Paths", "SRC_DIRECTORY"))
LOCAL_LOGS_DIRECTORY = os.path.join(PROJECT_ROOT, "logs")
ASSETS_DIRECTORY = os.path.abspath(config.get("Paths", "ASSETS_DIRECTORY"))
VEXLIB_DIRECTORY = os.path.abspath(config.get("Paths", "VEXLIB_DIRECTORY"))
POSIX_MOUNT_POINT_DIR = eval(config.get("Paths", "POSIX_MOUNT_POINT_DIR"))
DRIVE_IDENTIFIER_STRING = config.get("Drive", "DRIVE_IDENTIFIER_STRING")
FIND_VEX_DISK_MAX_ATTEMPTS = config.getint("Drive", "FIND_VEX_DISK_MAX_ATTEMPTS")
FIND_VEX_DISK_TIME_BETWEEN_ATTEMPTS = config.getfloat(
    "Drive", "FIND_VEX_DISK_TIME_BETWEEN_ATTEMPTS"
)
DEPLOY_EXCLUDE_REGEX = config.get("Deploy", "DEPLOY_EXCLUDE_REGEX")
