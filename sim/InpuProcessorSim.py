import matplotlib.pyplot as plt

from VEXLib.Math import apply_deadband


class InputProcessor:
    def __init__(self):
        """
        Initialize the input processor with an empty pipeline.
        """
        self.pipeline = []

    def add_step(self, function):
        """
        Add a processing step to the pipeline.
        :param function: A callable function that takes input and returns processed output.
        """
        self.pipeline.append(function)

    def process(self, input_value):
        """
        Process the input through the pipeline.
        :param input_value: The initial input value to process.
        :return: The processed output.
        """
        for step in self.pipeline:
            input_value = step(input_value)
        return input_value

    def visualize_pipeline(self, input_values):
        """
        Visualize the effect of the pipeline on a range of input values.
        :param input_values: A list of input values to process.
        """
        intermediate_outputs = [input_values]
        current_values = input_values

        for step in self.pipeline:
            # Apply the current step to all values
            current_values = [step(value) for value in current_values]
            intermediate_outputs.append(current_values)

        # Plot the transformations
        plt.figure(figsize=(10, 6))
        for i, outputs in enumerate(intermediate_outputs):
            plt.plot(input_values, outputs, label=f"Step {i}" if i > 0 else "Input")

        plt.xlabel("Input Value")
        plt.ylabel("Output Value")
        plt.title("Pipeline Visualization")
        plt.legend()
        plt.grid(True)
        plt.show()


# Initialize an InputProcessor
processor = InputProcessor()

# Add Deadbanding
processor.add_step(lambda x: apply_deadband(x, 0.1, 1))

# Add Cubic Filtering
processor.add_step(lambda x: x ** 3)


# Add Slew Rate Limiting
class SlewRateLimiter:
    def __init__(self, max_slew_rate=0.05):
        self.previous_value = 0
        self.max_slew_rate = max_slew_rate

    def limit(self, current_value):
        delta = current_value - self.previous_value
        if abs(delta) > self.max_slew_rate:
            delta = self.max_slew_rate * (1 if delta > 0 else -1)
        self.previous_value += delta
        return self.previous_value


slew_limiter = SlewRateLimiter(max_slew_rate=0.2)
processor.add_step(slew_limiter.limit)

# Generate a range of input values (-1.0 to 1.0)
input_values = [x / 100 for x in range(-100, 101)]

# Visualize the pipeline
processor.visualize_pipeline(input_values)
