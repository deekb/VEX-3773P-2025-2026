# Function to create a 1D Gaussian kernel
import math


def create_gaussian_kernel(sigma, kernel_size):
    kernel = []
    sum_val = 0
    half_size = (kernel_size - 1) / 2
    for i in range(kernel_size):
        x = i - half_size
        g = math.exp(-0.5 * (x / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))
        kernel.append(g)
        sum_val += g

    # Normalize the kernel so that its sum is 1
    return [val / sum_val for val in kernel]


class RealTimeGaussianSmoother:
    def __init__(self, sigma: float, kernel_size: int):
        self.kernel_size = kernel_size
        self.sigma = sigma
        self.kernel = create_gaussian_kernel(sigma, kernel_size)
        self.buffer = [0] * kernel_size
        self.index = 0

    def smooth(self, new_data_point):
        # Update buffer with new data point
        self.buffer[self.index] = new_data_point
        self.index = (self.index + 1) % self.kernel_size  # Move index in a circular manner

        # Apply Gaussian smoothing
        smoothed_value = 0
        for i in range(self.kernel_size):
            buffer_index = (self.index + i) % self.kernel_size
            smoothed_value += self.buffer[buffer_index] * self.kernel[i]

        return smoothed_value
