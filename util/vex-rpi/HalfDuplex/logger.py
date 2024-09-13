import sdnotify


# Systemd notifier for service management
systemd_notifier = sdnotify.SystemdNotifier()


def log(message):
    """
    Logs a message and sends a notification to systemd.

    Args:
        message (str): The message to be logged and notified.
    """
    print(message)
    systemd_notifier.notify(f"STATUS={message}")
