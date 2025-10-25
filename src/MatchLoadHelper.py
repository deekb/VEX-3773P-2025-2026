from vex import DigitalOut

class MatchLoadHelper:
    """
    A subsystem class that controls a pneumatic piston for a VEX robot’s match loader mechanism.

    The Match Load Helper manages the piston responsible for assisting with  removing
    game elements from the match-load towers during a match.

    Attributes:
        piston (DigitalOut): A digital output object controlling the pneumatic solenoid.
    """

    def __init__(self, piston: DigitalOut):
        """
        Initializes the MatchLoadHelper with a specified piston output.

        Args:
            piston (DigitalOut): The digital output that activates the pneumatic piston.
        """
        self.piston = piston

    def extend(self):
        """
        Extends the piston to activate the match loader mechanism.

        This method sends a high (True) signal to the digital output,
        opening the pneumatic valve and extending the piston.
        """
        self.piston.set(True)

    def retract(self):
        """
        Retracts the piston to deactivate the match loader mechanism.

        This method sends a low (False) signal to the digital output,
        closing the pneumatic valve and retracting the piston.
        """
        self.piston.set(False)
