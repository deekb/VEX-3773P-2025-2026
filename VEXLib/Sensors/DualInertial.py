from vex import Inertial, DEGREES


class DualInertial:
    """
    Wraps two inertial sensors and averages their readings.
    Exposes the same interface as vex.Inertial so it is a
    drop-in replacement anywhere a single sensor is accepted.
    """

    DIVERGENCE_THRESHOLD = 5.0  # degrees

    def __init__(self, sensor_a: Inertial, sensor_b: Inertial, on_divergence=None):
        self._a = sensor_a
        self._b = sensor_b
        self._on_divergence = on_divergence
        self._diverging = False

    def set_turn_type(self, turn_type):
        self._a.set_turn_type(turn_type)
        self._b.set_turn_type(turn_type)

    def rotation(self, units=DEGREES):
        a = self._a.rotation(units)
        b = self._b.rotation(units)
        diverging_now = abs(a - b) > self.DIVERGENCE_THRESHOLD
        if diverging_now != self._diverging:
            self._diverging = diverging_now
            if self._on_divergence is not None:
                self._on_divergence(a, b, diverging_now)
        if diverging_now:
            return a
        return (a + b) / 2.0

    def calibrate(self):
        self._a.calibrate()
        self._b.calibrate()

    def is_calibrating(self):
        return self._a.is_calibrating() or self._b.is_calibrating()

    def set_heading(self, value, units=DEGREES):
        self._a.set_heading(value, units)
        self._b.set_heading(value, units)
