import math

inches_per_foot = 12.0
meters_per_inch = 0.0254
seconds_per_minute = 60.0
kilograms_per_pound = 0.453592
milliseconds_per_second = 1000.0
microseconds_per_millisecond = 1000.0
centimeters_per_meter = 100.0


def meters_to_feet(meters):
    return meters_to_inches(meters) / inches_per_foot


def feet_to_meters(feet):
    return inches_to_meters(feet * inches_per_foot)


def meters_to_inches(meters):
    return meters / meters_per_inch


def meters_to_centimeters(meters):
    return meters * centimeters_per_meter


def inches_to_meters(inches):
    return inches * meters_per_inch


def centimeters_to_meters(centimeters):
    return centimeters / centimeters_per_meter


def degrees_to_radians(degrees):
    return math.radians(degrees)


def radians_to_degrees(radians):
    return math.degrees(radians)


def radians_to_rotations(radians):
    return radians / (math.pi * 2)


def degrees_to_rotations(degrees):
    return degrees / 360


def rotations_to_degrees(rotations):
    return rotations * 360


def rotations_to_radians(rotations):
    return rotations * 2 * math.pi


def rotations_per_minute_to_radians_per_second(rpm):
    return rpm * math.pi / (seconds_per_minute / 2)


def rotations_per_second_to_radians_per_second(rps):
    return rps * math.pi * 2


def rotations_per_minute_to_rotations_per_second(rpm):
    return rpm * seconds_per_minute


def radians_per_second_to_rotations_per_minute(radians_per_second):
    return radians_per_second * (seconds_per_minute / 2) / math.pi


def radians_per_second_to_rotations_per_second(rotations_per_second):
    return rotations_per_second / (2 * math.pi)


def microseconds_to_seconds(microseconds):
    return microseconds / (microseconds_per_millisecond * milliseconds_per_second)


def microseconds_to_milliseconds(microseconds):
    return microseconds / microseconds_per_millisecond


def milliseconds_to_seconds(milliseconds):
    return milliseconds / milliseconds_per_second


def seconds_to_milliseconds(seconds):
    return seconds * milliseconds_per_second


def kilograms_to_pounds(kilograms):
    return kilograms / kilograms_per_pound


def pounds_to_kilograms(lbs):
    return lbs * kilograms_per_pound
