from VEXLib.Util.Logging import Logger
from vex import DigitalOut, Brain

ring_descorer_log = Logger(Brain().sdcard, Brain().screen, "ring_descorer")


class RingDescorer:
    def __init__(self, piston_port):
        self.ring_descorer_piston = DigitalOut(piston_port)
        self.ring_descorer_state = False
        self.log = ring_descorer_log

    def _update_state(self):
        self.log.trace("_update_state: setting state to {}".format(self.ring_descorer_state))
        self.ring_descorer_piston.set(self.ring_descorer_state)

    def descore_ring(self):
        self.log.trace("Descoring Ring")
        self.ring_descorer_state = True
        self._update_state()

    def reset_ring_descorer(self):
        self.log.trace("Resetting Ring descorer")
        self.ring_descorer_state = False
        self._update_state()

    def toggle_descorer(self):
        self.log.trace("Toggling descorer from {} to {}".format(self.ring_descorer_state, not self.ring_descorer_state))
        self.ring_descorer_state = not self.ring_descorer_state
        self._update_state()
