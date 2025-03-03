import json

from VEXLib.Math import MathUtil
from VEXLib.Util import time
from vex import TorqueUnits, PERCENT, PowerUnits


def collect_power_relationship_data(motor_list, step_delay=0.25, power_step=0.005, max_power=1.0):
    """
    Ramp the input power from 0 to the maximum power and collect data about average torque, power, and efficiency across the motors.

    Args:
        motor_list: A list of motors to run and average
        step_delay: Time (in seconds) to wait between each power step.
        power_step: Incremental power step (-1 to 1).
        max_power: Maximum allowable duty cycle -1 to 1.

    Returns:
        data: A JSON string with input power and average torque, speed, output power, and efficiency data.
    """
    data = {
        "input_power": [],
        "torque": [],
        "speed": [],
        "output_power": [],
        "efficiency": []
    }

    print("Starting power ramp and data collection...")

    for input_power in [i * power_step for i in range(int(max_power / power_step) + 1)]:
        # Apply power to all motors
        for motor in motor_list:
            motor.set(input_power)

        torques = speeds = output_powers = efficiencies = []

        # Wait for the drivetrain to respond
        time.sleep(step_delay)
        for _ in range(10):
            torques.extend([motor.torque(TorqueUnits.NM) for motor in motor_list])
            speeds.extend([motor.velocity(PERCENT) for motor in motor_list])
            output_powers.extend([motor.power(PowerUnits.WATT) for motor in motor_list])
            efficiencies.extend([motor.efficiency(PERCENT) for motor in motor_list])
            time.sleep(0.1)

        average_torque = MathUtil.average_iterable(torques)
        average_speed = MathUtil.average_iterable(speeds)
        average_output_power = MathUtil.average_iterable(output_powers)
        average_efficiency = MathUtil.average_iterable(efficiencies)

        # Append data to the lists
        data["input_power"].append(input_power)
        data["torque"].append(average_torque)
        data["speed"].append(average_speed)
        data["output_power"].append(average_output_power)
        data["efficiency"].append(average_efficiency)

        print(
            "Input Power: {:.2f}, Speed: {:.2f}%, Torque: {:.2f}Nm, Output Power: {:.2f}W, Efficiency: {:.2f}%".format(
                input_power,
                average_speed,
                average_torque,
                average_output_power,
                average_efficiency))

    # Stop the motor group
    for motor in motor_list:
        motor.set(0.0)

    # Serialize data in JSON format
    json_data = json.dumps(data)
    return json_data
