import time
from math import sin, pi, tan

from util.approximate_trigonometric_functions import approximate_sin, approximate_cos, approximate_tan


def measure_execution_time():
    """
    Measure the average time it takes for `approximate_sin` and `math.sin`
    to compute sine values over a range of inputs, using `time.perf_counter_ns`.
    """
    # Local references for faster access
    sin_func = sin
    approx_func = approximate_sin

    # Define range, number of test points, and step for input generation
    test_points = 1000000  # Number of test points
    start = -pi / 2
    end = pi / 2
    step = (end - start) / test_points

    # Measure time for approximate_sin in nanoseconds
    start_time = time.perf_counter_ns()
    for i in range(test_points + 1):
        x = start + i * step
        approx_func(x)
    approx_time_ns = time.perf_counter_ns() - start_time

    # Measure time for math.sin in nanoseconds
    start_time = time.perf_counter_ns()
    for i in range(test_points + 1):
        x = start + i * step
        sin_func(x)
    math_time_ns = time.perf_counter_ns() - start_time

    # Compute average time per input in nanoseconds
    approx_avg_time_ns = approx_time_ns / (test_points + 1)
    math_avg_time_ns = math_time_ns / (test_points + 1)

    # Print timing results
    print("---------- Timing Results ----------")
    print(f"Number of test points: {test_points + 1}")
    print(f"Total time for `approximate_sin`: {approx_time_ns} nanoseconds")
    print(f"Average time per run for `approximate_sin`: {approx_avg_time_ns:.2f} nanoseconds")
    print(f"Total time for `math.sin`: {math_time_ns} nanoseconds")
    print(f"Average time per run for `math.sin`: {math_avg_time_ns:.2f} nanoseconds")


def evaluate_accuracy_with_cosine():
    """
    Evaluate both the accuracy of `approximate_sin(x)` and `approximate_cos(x)`
    by comparing their results against Python's standard `math.sin` and `math.cos`
    implementations, respectively.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from math import sin, cos, pi

    # Define test range and resolution
    start = -2 * pi
    end = 2 * pi
    step = 0.01  # Small step size for high resolution
    test_inputs = np.arange(start, end, step)

    # Store outputs and errors for sine
    approx_sin_outputs = []
    true_sin_outputs = []
    sin_absolute_errors = []
    sin_relative_errors = []

    # Store outputs and errors for cosine
    approx_cos_outputs = []
    true_cos_outputs = []
    cos_absolute_errors = []
    cos_relative_errors = []

    # Store outputs and errors for tan
    approx_tan_outputs = []
    true_tan_outputs = []
    tan_absolute_errors = []
    tan_relative_errors = []

    for x in test_inputs:
        # Sine calculations
        approx_sin = approximate_sin(x)
        true_sin = sin(x)
        approx_sin_outputs.append(approx_sin)
        true_sin_outputs.append(true_sin)
        sin_absolute_errors.append(abs(approx_sin - true_sin))
        sin_relative_errors.append(abs(approx_sin - true_sin) / (abs(true_sin) + 1e-12))  # Avoid division by zero

        # Cosine calculations
        approx_cos = approximate_cos(x)
        true_cos = cos(x)
        approx_cos_outputs.append(approx_cos)
        true_cos_outputs.append(true_cos)
        cos_absolute_errors.append(abs(approx_cos - true_cos))
        cos_relative_errors.append(abs(approx_cos - true_cos) / (abs(true_cos) + 1e-12))  # Avoid division by zero

        # Cosine calculations
        approx_tan = approximate_tan(x)
        true_tan = tan(x)
        approx_tan_outputs.append(approx_tan)
        true_tan_outputs.append(true_tan)
        tan_absolute_errors.append(abs(approx_tan - true_tan))
        tan_relative_errors.append(abs(approx_tan - true_tan) / (abs(true_tan) + 1e-12))  # Avoid division by zero

    # Convert errors to numpy arrays for easier analysis
    sin_absolute_errors = np.array(sin_absolute_errors)
    sin_relative_errors = np.array(sin_relative_errors)
    cos_absolute_errors = np.array(cos_absolute_errors)
    cos_relative_errors = np.array(cos_relative_errors)
    tan_absolute_errors = np.array(cos_absolute_errors)
    tan_relative_errors = np.array(cos_relative_errors)

    # Sine error statistics
    sin_max_abs_error = np.max(sin_absolute_errors)
    sin_avg_abs_error = np.mean(sin_absolute_errors)
    sin_max_rel_error = np.max(sin_relative_errors)
    sin_avg_rel_error = np.mean(sin_relative_errors)

    # Cosine error statistics
    cos_max_abs_error = np.max(cos_absolute_errors)
    cos_avg_abs_error = np.mean(cos_absolute_errors)
    cos_max_rel_error = np.max(cos_relative_errors)
    cos_avg_rel_error = np.mean(cos_relative_errors)

    # Tangent error statistics
    tan_max_abs_error = np.max(tan_absolute_errors)
    tan_avg_abs_error = np.mean(tan_absolute_errors)
    tan_max_rel_error = np.max(tan_relative_errors)
    tan_avg_rel_error = np.mean(tan_relative_errors)

    # Print sine and cosine error metrics
    print("---------- Accuracy Evaluation for Sine ----------")
    print(f"Maximum absolute error (sin): {sin_max_abs_error:.8f}")
    print(f"Average absolute error (sin): {sin_avg_abs_error:.8f}")
    print(f"Maximum relative error (sin): {sin_max_rel_error:.8f}")
    print(f"Average relative error (sin): {sin_avg_rel_error:.8f}")

    print("\n---------- Accuracy Evaluation for Cosine ----------")
    print(f"Maximum absolute error (cos): {cos_max_abs_error:.8f}")
    print(f"Average absolute error (cos): {cos_avg_abs_error:.8f}")
    print(f"Maximum relative error (cos): {cos_max_rel_error:.8f}")
    print(f"Average relative error (cos): {cos_avg_rel_error:.8f}")

    print("\n---------- Accuracy Evaluation for Tangent ----------")
    print(f"Maximum absolute error (tan): {tan_max_abs_error:.8f}")
    print(f"Average absolute error (tan): {tan_avg_abs_error:.8f}")
    print(f"Maximum relative error (tan): {tan_max_rel_error:.8f}")
    print(f"Average relative error (tan): {tan_avg_rel_error:.8f}")

    # Plot results
    plt.figure(figsize=(20, 20))

    # Sine: Outputs comparison
    plt.subplot(6, 1, 1)
    plt.plot(test_inputs, true_sin_outputs, label="math.sin(x)", color="green", linestyle="dashed")
    plt.plot(test_inputs, approx_sin_outputs, label="approximate_sin(x)", color="orange")
    plt.title("Sine Outputs Comparison")
    plt.xlabel("Input (x)")
    plt.ylabel("Output (sin)")
    plt.legend()
    plt.grid(True)

    # Cosine: Outputs comparison
    plt.subplot(6, 1, 2)
    plt.plot(test_inputs, true_cos_outputs, label="math.cos(x)", color="blue", linestyle="dashed")
    plt.plot(test_inputs, approx_cos_outputs, label="approximate_cos(x)", color="red")
    plt.title("Cosine Outputs Comparison")
    plt.xlabel("Input (x)")
    plt.ylabel("Output (cos)")
    plt.legend()
    plt.grid(True)

    # Tangent: Outputs comparison
    plt.subplot(6, 1, 3)
    plt.plot(test_inputs, true_tan_outputs, label="math.tan(x)", color="blue", linestyle="dashed")
    plt.plot(test_inputs, approx_tan_outputs, label="approximate_tan(x)", color="purple")
    plt.title("Tangent Outputs Comparison")
    plt.xlabel("Input (x)")
    plt.ylabel("Output (tan)")
    plt.ylim(-pi, pi)
    plt.legend()
    plt.grid(True)

    # Sine: Absolute Error
    plt.subplot(6, 1, 4)
    plt.plot(test_inputs, sin_absolute_errors, label="Sine Absolute Error", color="blue")
    plt.title("Sine Absolute Error")
    plt.xlabel("Input (x)")
    plt.ylabel("Absolute Error")
    plt.grid(True)
    plt.legend()

    # Cosine: Absolute Error
    plt.subplot(6, 1, 5)
    plt.plot(test_inputs, cos_absolute_errors, label="Cosine Absolute Error", color="red")
    plt.title("Cosine Absolute Error")
    plt.xlabel("Input (x)")
    plt.ylabel("Absolute Error")
    plt.grid(True)
    plt.legend()

    # Tangent: Absolute Error
    plt.subplot(6, 1, 6)
    plt.plot(test_inputs, tan_absolute_errors, label="Tangent Absolute Error", color="green")
    plt.title("Tangent Absolute Error")
    plt.xlabel("Input (x)")
    plt.ylabel("Absolute Error")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print(approximate_tan(1))
    # Run the timing and accuracy evaluations
    # try:
    print("Running timing evaluation...\n")
    measure_execution_time()

    print("\nRunning accuracy evaluation...\n")
    evaluate_accuracy_with_cosine()
    # except Exception as e:
    #     print(f"Test failed: {e}")
