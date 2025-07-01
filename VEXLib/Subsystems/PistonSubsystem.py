from vex import DigitalOut


class PistonSubsystem:
    def __init__(self, port, extended_state=True, name="Piston", state_names=None):
        """
        Initializes the piston subsystem.

        :param port: The DigitalOut port where the piston is connected.
        :param extended_state: The state considered as 'extended', default is True.
        :param name: The name of the piston subsystem.
        :param state_names: A dictionary with custom names for the states (e.g., {"extend": "deploy", "retract": "store"}).
        """
        self.piston = DigitalOut(port)
        self.piston_state = not extended_state  # Initially retracted
        self.extended_state = extended_state  # Which value represents extended
        self.name = name

        # If state_names is provided, use those; otherwise, use defaults
        self.state_names = state_names if state_names else {"extend": "extend",
                                                            "retract": "retract",
                                                            "toggle": "toggle"}

        # Dynamically assign methods based on the given state names
        self._assign_state_methods()

        # Set the initial state
        self._update_state()

    def _update_state(self):
        """Updates the Piston's state via DigitalOut."""
        self.piston.set(self.piston_state)

    def _assign_state_methods(self):
        """
        Dynamically defines and assigns methods based on state names.
        """

        # Define the `extend` method using the appropriate state name
        def extend_function():
            """Extends the piston."""
            self.piston_state = self.extended_state
            self._update_state()

        # Define the `retract` method using the appropriate state name
        def retract_function():
            """Retracts the piston."""
            self.piston_state = not self.extended_state
            self._update_state()

        # Define the `toggle` method using the appropriate state name
        def toggle_function():
            """Toggles the piston state."""
            self.piston_state = not self.piston_state
            self._update_state()

        # Dynamically assign function names
        setattr(self, self.state_names["extend"], extend_function)
        setattr(self, self.state_names["retract"], retract_function)
        setattr(self, self.state_names["toggle"], toggle_function)

    def get_state(self):
        """
        Returns the current state of the piston.
        :return: True if the piston is extended, False if retracted.
        """
        return self.piston_state == self.extended_state

    def __str__(self):
        """
        String representation of the piston subsystem, showing its current state.
        :return: Current status as a string.
        """
        state = "extended" if self.get_state() else "retracted"
        return f"{self.name}: Piston is currently {state}."
