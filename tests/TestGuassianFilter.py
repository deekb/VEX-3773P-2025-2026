import unittest
import math
import random
import matplotlib.pyplot as plt
from VEXLib.Algorithms.GuassianFilter import RealTimeGaussianSmoother, create_gaussian_kernel


def generate_triangle_wave(length=200, period=50, amplitude=1, noise_level=0.1):
    """
    Generates a noisy triangle wave.
    :param length: Number of data points
    :param period: Length of one complete up-down cycle
    :param amplitude: Peak value of the wave
    :param noise_level: Random noise added to simulate real-world data
    :return: List of values representing the noisy triangle wave
    """
    wave = [(2 * amplitude / period) * (i % period) if (i // period) % 2 == 0
            else (2 * amplitude - (2 * amplitude / period) * (i % period))
            for i in range(length)]

    # Add random noise
    wave = [x + random.uniform(-noise_level, noise_level) for x in wave]
    return wave


class TestRealTimeGaussianSmoother(unittest.TestCase):
    def test_initialization(self):
        smoother = RealTimeGaussianSmoother(sigma=1.0, kernel_size=3)
        self.assertEqual(smoother.sigma, 1.0)
        self.assertEqual(smoother.kernel_size, 3)
        self.assertEqual(len(smoother.kernel), 3)
        self.assertEqual(len(smoother.buffer), 3)

    def test_smooth_with_constant_input(self):
        smoother = RealTimeGaussianSmoother(sigma=1.0, kernel_size=3)
        for _ in range(10):
            result = smoother.smooth(1.0)
        self.assertAlmostEqual(result, 1.0, places=5)

    def test_smooth_with_varying_input(self):
        smoother = RealTimeGaussianSmoother(sigma=1.0, kernel_size=3)
        inputs = [0.0, 1.0, 2.0, 3.0]
        expected_outputs = [0.0, 0.274068619061197, 1.0, 2.0]
        for i, input_value in enumerate(inputs):
            result = smoother.smooth(input_value)
            self.assertAlmostEqual(result, expected_outputs[i], places=5)

    def test_smooth_with_edge_case(self):
        smoother = RealTimeGaussianSmoother(sigma=1.0, kernel_size=3)
        result = smoother.smooth(0.0)
        self.assertAlmostEqual(result, 0.0, places=5)

    def test_create_gaussian_kernel(self):
        kernel = create_gaussian_kernel(sigma=1.0, kernel_size=3)
        self.assertAlmostEqual(sum(kernel), 1.0, places=5)
        expected_kernel = [0.274068619061197, 0.45186276187760605, 0.274068619061197]
        for i in range(len(kernel)):
            self.assertAlmostEqual(kernel[i], expected_kernel[i], places=5)
        self.assertEqual(kernel, list(reversed(kernel)))

    def test_visual_check(self):
        # Initialize the Gaussian Smoother
        smoother = RealTimeGaussianSmoother(sigma=2, kernel_size=15)

        # Generate random data to simulate input
        raw_data = [math.sin((i / 100) * math.pi) + random.uniform(-0.1, 0.1) for i in range(200)]
        raw_data = [1 if 50 <= i < 150 else 0 for i in range(100)] + [i for i in range(100)]
        raw_data = generate_triangle_wave()
        smoothed_data = []

        # Smooth the data using the smoother
        for point in raw_data:
            smoothed_data.append(smoother.smooth(point))

        # Plot the raw and smoothed data
        plt.figure(figsize=(10, 8))
        plt.plot(raw_data, label='Raw Data')
        plt.plot(smoothed_data, label='Smoothed Data')
        plt.title("Gaussian Smoothing Visual Test")
        plt.xlabel("Time Steps")
        plt.ylabel("Value")
        plt.legend()
        plt.show()


class TestCreateGaussianKernel(unittest.TestCase):
    def test_kernel_sum(self):
        kernel = create_gaussian_kernel(sigma=1.0, kernel_size=3)
        self.assertAlmostEqual(sum(kernel), 1.0, places=5)

    def test_kernel_values(self):
        kernel = create_gaussian_kernel(sigma=1.0, kernel_size=3)
        expected_kernel = [0.274068619061197, 0.45186276187760605, 0.274068619061197]
        for i in range(len(kernel)):
            self.assertAlmostEqual(kernel[i], expected_kernel[i], places=5)

    def test_kernel_symmetry(self):
        kernel = create_gaussian_kernel(sigma=1.0, kernel_size=3)
        self.assertEqual(kernel, kernel[::-1])


if __name__ == '__main__':
    unittest.main()