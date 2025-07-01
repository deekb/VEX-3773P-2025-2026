import math
import random

import matplotlib.pyplot as plt


def pad_to_power_of_2(signal):
    """Pads the signal to the next power of 2 with zeros if necessary."""
    n = len(signal)
    target_size = 1 << (n - 1).bit_length()  # Next power of 2
    return signal + [0] * (target_size - n)


def fft(signal):
    """
    Compute the Fast Fourier Transform (FFT) using the Cooley-Tukey algorithm.
    Works for any input length by padding to the next power of 2.

    :param signal: List of real or complex numbers representing the input signal.
    :return: List of complex numbers representing the frequency domain of the signal.
    """
    n = len(signal)
    if n <= 1:
        return signal

    if not (n & (n - 1)) == 0:  # If not a power of 2, pad it
        signal = pad_to_power_of_2(signal)
        n = len(signal)

    even_fft = fft(signal[0::2])
    odd_fft = fft(signal[1::2])

    result = [0] * n
    for k in range(n // 2):
        t = (
            complex(math.cos(-2 * math.pi * k / n), math.sin(-2 * math.pi * k / n))
            * odd_fft[k]
        )
        result[k] = even_fft[k] + t
        result[k + n // 2] = even_fft[k] - t

    return result


def ifft(freq_data):
    """
    Compute the Inverse Fast Fourier Transform (IFFT).
    :param freq_data: List of complex numbers representing the frequency spectrum.
    :return: List of real numbers representing the reconstructed time-domain signal.
    """
    n = len(freq_data)
    if n <= 1:
        return freq_data

    even_ifft = ifft(freq_data[0::2])
    odd_ifft = ifft(freq_data[1::2])

    result = [0] * n
    for k in range(n // 2):
        t = (
            complex(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n))
            * odd_ifft[k]
        )
        result[k] = (even_ifft[k] + t) / 2  # Normalize
        result[k + n // 2] = (even_ifft[k] - t) / 2  # Normalize

    return result


def notch_filter(fft_data, sample_rate, notch_freq, bandwidth=1):
    """
    Apply a notch filter to remove a specific frequency (e.g., 50 Hz) and its surrounding frequencies.

    :param fft_data: List of complex numbers (FFT output).
    :param sample_rate: Sampling rate of the signal in Hz.
    :param notch_freq: Frequency to filter out (e.g., 50 Hz).
    :param bandwidth: Width of the notch around the notch_freq (default is 1 Hz).
    :return: Filtered FFT data.
    """
    n = len(fft_data)
    freq_resolution = sample_rate / n  # Frequency resolution per bin

    # Find the index corresponding to the notch frequency
    notch_index = int(notch_freq / freq_resolution)

    # Remove frequencies within the bandwidth range of the notch
    for i in range(n):
        freq = i * freq_resolution
        # If the frequency is within the notch range, zero it out
        if (
            abs(freq - notch_freq) < bandwidth
            or abs(freq - (sample_rate - notch_freq)) < bandwidth
        ):
            fft_data[i] = 0  # Remove the frequency component

    return fft_data


# Generate signal with 50 Hz noise
sample_rate = 500  # Hz
signal_length = 500  # Samples


# Simulating a signal with 50 Hz noise
def generate_signal_with_50hz_noise(length=100, sample_rate=100):
    return [
        math.sin(2 * math.pi * 5 * t / sample_rate)  # 5 Hz component
        + 0.1 * math.sin(2 * math.pi * 20 * t / sample_rate)  # 20 Hz component
        + 0.4 * math.sin(2 * math.pi * 50 * t / sample_rate)  # 50 Hz noise
        + 0.2 * (random.uniform(-1, 1))  # Random noise
        for t in range(length)
    ]


# Generate signal
signal = generate_signal_with_50hz_noise(length=signal_length, sample_rate=sample_rate)

# Compute FFT
fft_result = fft(signal)

# Apply Notch Filter to remove 50 Hz noise
notch_filtered_fft = notch_filter(
    fft_result[:], sample_rate, notch_freq=140, bandwidth=130
)

# Compute IFFT to reconstruct the filtered signal
filtered_signal = ifft(notch_filtered_fft)

# Trim filtered signal to the original signal length (avoid padding artifacts)
filtered_signal = filtered_signal[:signal_length]

# Compute frequency bins
n = len(fft_result)
frequencies = [i * sample_rate / n for i in range(n // 2)]

# Compute magnitude spectrum before and after filtering
magnitude_before = [abs(fft_result[i]) for i in range(n // 2)]
magnitude_after = [abs(notch_filtered_fft[i]) for i in range(n // 2)]

# Plot results
plt.figure(figsize=(16, 6))

# Time-domain signal
plt.subplot(2, 3, 1)
plt.plot(signal, label="Original Signal")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.title("Original Signal (Time Domain)")
plt.legend()

# Time-domain filtered signal
plt.subplot(2, 3, 2)
plt.plot(filtered_signal, label="Filtered Signal", color="red")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.title("Filtered Signal (Time Domain)")
plt.legend()

# Frequency spectrum before filtering
plt.subplot(2, 3, 4)
plt.plot(frequencies, magnitude_before, label="Original Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("FFT Spectrum (Before Filtering)")
plt.legend()

# Frequency spectrum after filtering
plt.subplot(2, 3, 5)
plt.plot(frequencies, magnitude_after, label="Filtered Spectrum", color="red")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("FFT Spectrum (After Filtering)")
plt.legend()

# Overlay: Original and Filtered signals in the rightmost column (Time Domain)
plt.subplot(2, 3, 3)
plt.plot(signal, label="Original Signal", color="blue", alpha=0.7)
plt.plot(filtered_signal, label="Filtered Signal", color="red", linestyle="--")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.title("Original vs Filtered Signal (Overlay)")
plt.legend()

# Overlay: Original and Filtered frequency spectra in the rightmost column (Frequency Domain)
plt.subplot(2, 3, 6)
plt.plot(
    frequencies, magnitude_before, label="Original Spectrum", color="blue", alpha=0.7
)
plt.plot(
    frequencies, magnitude_after, label="Filtered Spectrum", color="red", linestyle="--"
)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Original vs Filtered Spectrum (Overlay)")
plt.legend()

plt.tight_layout()
plt.show()
