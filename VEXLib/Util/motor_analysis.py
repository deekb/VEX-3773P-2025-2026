from VEXLib.Math import average_iterable
from VEXLib.Math.MathUtil import linspace
from VEXLib.Util import time
from VEXLib.Util.Logging import TimeSeriesLogger
from VEXLib.Motor import Motor
from vex import TorqueUnits, PERCENT, PowerUnits


def collect_power_relationship_data(filename, motor_list: list[Motor], power_range=(-1.0, 1.0), sample_count=100, samples_per_power=10, delay_between_powers_ms=50, delay_between_samples_ms=10):
    """
    Ramp the input power across the power range and collect data about the average speed, torque, power, and efficiency across the motors.
    At each power level, collect multiple samples and report the average.
    """
    logger = TimeSeriesLogger(
        filename,
        ["input_power",
         "speed",
         "torque",
         "efficiency",
         "output_power"]
    )

    for motor in motor_list:
        motor.set(power_range[0])

    time.sleep(1)  # Let motors get to initial speed

    power_values = linspace(power_range[0], power_range[1], sample_count)

    for input_power in power_values:
        print("Applying power: {}".format(input_power))

        for motor in motor_list:
            motor.set(input_power)
        time.sleep_ms(delay_between_powers_ms)

        speed_samples = []
        torque_samples = []
        efficiency_samples = []
        output_power_samples = []

        for _ in range(samples_per_power):
            speed_samples.append(average_iterable([motor.velocity(PERCENT) for motor in motor_list]))
            torque_samples.append(average_iterable([motor.torque(TorqueUnits.NM) for motor in motor_list]))
            efficiency_samples.append(average_iterable([motor.efficiency(PERCENT) for motor in motor_list]))
            output_power_samples.append(average_iterable([motor.power(PowerUnits.WATT) for motor in motor_list]))
            if samples_per_power > 1:
                time.sleep_ms(delay_between_samples_ms)

        logger.write_data({
            "input_power": input_power,
            "speed": average_iterable(speed_samples),
            "torque": average_iterable(torque_samples),
            "efficiency": average_iterable(efficiency_samples),
            "output_power": average_iterable(output_power_samples)
        })

    for motor in motor_list:
        motor.set(0)
