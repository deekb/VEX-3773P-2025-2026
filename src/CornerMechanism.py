class Sides:
    LEFT = 1
    RIGHT = 2


class CornerMechanism:
    def __init__(self, left_digital_out, right_digital_out):
        self.left_corner_mechanism_piston = left_digital_out
        self.right_corner_mechanism_piston = right_digital_out
        self.corner_mechanism_state = False
        self.active_side = Sides.LEFT

    def _update_state(self):
        if self.active_side == Sides.LEFT:
            self.left_corner_mechanism_piston.set(self.corner_mechanism_state)
        elif self.active_side == Sides.RIGHT:
            self.right_corner_mechanism_piston.set(self.corner_mechanism_state)

    def lower_corner_mechanism(self):
        self.corner_mechanism_state = True
        self._update_state()

    def raise_corner_mechanism(self):
        self.corner_mechanism_state = False
        self._update_state()

    def toggle_corner_mechanism(self):
        self.corner_mechanism_state = not self.corner_mechanism_state
        self._update_state()
