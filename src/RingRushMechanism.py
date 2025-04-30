from VEXLib.Util.Logging import Logger
from vex import DigitalOut, Brain


# ring_rush_mechanism_log = Logger(Brain().sdcard, Brain().screen, "ring_rush_mechanism")


class RingRushMechanism:
    def __init__(self, piston_port):
        self.ring_rush_mechanism_piston = DigitalOut(piston_port)
        self.ring_rush_mechanism_state = False
        # self.log = ring_rush_mechanism_log

    def _update_state(self):
        # self.log.trace(
        # "_update_state: setting state to {}".format(self.ring_rush_mechanism_state)
        # )
        self.ring_rush_mechanism_piston.set(self.ring_rush_mechanism_state)

    def lower_ring_rush_mechanism(self):
        # self.log.trace("Lowering Ring Rush Mechanism")
        self.ring_rush_mechanism_state = True
        self._update_state()

    def raise_ring_rush_mechanism(self):
        # self.log.trace("Raising Ring Rush Mechanism")
        self.ring_rush_mechanism_state = False
        self._update_state()

    def toggle_ring_rush_mechanism(self):
        # self.log.trace(
        #     "Toggling ring rush mechanism from {} to {}".format(
        #         self.ring_rush_mechanism_state, not self.ring_rush_mechanism_state
        #     )
        # )
        self.ring_rush_mechanism_state = not self.ring_rush_mechanism_state
        self._update_state()
