from math import sqrt


class Constraints:
    max_velocity: float
    max_acceleration: float

    def __init__(self, max_velocity, max_acceleration):
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration


class State:
    position: float
    velocity: float

    def __init__(self, position=0.0, velocity=0.0):
        self.position = position
        self.velocity = velocity

    def __repr__(self):
        return "State(position=" + str(self.position) + ", velocity=" + str(self.velocity) + ")"


class TrapezoidProfile:
    def __init__(self, constraints):
        self.constraints = constraints
        self.new_api = True
        self.direction = 1
        self.current = State()
        self.goal = State()
        self.end_acceleration = 0.0
        self.end_full_speed = 0.0
        self.end_deceleration = 0.0

    @staticmethod
    def should_flip_acceleration(initial, goal):
        return initial.position > goal.position

    def _direct(self, inp):
        result = State(inp.position, inp.velocity)
        result.position *= self.direction
        result.velocity *= self.direction
        return result

    def calculate(self, t, initial_state, goal_state):
        self.direction = -1 if self.should_flip_acceleration(initial_state, goal_state) else 1
        self.current = self._direct(initial_state)
        goal_state = self._direct(goal_state)

        if self.current.velocity > self.constraints.max_velocity:
            self.current.velocity = self.constraints.max_velocity

        cutoff_begin = self.current.velocity / self.constraints.max_acceleration
        cutoff_distance_begin = (cutoff_begin**2 * self.constraints.max_acceleration) / 2.0

        cutoff_end = goal_state.velocity / self.constraints.max_acceleration
        cutoff_distance_end = (cutoff_end**2 * self.constraints.max_acceleration) / 2.0

        full_trapezoid_distance = (
                cutoff_distance_begin + (goal_state.position - self.current.position) + cutoff_distance_end
        )
        acceleration_time = self.constraints.max_velocity / self.constraints.max_acceleration

        full_speed_distance = full_trapezoid_distance - (acceleration_time**2 * self.constraints.max_acceleration)

        if full_speed_distance < 0:
            acceleration_time = sqrt(full_trapezoid_distance / self.constraints.max_acceleration)
            full_speed_distance = 0

        self.end_acceleration = acceleration_time - cutoff_begin
        self.end_full_speed = self.end_acceleration + full_speed_distance / self.constraints.max_velocity
        self.end_deceleration = self.end_full_speed + acceleration_time - cutoff_end
        result = State(self.current.position, self.current.velocity)

        if t < self.end_acceleration:
            result.velocity += t * self.constraints.max_acceleration
            result.position += (self.current.velocity + t * self.constraints.max_acceleration / 2.0) * t
        elif t < self.end_full_speed:
            result.velocity = self.constraints.max_velocity
            result.position += (
                (self.current.velocity + self.end_acceleration * self.constraints.max_acceleration / 2.0) * self.end_acceleration +
                self.constraints.max_velocity * (t - self.end_acceleration)
            )
        elif t <= self.end_deceleration:
            result.velocity = goal_state.velocity + (self.end_deceleration - t) * self.constraints.max_acceleration
            time_left = self.end_deceleration - t
            result.position = (
                    goal_state.position - ((goal_state.velocity + time_left * self.constraints.max_acceleration / 2.0) * time_left)
            )
        else:
            result = goal_state

        return self._direct(result)

    def time_left_until(self, target):
        position = self.current.position * self.direction
        velocity = self.current.velocity * self.direction

        end_acceleration = self.end_acceleration * self.direction
        end_full_speed = self.end_full_speed * self.direction - end_acceleration

        if target < position:
            end_acceleration = -end_acceleration
            end_full_speed = -end_full_speed
            velocity = -velocity

        end_acceleration = max(end_acceleration, 0)
        end_full_speed = max(end_full_speed, 0)

        acceleration = self.constraints.max_acceleration
        deceleration = -self.constraints.max_acceleration

        distance_to_target = abs(target - position)
        if distance_to_target < 1e-6:
            return 0

        acceleration_distance = velocity * end_acceleration + 0.5 * acceleration * end_acceleration**2

        deceleration_velocity = sqrt(abs(velocity**2 + 2 * acceleration * acceleration_distance)) if end_acceleration > 0 else velocity

        full_speed_distance = self.constraints.max_velocity * end_full_speed
        deceleration_distance = distance_to_target - full_speed_distance - acceleration_distance

        acceleration_time = (-velocity + sqrt(abs(velocity**2 + 2 * acceleration * acceleration_distance))) / acceleration

        deceleration_time = (-deceleration_velocity + sqrt(abs(deceleration_velocity**2 + 2 * deceleration * deceleration_distance))) / deceleration

        full_speed_time = full_speed_distance / self.constraints.max_velocity

        return acceleration_time + full_speed_time + deceleration_time

    def total_time(self):
        return self.end_deceleration

    def is_finished(self, t):
        return t >= self.total_time()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    # Constants
    max_velocity = 0.4  # m/s
    max_acceleration = 0.05  # m/s^2

    # Create TrapezoidProfile
    constraints = Constraints(max_velocity, max_acceleration)
    initial_state = State(0.0, 0)
    goal_state = State(10, -1)
    profile = TrapezoidProfile(constraints)

    profile.calculate(0, initial_state, goal_state)

    # Calculate total time for the profile
    total_time = profile.total_time()

    # Simulate the profile
    dt = 0.01
    simulation_time = np.arange(0.0, total_time, dt)

    positions = []
    velocities = []

    for t in simulation_time:
        state = profile.calculate(t, initial_state, goal_state)
        positions.append(state.position)
        velocities.append(state.velocity)

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.plot(simulation_time, positions, label="Position")
    plt.title("Trapezoid Profile Simulation")
    plt.ylabel("Position (m)")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(simulation_time, velocities, label="Velocity")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()

    plt.tight_layout()
    plt.show()
