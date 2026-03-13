"""
A lightweight FFT module implementing:
- Cooley-Tukey FFT (recursive)
- Inverse FFT
- Notch filtering in the frequency domain
- Signal generation utilities
- Relies only on builtin math library
- Optional demo visualization

Author: Derek Baier
"""

import math


# ============================================================
# Core FFT Utilities
# ============================================================

def pad_to_power_of_2(signal):
    """
    Pad a signal to the next power of 2 using zeros.

    :param signal: Input signal (real or complex values)
    :return: Zero-padded signal
    """
    n = len(signal)
    if n == 0:
        return []

    target_size = 1 << (n - 1).bit_length()
    return list(signal) + [0] * (target_size - n)


def fft(signal):
    """
    Compute the Fast Fourier Transform using the recursive
    Cooley-Tukey radix-2 algorithm.

    Automatically pads input to next power of 2 if needed.

    :param signal: Real or complex time-domain signal
    :return: Frequency-domain representation (complex list)
    """
    n = len(signal)

    if n <= 1:
        return list(signal)

    if (n & (n - 1)) != 0:
        signal = pad_to_power_of_2(signal)
        n = len(signal)

    even_fft = fft(signal[0::2])
    odd_fft = fft(signal[1::2])

    result = [0j] * n
    for k in range(n // 2):
        twiddle = complex(
            math.cos(-2 * math.pi * k / n),
            math.sin(-2 * math.pi * k / n),
        )
        t = twiddle * odd_fft[k]
        result[k] = even_fft[k] + t
        result[k + n // 2] = even_fft[k] - t

    return result


def ifft(freq_data):
    """
    Compute the Inverse Fast Fourier Transform.

    :param freq_data: Frequency-domain data
    :return: Reconstructed time-domain signal
    """
    n = len(freq_data)

    if n <= 1:
        return list(freq_data)

    even_ifft = ifft(freq_data[0::2])
    odd_ifft = ifft(freq_data[1::2])

    result = [0j] * n
    for k in range(n // 2):
        twiddle = complex(
            math.cos(2 * math.pi * k / n),
            math.sin(2 * math.pi * k / n),
        )
        t = twiddle * odd_ifft[k]

        result[k] = (even_ifft[k] + t) / 2
        result[k + n // 2] = (even_ifft[k] - t) / 2

    return result


# ============================================================
# Filtering
# ============================================================

def notch_filter(
    fft_data,
    sample_rate: float,
    notch_freq: float,
    bandwidth: float = 1.0,
):
    """
    Apply a notch filter to remove a specific frequency and
    its mirrored component.

    :param fft_data: FFT output
    :param sample_rate: Sampling rate in Hz
    :param notch_freq: Frequency to remove
    :param bandwidth: Width of frequency band to remove
    :return: Filtered FFT data
    """
    n = len(fft_data)
    freq_resolution = sample_rate / n

    for i in range(n):
        freq = i * freq_resolution

        if (
            abs(freq - notch_freq) < bandwidth
            or abs(freq - (sample_rate - notch_freq)) < bandwidth
        ):
            fft_data[i] = 0j

    return fft_data


# ============================================================
# Demo / Visualization
# ============================================================

def demo(
    sample_rate: int = 500,
    signal_length: int = 500,
    notch_freq: float = 140.0,
    bandwidth: float = 130.0,
) -> None:
    """
    Run a demonstration of FFT, notch filtering,
    and visualization using matplotlib.
    """
    import matplotlib.pyplot as plt
    import random

    def generate_signal_with_50hz_noise(
        length: int = 100,
        sample_rate: float = 100.0,
    ):
        """
        Generate a synthetic signal composed of:
        - 5 Hz sine
        - 20 Hz sine
        - 50 Hz noise
        - random noise
        """
        return [
            math.sin(2 * math.pi * 5 * t / sample_rate)
            + 0.1 * math.sin(2 * math.pi * 20 * t / sample_rate)
            + 0.4 * math.sin(2 * math.pi * 50 * t / sample_rate)
            + 0.2 * random.uniform(-1, 1)
            for t in range(length)
        ]

    # Generate signal
    signal = generate_signal_with_50hz_noise(
        length=signal_length, sample_rate=sample_rate
    )

    # Compute FFT
    fft_result = fft(signal)

    # Apply Notch Filter to remove 50 Hz noise
    notch_filtered_fft = notch_filter(
        fft_result[:], sample_rate, notch_freq=notch_freq, bandwidth=bandwidth
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
        frequencies,
        magnitude_before,
        label="Original Spectrum",
        color="blue",
        alpha=0.7,
    )
    plt.plot(
        frequencies,
        magnitude_after,
        label="Filtered Spectrum",
        color="red",
        linestyle="--",
    )
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Original vs Filtered Spectrum (Overlay)")
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    demo()
