class CornerMechanism:
    def __init__(self, digital_out):
        self.corner_mechanism_piston = digital_out
        self.corner_mechanism_state = False

    def _update_state(self):
        self.corner_mechanism_piston.set(self.corner_mechanism_state)

    def lower_corner_mechanism(self):
        self.corner_mechanism_state = True
        self._update_state()

    def raise_corner_mechanism(self):
        self.corner_mechanism_state = False
        self._update_state()

    def toggle_corner_mechanism(self):
        self.corner_mechanism_state = not self.corner_mechanism_state
        self._update_state()
