class ConnectionSynchronizer:
    def __init__(self):
        self.serial_is_connected = True
        self.network_socket_is_connected = True
        self.rpi_restart_requested = False
        self.bridge_restart_requested = False

    def set_both_connected(self):
        self.serial_is_connected = True
        self.network_socket_is_connected = True

    def set_both_disconnected(self):
        self.serial_is_connected = False
        self.network_socket_is_connected = False

    def get_both_connected(self):
        return self.serial_is_connected and self.network_socket_is_connected

    def get_both_disconnected(self):
        return not self.serial_is_connected and not self.network_socket_is_connected

    def get_any_disconnected(self):
        return not self.get_both_connected()

    def get_any_restart_requested(self):
        return self.rpi_restart_requested or self.bridge_restart_requested
