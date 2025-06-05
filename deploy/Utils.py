import hashlib
import math
import os
import re
import shutil
import subprocess
import time
from typing import Optional
import ast

from deploy import POSIX_MOUNT_POINT_DIR, DEPLOY_EXCLUDE_REGEX

__all__ = [
    "get_checksum",
    "copy_if_changed",
    "RemovableDisk",
    "get_removable_disks",
    "unmount_drive",
    "convert_size",
    "find_vex_disk",
    "exclude_from_deploy",
]


def exclude_from_deploy(filename: str) -> bool:
    """
    Tells the program which files to ignore while scanning the 'deploy' directory.

    Args:
        filename: The name of the file to check.

    Returns:
        bool: True if the file should be excluded, otherwise False.
    """
    return re.search(DEPLOY_EXCLUDE_REGEX, filename) is not None


def get_checksum(file_path: str) -> str:
    """
    Get the MD5 checksum of a file, useful for determining if a file has changed on disk.

    Args:
        file_path: The path of the file.

    Returns:
        str: The checksum of the file.
    """
    with open(file_path, "rb") as file:
        return hashlib.md5(file.read()).hexdigest()


def copy_if_changed(
    files_to_copy: list[str],
    target_directory: str,
    base_folder_to_copy_from: str,
    dry_run: bool = False,
) -> tuple[int, int]:
    """
    Copy files from source to target if they have changed.

    Args:
        files_to_copy: List of file paths to copy.
        target_directory: The target directory for copying files.
        base_folder_to_copy_from: The base folder to compare file paths against.
        dry_run: If True, no actual copying will happen (default is False).

    Returns:
        tuple: A tuple containing two values:
            - The number of deployed files.
            - The total deployed size in bytes.
    """
    deployed_count = 0
    deployed_size_bytes = 0

    # Ensure target directory exists
    if not os.path.exists(target_directory) and not dry_run:
        os.makedirs(target_directory)

    for file in files_to_copy:
        relative_path = os.path.relpath(file, base_folder_to_copy_from)
        target_path = os.path.join(target_directory, relative_path)
        target_dir = os.path.dirname(target_path)

        if not os.path.exists(target_dir) and not dry_run:
            os.makedirs(target_dir)

        if os.path.isdir(target_path):
            print(f"{target_path} exists as a folder, removing it")
            if not dry_run:
                shutil.rmtree(target_path)

        file_to_copy_checksum = get_checksum(file)
        file_to_overwrite_checksum = None

        if os.path.isfile(target_path):
            file_to_overwrite_checksum = get_checksum(target_path)

        if file_to_copy_checksum != file_to_overwrite_checksum:
            if file_to_overwrite_checksum:
                # print(f"{target_path} exists but has invalid checksum: {file_to_overwrite_checksum}, pushing")
                if not dry_run:
                    os.remove(target_path)
            # else:
            #     print(f"{target_path} does not exist, pushing")
            if not dry_run:
                shutil.copy(file, target_path)
            deployed_count += 1
            deployed_size_bytes += os.path.getsize(file)

    return deployed_count, deployed_size_bytes


class RemovableDisk:
    """
    A class representing a removable disk.

    Attributes:
        path (str): The path of the removable disk.
        name (str): The name of the removable disk.
    """

    def __init__(self, path: str, name: str):
        """
        Initializes a RemovableDisk instance.

        Args:
            path: The path of the disk.
            name: The name of the disk.
        """
        self.path = path
        self.name = name


def get_removable_disks(posix_mount_point_dir: str) -> list[RemovableDisk]:
    """
    Returns a list of removable disks found in the specified mount point directory.

    Args:
        posix_mount_point_dir: The directory where removable disks are mounted.

    Returns:
        list: A list of RemovableDisk instances representing the removable disks.
    """
    removable_drives = []

    if os.name == "nt":
        import psutil, win32api

        disks = psutil.disk_partitions()
        for disk in disks:
            if disk.fstype:
                removable_drives.append(
                    RemovableDisk(
                        win32api.GetVolumeInformation(disk.device)[0], disk.mountpoint
                    )
                )

    elif os.name == "posix":
        mount_points = os.listdir(posix_mount_point_dir)
        for mount_point in mount_points:
            drive_name = os.path.basename(mount_point)
            disk_path = os.path.abspath(
                os.path.join(posix_mount_point_dir, mount_point)
            )
            removable_drives.append(RemovableDisk(disk_path, drive_name))

    return removable_drives


def find_vex_disk(
    drive_identifier_string: str, max_attempts: int, time_between_attempts: float
) -> Optional[RemovableDisk]:
    """
    Finds the VEX disk by scanning available removable disks.

    Args:
        drive_identifier_string: The identifier string that is part of the VEX disk name.
        max_attempts: The maximum number of attempts to find the disk.
        time_between_attempts: The time to wait between attempts.

    Returns:
        RemovableDisk: The VEX disk, or None if not found.
    """
    failure_count = 0
    while failure_count <= max_attempts:
        for disk in get_removable_disks(POSIX_MOUNT_POINT_DIR):
            if drive_identifier_string in disk.name:
                return disk
        failure_count += 1
        time.sleep(time_between_attempts)
    return None


def unmount_drive(drive_path: str) -> None:
    """
    Unmount the specified drive.

    Args:
        drive_path: The path of the drive to unmount.

    Raises:
        subprocess.CalledProcessError: If the unmount command fails.
    """
    if os.name == "nt":
        eject_command = (
            f"powershell $driveEject = New-Object -comObject Shell.Application;"
            f"$driveEject.Namespace(17).ParseName('''{drive_path}''').InvokeVerb('''Eject''')"
        )
    else:
        eject_command = ["umount", drive_path]

    subprocess.run(eject_command, check=True)


def convert_size(size_bytes: int) -> str:
    """
    Convert a size in bytes to a human-readable format.

    Args:
        size_bytes: The size in bytes.

    Returns:
        str: The size in a human-readable format (e.g., KB, MB, GB).
    """
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "ZB", "YB")
    if size_bytes == 0:
        return f"0 {size_name[0]}"
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


class FStringToFormatTransformer(ast.NodeTransformer):
    def visit_JoinedStr(self, node):
        # Convert f-strings (JoinedStr) to .format() calls
        format_string = ""
        format_args = []
        for value in node.values:
            if isinstance(value, ast.Str):
                format_string += value.s
            elif isinstance(value, ast.FormattedValue):
                format_string += "{}"
                format_args.append(ast.unparse(value.value) if hasattr(ast, "unparse") else self._unparse(value.value))
        format_call = "{}.format({})".format(
            repr(format_string),
            ", ".join(format_args)
        )
        return ast.parse(format_call).body[0].value


def process_file_in_place(file_path):
    with open(file_path, "r") as f:
        source = f.read()
    tree = ast.parse(source)
    transformer = FStringToFormatTransformer()
    transformed_tree = transformer.visit(tree)
    transformed_code = ast.unparse(transformed_tree) if hasattr(ast, "unparse") else compile(transformed_tree, file_path, "exec")
    with open(file_path, "w") as f:
        f.write(transformed_code)


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                process_file_in_place(os.path.join(root, file))
