#! /usr/bin/env python3
"""
Log Viewer Module

This module provides functionality to read, filter, and display log files with rich formatting.
It supports various log levels and allows filtering based on log levels and regex patterns.

Functions:
    read_logs(file_path)
    filter_logs(logs, levels=None, regex=None, comparison="leq", case_insensitive=False, show_all=False)
    display_log_info(logs, filtered_logs, file_path, levels, comparison, show_all)
    display_logs(logs)
    _prepare_levels(levels, show_all)
    _get_log_level(log)
    _should_include_log(log_level, levels, comparison, show_all)
    _matches_regex(log, regex, case_insensitive)
    _count_log_levels(filtered_logs)
    _format_log_levels_display(log_levels_count, levels, comparison, show_all)
    _print_log(log)

Usage Examples:
    # By default log levels higher than or equal to DEBUG are shown
    python LogView.py logs/main-1.log

    # Choose to show logs higher than, less than, or equal to the specified level with LEQ, HEQ, and EQ
    python LogView.py logs/main-1.log --comparison EQ

    # If two or more log levels are specified only they will be shown
    python LogView.py logs/main-1.log --info --warn

    # Logs can be filtered using a reqular expression, which can optionally be made case-insensitive
    python LogView.py logs/main-1.log --regex "Calibrating" --case-insensitive

    # You can also view all log entries
    python LogView.py logs/main-1.log --all
"""

import os.path
import re

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

# Define log levels and their corresponding colors
log_levels = {
    "TRACE": "dim",
    "DEBUG": "cyan",
    "INFO": "green",
    "WARN": "yellow",
    "ERROR": "red",
    "FATAL": "bold red",
}

log_levels_order = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"]


def read_logs(file_path):
    """
    Read the log file and return its contents as a list of lines.

    Args:
        file_path (str): The path to the log file.

    Returns:
        list: A list of log entries (lines).
    """
    with open(file_path, "r") as file:
        return file.readlines()


def filter_logs(
    logs,
    levels=None,
    regex=None,
    comparison="leq",
    case_insensitive=False,
    show_all=False,
):
    """
    Filter the logs based on the specified log levels and regex pattern.

    Args:
        logs (list): The list of log entries.
        levels (list, optional): The list of log levels to include. Defaults to None.
        regex (str, optional): The regex pattern to filter logs. Defaults to None.
        comparison (str, optional): The comparison type for log levels. Defaults to "leq".
        case_insensitive (bool, optional): Whether the regex pattern is case insensitive. Defaults to False.
        show_all (bool, optional): Whether to show all log levels. Defaults to False.

    Returns:
        list: The filtered list of log entries.
    """
    filtered_logs = []
    levels = _prepare_levels(levels, show_all)
    for log in logs:
        log_level = _get_log_level(log)
        if not log_level:
            continue
        if not _should_include_log(log_level, levels, comparison, show_all):
            continue
        if regex and not _matches_regex(log, regex, case_insensitive):
            continue
        filtered_logs.append(log)
    return filtered_logs


def display_log_info(logs, filtered_logs, file_path, levels, comparison, show_all):
    """
    Display information about the filtered logs.

    Args:
        logs (list): The list of all log entries.
        filtered_logs (list): The list of filtered log entries.
        file_path (str): The path to the log file.
        levels (list): The list of log levels to include.
        comparison (str): The comparison type for log levels.
        show_all (bool): Whether to show all log levels.
    """
    os.system("clear||cls")
    log_info = f"Showing: {len(filtered_logs)} / {len(logs)} entries\n"
    levels = _prepare_levels(levels, show_all)
    log_levels_count = _count_log_levels(filtered_logs)
    log_levels_display = _format_log_levels_display(
        log_levels_count, levels, comparison, show_all
    )
    log_info += "\n".join(log_levels_display)
    console.print(Panel(log_info, title=os.path.basename(file_path), expand=False))


def display_logs(logs):
    """
    Display the log entries.

    Args:
        logs (list): The list of log entries.
    """
    if not logs:
        console.print(
            "No log entries found for the specified criteria.", style="bold red"
        )
        return
    for log in logs:
        _print_log(log)


def _prepare_levels(levels, show_all):
    """
    Prepare the list of log levels to include.

    Args:
        levels (list): The list of log levels to include.
        show_all (bool): Whether to show all log levels.

    Returns:
        list: The prepared list of log levels.
    """
    if not show_all and levels:
        levels = [level.upper() for level in levels]
        for level in levels:
            if level not in log_levels_order:
                raise ValueError(
                    f"Invalid log level: {level}. Valid log levels are: {', '.join(log_levels_order)}"
                )
    return levels


def _get_log_level(log):
    """
    Get the log level from a log entry.

    Args:
        log (str): The log entry.

    Returns:
        str: The log level, or None if not found.
    """
    return next((lvl for lvl in log_levels if log.startswith(f"<{lvl}>")), None)


def _should_include_log(log_level, levels, comparison, show_all):
    """
    Determine whether a log entry should be included based on its log level.

    Args:
        log_level (str): The log level of the entry.
        levels (list): The list of log levels to include.
        comparison (str): The comparison type for log levels.
        show_all (bool): Whether to show all log levels.

    Returns:
        bool: True if the log entry should be included, False otherwise.
    """
    if show_all or not levels:
        return True
    log_level_index = log_levels_order.index(log_level)
    if comparison.upper() == "EQ":
        return log_level in levels
    elif comparison.upper() == "LEQ":
        return any(log_levels_order.index(lvl) >= log_level_index for lvl in levels)
    elif comparison.upper() == "HEQ":
        return any(log_levels_order.index(lvl) <= log_level_index for lvl in levels)
    return False


def _matches_regex(log, regex, case_insensitive):
    """
    Check if a log entry matches a regex pattern.

    Args:
        log (str): The log entry.
        regex (str): The regex pattern.
        case_insensitive (bool): Whether the regex pattern is case insensitive.

    Returns:
        bool: True if the log entry matches the regex pattern, False otherwise.
    """
    flags = re.IGNORECASE if case_insensitive else 0
    return re.search(regex, log, flags=flags)


def _count_log_levels(filtered_logs):
    """
    Count the occurrences of each log level in the filtered logs.

    Args:
        filtered_logs (list): The list of filtered log entries.

    Returns:
        dict: A dictionary with log levels as keys and their counts as values.
    """
    log_levels_count = {lvl: 0 for lvl in log_levels_order}
    for log in filtered_logs:
        log_level = _get_log_level(log)
        if log_level:
            log_levels_count[log_level] += 1
    return log_levels_count


def _format_log_levels_display(log_levels_count, levels, comparison, show_all):
    """
    Format the log levels display.

    Args:
        log_levels_count (dict): A dictionary with log levels as keys and their counts as values.
        levels (list): The list of log levels to include.
        comparison (str): The comparison type for log levels.
        show_all (bool): Whether to show all log levels.

    Returns:
        list: A list of formatted log levels display strings.
    """
    log_levels_display = []
    for log_level in log_levels_order:
        color = log_levels[log_level]
        count = log_levels_count[log_level]
        if not show_all and levels:
            if len(levels) > 1:
                if log_level not in levels:
                    continue
            else:
                log_level_index = log_levels_order.index(log_level)
                if comparison == "eq" and log_level not in levels:
                    continue
                elif comparison == "leq" and all(
                    log_levels_order.index(lvl) > log_level_index for lvl in levels
                ):
                    continue
                elif comparison == "heq" and all(
                    log_levels_order.index(lvl) < log_level_index for lvl in levels
                ):
                    continue
        log_levels_display.append(f"[{color}]<{log_level}>: {count}[/]")
    return log_levels_display


def _print_log(log):
    """
    Print a log entry with the appropriate color based on its log level.

    Args:
        log (str): The log entry.
    """
    for level, color in log_levels.items():
        if log.startswith(f"<{level}>"):
            text = Text(log.strip(), style=color)
            console.print(text)
            break


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Log Viewer - A tool to view and filter log files with rich formatting."
    )
    parser.add_argument("file", help="Path to the log file to be viewed.")
    parser.add_argument("--trace", action="store_true", help="Show TRACE level logs.")
    parser.add_argument("--debug", action="store_true", help="Show DEBUG level logs.")
    parser.add_argument("--info", action="store_true", help="Show INFO level logs.")
    parser.add_argument("--warn", action="store_true", help="Show WARN level logs.")
    parser.add_argument("--error", action="store_true", help="Show ERROR level logs.")
    parser.add_argument("--fatal", action="store_true", help="Show FATAL level logs.")
    parser.add_argument("--all", action="store_true", help="Show all log levels.")
    parser.add_argument(
        "--comparison",
        default="HEQ",
        help="Comparison type for log levels: EQ: equal to the specified level, LEQ: lower than (more verbose) or equal to the specified level, or HEQ: higher than (less verbose) or equal to the specified level. Default is HEQ.",
    )
    parser.add_argument("--regex", help="Filter logs by a regex pattern.")
    parser.add_argument(
        "--case-insensitive",
        action="store_true",
        help="Make the regex pattern case insensitive.",
    )
    args = parser.parse_args()

    levels = []
    if args.trace:
        levels.append("TRACE")
    if args.debug:
        levels.append("DEBUG")
    if args.info:
        levels.append("INFO")
    if args.warn:
        levels.append("WARN")
    if args.error:
        levels.append("ERROR")
    if args.fatal:
        levels.append("FATAL")

    try:
        logs = read_logs(args.file)
        filtered_logs = filter_logs(
            logs,
            levels=levels,
            regex=args.regex,
            comparison=args.comparison,
            case_insensitive=args.case_insensitive,
            show_all=args.all,
        )
        display_log_info(
            logs,
            filtered_logs,
            file_path=args.file,
            levels=levels,
            comparison=args.comparison,
            show_all=args.all,
        )
        display_logs(filtered_logs)
    except ValueError as e:
        console.print(str(e), style="bold red")
