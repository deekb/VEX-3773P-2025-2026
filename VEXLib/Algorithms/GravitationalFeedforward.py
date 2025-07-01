import math


class GravitationalFeedforward:
    """
    A feedforward used to combat gravity.
    """

    def __init__(self, kg: float = 0.0, horizontal_rotation: float = 0.0, vertical_rotation: float = 0.0):
        """
        Initializes a GravitationalFeedforward instance.

        Args:
            kg: Gravitational gain value for the feedforward.
            horizontal_rotation: The rotation considered as horizontal.
            vertical_rotation: The rotation considered as vertical.
        """
        self.kg = kg
        self.horizontal_rotation = horizontal_rotation
        self.vertical_rotation = vertical_rotation

    def update(self, current_rotation: float) -> float:
        """
        Update the feedforward state with the most recent current value and calculate the control output.

        Args:
            current_rotation: The current rotation measurement.

        Returns:
            The calculated control output.
        """
        rotation_radians = math.radians(current_rotation)

        # Normalize the current rotation within the range [0, vertical_rotation]
        rotation_radians %= math.pi * 2

        # Calculate the gravitational feedforward output using trigonometry
        return math.sin(rotation_radians) * self.kg
