def desaturate_wheel_speeds(speeds):
    maximum_power = max(*speeds)

    if maximum_power > 1:
        # At least one of the motor velocities are over the maximum possible velocity
        # This will result in clipping, meaning that the motor speeds will be "clipped" off to the maximum (1)
        # We will lose some control of our turning while we are moving quickly
        # To solve this issue we can detect if any motor velocities exceed the maximum possible velocity and
        # Use the inverse of the maximum motor power as a scalar by dividing by it.
        # This will always output all values in a range from 0-1
        speeds = [speed / maximum_power for speed in speeds]
    return speeds