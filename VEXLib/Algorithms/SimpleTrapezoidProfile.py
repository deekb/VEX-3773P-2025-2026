import math
import matplotlib.pyplot as plt


def generate_trapezoid_profile(max_v, time_to_max_v, dt, goal, disable_start_acceleration=False,
                               disable_end_acceleration=False):
    """Creates a trapezoid profile with the given constraints.

    Returns:
        t_rec -- list of timestamps
        x_rec -- list of positions at each timestep
        v_rec -- list of velocities at each timestep
        a_rec -- list of accelerations at each timestep

    Keyword arguments:
        max_v -- maximum velocity of profile
        time_to_max_v -- time from rest to maximum velocity
        dt -- timestep
        goal -- final position when the profile is at rest
        disable_start_acceleration -- if True, disables the start acceleration
        disable_end_acceleration -- if True, disables the end acceleration
    """

    t_rec = [0.0]
    x_rec = [0.0]
    v_rec = [0.0]
    a_rec = [0.0]
    a = max_v / time_to_max_v
    time_at_max_v = goal / max_v - time_to_max_v

    # If profile is short
    if max_v * time_to_max_v > goal:
        time_to_max_v = math.sqrt(goal / a)
        time_from_max_v = time_to_max_v
        time_total = 2.0 * time_to_max_v
        profile_max_v = a * time_to_max_v
    else:
        time_from_max_v = time_to_max_v + time_at_max_v
        time_total = time_from_max_v + time_to_max_v
        profile_max_v = max_v

    while t_rec[-1] < time_total:
        t = t_rec[-1] + dt
        t_rec.append(t)
        if t < time_to_max_v and not disable_start_acceleration:
            # Accelerate up
            a_rec.append(a)
            v_rec.append(a * t)
        elif t < time_from_max_v:
            # Maintain max velocity
            a_rec.append(0.0)
            v_rec.append(profile_max_v)
        elif t < time_total and not disable_end_acceleration:
            # Accelerate down
            decel_time = t - time_from_max_v
            a_rec.append(-a)
            v_rec.append(profile_max_v - a * decel_time)
        else:
            a_rec.append(0.0)
            v_rec.append(0.0)
        x_rec.append(x_rec[-1] + v_rec[-1] * dt)

    return t_rec, x_rec, v_rec, a_rec


# Parameters
max_v = 2.0
time_to_max_v = 1.0
dt = 0.01
goal = 10.0

# Generate profile with start acceleration disabled
t_rec, x_rec, v_rec, a_rec = generate_trapezoid_profile(max_v, time_to_max_v, dt, goal, disable_start_acceleration=True)

# Plotting
plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(t_rec, x_rec, label='Position')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t_rec, v_rec, label='Velocity', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(t_rec, a_rec, label='Acceleration', color='green')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s²)')
plt.legend()

plt.tight_layout()
plt.show()
