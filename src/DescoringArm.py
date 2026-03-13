from vex import DigitalOut

class DescoringArm:
    """
    A subsystem class that controls a pneumatic piston for the descoring arm.

    Attributes:
        piston (DigitalOut): A digital output object controlling the pneumatic solenoid.
    """

    def __init__(self, in_out_piston: DigitalOut, up_down_piston: DigitalOut):
        """
        Initializes the MatchLoadHelper with a specified piston output.

        Args:
            piston (DigitalOut): The digital output that activates the pneumatic piston.
        """
        self.in_out_piston = in_out_piston
        self.up_down_piston = up_down_piston
        self.up_state = False
        self.out_state = False

    def piston_out(self):
        """
        Extends the piston to activate the match loader mechanism.

        This method sends a high (True) signal to the digital output,
        opening the pneumatic valve and extending the piston.
        """
        self.out_state = True
        self.in_out_piston.set(self.out_state)

    def piston_in(self):
        """
        Retracts the piston to deactivate the match loader mechanism.

        This method sends a low (False) signal to the digital output,
        closing the pneumatic valve and retracting the piston.
        """
        self.out_state = False
        self.in_out_piston.set(self.out_state)

    def piston_up(self):
        """
        Extends the piston to activate the match loader mechanism.

        This method sends a high (True) signal to the digital output,
        opening the pneumatic valve and extending the piston.
        """
        self.up_state = True
        self.up_down_piston.set(self.up_state)

    def piston_down(self):
        """
        Retracts the piston to deactivate the match loader mechanism.

        This method sends a low (False) signal to the digital output,
        closing the pneumatic valve and retracting the piston.
        """
        self.up_state = False
        self.up_down_piston.set(self.up_state)


    def wing_stow(self):
        self.piston_in()
        self.piston_down()

    def wing_out_and_down(self):
        self.piston_out()
        self.piston_down()

    def wing_out_and_up(self):
        self.piston_out()
        self.piston_up()

    def next_state(self):
        if not self.out_state:
            self.wing_out_and_down()
        elif self.out_state and not self.up_state:
            self.wing_out_and_up()

    def previous_state(self):
        if self.out_state and not self.up_state:
            self.wing_stow()
        elif self.out_state and not self.up_state:
            self.wing_out_and_down()


