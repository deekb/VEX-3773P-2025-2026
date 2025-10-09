from vex import DigitalOut


class MatchLoadHelper:
    def __init__(self, piston: DigitalOut):
        self.piston = piston

    def extend(self):
        self.piston.set(True)

    def retract(self):
        self.piston.set(False)