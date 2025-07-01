import vex
from VEXLib.Geometry.Rotation2d import Rotation2d


class DirectionType:
    CLOCKWISE = 1
    COUNTER_CLOCKWISE = 2


class Inertial(vex.Inertial):
    # TODO: Finish this before using
    def __init__(self, port):
        super().__init__(port)
        self.direction_correction_coefficient = 1
        self.zero_heading_offset = 0

    def set_positive_direction(self, direction):
        if direction == DirectionType.CLOCKWISE:
            self.direction_correction_coefficient = 1
        elif direction == DirectionType.COUNTER_CLOCKWISE:
            self.direction_correction_coefficient = -1

    def set_clockwise_positive(self):
        self.set_positive_direction(DirectionType.CLOCKWISE)

    def set_counter_clockwise_positive(self):
        self.set_positive_direction(DirectionType.COUNTER_CLOCKWISE)

    # def set_zero_heading(self):
    #     self.zero_heading_offset =

    def calibrate(self, blocking=True):
        super().calibrate()
        if blocking:
            self.wait_for_calibration()

    def wait_for_calibration(self):
        while self.is_calibrating():
            pass

    def done_calibrating(self):
        return not self.is_calibrating()

    def get_rotation(self) -> Rotation2d:
        return Rotation2d.from_degrees(self.rotation()) * self.direction_correction_coefficient

    def get_normalized_rotation(self) -> Rotation2d:
        return self.get_rotation().normalize()
