from VEXLib.Util import time
from VEXLib.Util.Logging import TimeSeriesLogger
from vex import TorqueUnits, PERCENT, PowerUnits


def get_motor_data(motor):
    """
    Get data from the motor.

    Args:
        motor: The motor to get data from.

    Returns:
        A dictionary containing torque, speed, output power, and efficiency of the motor.
    """
    return {
        "time (s)": time.time(),
        "torque (Nm)": motor.torque(TorqueUnits.NM),
        "speed (% of rated)": motor.velocity(PERCENT),
        "output_power (W)": motor.power(PowerUnits.WATT),
        "efficiency (%)": motor.efficiency(PERCENT)
    }


def collect_power_relationship_data(filename, motor_list, step_delay=0.05, power_step=0.05, max_power=1.0, data_collection_interval=0, data_points_per_step=1, speed_function=lambda motor: motor.velocity(PERCENT), speed_unit="% of rated"):
    """
    Ramp the input power from 0 to the maximum power and collect data about average torque, power, and efficiency across the motors.

    Args:
        filename: The name of the file to log data.
        motor_list: A list of motors to run and average.
        step_delay: Time (in seconds) to wait between each power step.
        power_step: Incremental power step (0 to max_power).
        max_power: Maximum allowable duty cycle (0 to 1).
        speed_function: The function to get the speed of the motor.
        data_collection_interval: Time (in seconds) between data collections.
        data_points_per_step: Number of data points to collect per power step.
    """
    logger = TimeSeriesLogger(filename, list(get_motor_data(motor_list[0]).keys()) + ["input_power (% of rated)"])

    for motor in motor_list:
        motor.set(0)

    print("Starting power ramp and data collection...")

    for input_power in [i * power_step for i in range(int(max_power / power_step) + 1)]:
        print("Applying power: {}".format(input_power))
        # Apply power to all motors
        for motor in motor_list:
            motor.set(input_power)

        # Wait for the drivetrain to respond
        time.sleep(step_delay)
        for _ in range(data_points_per_step):
            aggregated_data = {
                "time (s)": 0,
                "torque (Nm)": 0,
                "speed (% of rated)": 0,
                "output_power (W)": 0,
                "efficiency (%)": 0,
                "input_power (% of rated)": input_power * 100
            }
            for motor in motor_list:
                data = get_motor_data(motor)
                aggregated_data["time (s)"] += data["time (s)"]
                aggregated_data["torque (Nm)"] += data["torque (Nm)"]
                aggregated_data["speed (% of rated)"] += data["speed (% of rated)"]
                aggregated_data["output_power (W)"] += data["output_power (W)"]
                aggregated_data["efficiency (%)"] += data["efficiency (%)"]
                aggregated_data["speed ({})".format(speed_unit)] = speed_function(motor)

            # Average the data
            for key in aggregated_data:
                if key != "input_power (% of rated)":
                    aggregated_data[key] /= len(motor_list)

            logger.write_data(aggregated_data)
            time.sleep(data_collection_interval)

    # Stop the motor group
    for motor in motor_list:
        motor.set(0.0)
