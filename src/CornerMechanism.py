class Sides:
    LEFT = 1
    RIGHT = 2


class CornerMechanism:
    def __init__(self, left_digital_out, right_digital_out):
        self.left_corner_mechanism_piston = left_digital_out
        self.right_corner_mechanism_piston = right_digital_out
        self.left_corner_mechanism_state = False
        self.right_corner_mechanism_state = False
        self.active_side = Sides.LEFT

    def _update_left_state(self):
        self.left_corner_mechanism_piston.set(self.left_corner_mechanism_state)

    def _update_right_state(self):
        self.right_corner_mechanism_piston.set(self.right_corner_mechanism_state)

    def lower_left_corner_mechanism(self):
        self.left_corner_mechanism_state = True
        self._update_left_state()

    def raise_left_corner_mechanism(self):
        self.left_corner_mechanism_state = False
        self._update_left_state()

    def lower_right_corner_mechanism(self):
        self.right_corner_mechanism_state = True
        self._update_right_state()

    def raise_right_corner_mechanism(self):
        self.right_corner_mechanism_state = False
        self._update_right_state()

    def toggle_active_corner_mechanism(self):
        if self.active_side == Sides.LEFT:
            self.left_corner_mechanism_state = not self.left_corner_mechanism_state
            self._update_left_state()
        if self.active_side == Sides.RIGHT:
            self.right_corner_mechanism_state = not self.right_corner_mechanism_state
            self._update_right_state()

    def toggle_left_corner_mechanism(self):
        self.left_corner_mechanism_state = not self.left_corner_mechanism_state
        self._update_left_state()

    def toggle_right_corner_mechanism(self):
        self.right_corner_mechanism_state = not self.right_corner_mechanism_state
        self._update_right_state()
