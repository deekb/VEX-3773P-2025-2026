from VEXLib.Math import is_near_continuous
import VEXLib.Util.time as time
from vex import VOLT, FORWARD, LedStateType, PERCENT, Rotation, DEGREES, Distance, MM
from ConstantsV2 import ScoringMechanismProperties


class ScoringMechanism:
    def __init__(self, lower_intake_motor, upper_intake_motor, rotation_sensor: Rotation, optical_sensor, distance_sensor: Distance):
        self.lower_intake_motor = lower_intake_motor
        self.upper_intake_motor = upper_intake_motor
        self.optical_sensor = optical_sensor
        self.distance_sensor = distance_sensor
        self.optical_sensor.set_light(LedStateType.ON)
        self.optical_sensor.set_light_power(100, PERCENT)
        self.ejecting_ring = False
        self.found_ring = False
        self.last_ring_sighting_encoder_count = 0
        self.rotation_sensor = rotation_sensor

    def set_speed(self, speed):
        self.spin_lower_intake(speed)
        self.spin_upper_intake(speed)

    def spin_lower_intake(self, speed):
        self.lower_intake_motor.spin(FORWARD, speed * (12 / 100), VOLT)

    def spin_upper_intake(self, speed):
        self.upper_intake_motor.spin(FORWARD, speed * (12 / 100), VOLT)

    def stop_motor(self):
        self.set_speed(0)

    def intake(self):
        self.set_speed(100)

    def outtake(self):
        self.set_speed(-100)

    def get_ring_color(self):
        if is_near_continuous(238, self.optical_sensor.hue(), 45, 0, 360):
            return "blue"
        elif is_near_continuous(10, self.optical_sensor.hue(), 10, 0, 360):
            return "red"
        else:
            return None

    def ring_is_near(self):
        return self.distance_sensor.object_distance(MM) < 70

    def intake_until_ring(self):
        self.intake()
        while not self.ring_is_near():
            pass
        self.stop_motor()
        print(self.get_ring_color())

    def eject_ring(self):
        self.found_ring = True
        self.ejecting_ring = True
        self.last_ring_sighting_encoder_count = self.rotation_sensor.position(DEGREES)

    def sort_ring(self, alliance_color):
        if self.ejecting_ring:
            if self.distance_sensor.object_distance(MM) < 150:
                self.last_ring_sighting_encoder_count = self.rotation_sensor.position(DEGREES)
            if self.rotation_sensor.position(DEGREES) - self.last_ring_sighting_encoder_count > ScoringMechanismProperties.EJECT_RING_DISTANCE:
                self.outtake()
                time.sleep(0.1)
                self.stop_motor()

                self.ejecting_ring = False
                self.found_ring = False
            return

        if self.ring_is_near():
            ring_color = self.get_ring_color()
            if ring_color != alliance_color:
                self.eject_ring()
            print(self.get_ring_color())

    def tick(self, alliance_color):
        self.sort_ring(alliance_color)
