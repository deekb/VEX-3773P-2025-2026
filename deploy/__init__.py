import argparse
import sys
import time
from subprocess import CalledProcessError

from rich.console import Console
from rich.text import Text

from deploy.Constants import *
from deploy.Utils import *

os.chdir(PROJECT_ROOT)

parser = argparse.ArgumentParser(description="VEX SD Card Deployment Tool")
parser.add_argument("--no-unmount", action="store_true", help="Do not unmount the SD card after operations")
parser.add_argument("--no-push-src", action="store_true", help="Skip pushing source files")
parser.add_argument("--no-push-lib", action="store_true", help="Skip pushing library files")
parser.add_argument("--no-push-deploy", action="store_true", help="Skip pushing deploy objects")
parser.add_argument("--no-pull-logs", action="store_true", help="Skip pulling logs")
parser.add_argument("--verbose", action="store_true", help="Enable verbose/debug output")
args = parser.parse_args()

console = Console()


def verbose_print(msg):
    if args.verbose:
        console.print(f"[blue][VERBOSE] {msg}")


# Helper function to scan a directory and get all file paths
def scan_directory(directory: str, exclude_fn=lambda path: False):
    return [
        str(os.path.join(root, file))
        for root, _, files in os.walk(directory)
        for file in files
        if os.path.isfile(os.path.join(root, file)) and (not exclude_fn(os.path.join(root, file)))
    ]


# Function to handle the file copy process and update counts
def copy_files_and_update_count(source_files, destination_folder, base_folder, update_fn):
    verbose_print(f"Files to copy: {source_files}")
    with console.status(f"[cyan]Copying files to {destination_folder}...") as status:
        update_fn(*copy_if_changed(source_files, destination_folder, base_folder_to_copy_from=base_folder))


def main():
    ascii_art_text = Text(ASCII_ART, style="bold bright_blue")
    console.print(ascii_art_text)

    with console.status("[cyan]Searching for SD card...") as status:
        vex_disk = find_vex_disk(DRIVE_IDENTIFIER_STRING, FIND_VEX_DISK_MAX_ATTEMPTS, FIND_VEX_DISK_TIME_BETWEEN_ATTEMPTS)

    if not vex_disk:
        console.print(
            f"[bold red]Could not find any storage medium with \"{DRIVE_IDENTIFIER_STRING}\" in name[/bold red]")
        sys.exit(19)  # ENODEV No such device

    vex_disk_path = vex_disk.path
    console.print(f"[bold green]Found VEX disk at {vex_disk_path}[/bold green]")

    total_files_deployed = 0
    total_bytes_copied = 0

    total_files_pulled = 0
    total_bytes_pulled = 0

    def update_deployed_count_and_size(deployed_count, deployed_size_bytes):
        nonlocal total_files_deployed, total_bytes_copied
        total_files_deployed += deployed_count
        total_bytes_copied += deployed_size_bytes

    def update_pulled_count_and_size(deployed_count, deployed_size_bytes):
        nonlocal total_files_pulled, total_bytes_pulled
        total_files_pulled += deployed_count
        total_bytes_pulled += deployed_size_bytes

    start_time = time.perf_counter()

    if not args.no_pull_logs:
        log_objects = scan_directory(str(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk_path, "logs")))
        verbose_print(f"Discovered logs: {log_objects}")
        copy_files_and_update_count(log_objects, os.path.join(PROJECT_ROOT, "logs/"),
                                    str(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk_path, "logs")),
                                    update_pulled_count_and_size)

    if not args.no_push_src:
        src_objects = scan_directory(SRC_DIRECTORY, exclude_from_deploy)
        copy_files_and_update_count(src_objects, str(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk_path)), SRC_DIRECTORY,
                                    update_deployed_count_and_size)

    if not args.no_push_lib:
        library_objects = scan_directory(VEXLIB_DIRECTORY, exclude_from_deploy)
        copy_files_and_update_count(library_objects, str(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk_path, "VEXlib")),
                                    VEXLIB_DIRECTORY, update_deployed_count_and_size)

    if not args.no_push_deploy:
        deploy_objects = scan_directory(DEPLOY_DIRECTORY, exclude_from_deploy)
        copy_files_and_update_count(deploy_objects, str(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk_path, "deploy")),
                                    DEPLOY_DIRECTORY, update_deployed_count_and_size)

    # Ensure the 'logs' directory exists
    if not os.path.isdir(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk_path, "logs")):
        os.mkdir(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk_path, "logs"))
        verbose_print("[bold yellow]Created missing 'logs' directory on disk[/bold yellow]")

    if not args.no_unmount:
        with console.status("[yellow]Unmounting drive, please do not remove :warning:") as status:
            while True:
                try:
                    time.sleep(0.25)
                    unmount_drive(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk_path))
                    break
                except CalledProcessError:
                    console.print("[bold yellow]Failed to unmount drive, retrying...[/bold yellow]")
                    continue
            verbose_print("[green]Unmounted drive successfully[/green]")

        console.print(f"[bold green]Completed in {round(time.perf_counter() - start_time, 2)} seconds[/bold green]")
        console.print("[bold green]You may now remove the drive :thumbsup:[/bold green]")
    else:
        console.print(f"[bold green]Completed in {round(time.perf_counter() - start_time, 2)} seconds[/bold green]")

    # Final stats with color
    console.print(f"[bold red]↑ Uploaded {total_files_deployed} files ({convert_size(total_bytes_copied)})[/bold red]")
    console.print(
        f"[bold blue]↓ Downloaded {total_files_pulled} files ({convert_size(total_bytes_pulled)})[/bold blue]")


if __name__ == "__main__":
    main()
