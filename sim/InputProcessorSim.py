import matplotlib.pyplot as plt

from VEXLib.Math import apply_deadband, cubic_filter
from VEXLib.Sensors.Controller import InputProcessor


class GraphedInputProcessor(InputProcessor):
    def __init__(self):
        """
        Initialize the input processor with an empty pipeline.
        """
        super().__init__()

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
        plt.figure(figsize=(7, 7))
        for i, outputs in enumerate(intermediate_outputs):
            plt.plot(input_values, outputs, label=f"Step {i}" if i > 0 else "Input")

        plt.xlabel("Input Value")
        plt.ylabel("Output Value")
        plt.title("Pipeline Visualization")
        plt.legend()
        plt.grid(True)
        plt.gca().set_aspect('equal', adjustable='box')  # Force square aspect ratio
        plt.show()


# Initialize an InputProcessor
processor = GraphedInputProcessor()

# Add processing steps
processor.add_step(lambda x: cubic_filter(x, 0))
processor.add_step(lambda x: apply_deadband(x, 0.05, 1))


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


# Generate a range of input values (-1.0 to 1.0)
input_values = [x / 100 for x in range(-100, 101)]

# Visualize the pipeline
processor.visualize_pipeline(input_values)
