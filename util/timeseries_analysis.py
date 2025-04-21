import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASENAME = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASENAME)

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", 0)  # Disable automatic line wrapping


class TimeSeriesAnalyzer:
    def __init__(self, filename):
        """
        Initialize the analyzer with the given CSV filename.

        :param filename: The path to the CSV file to analyze.
        """
        self.filename = filename
        self.data = self._load_data()
        self.time_column = self._detect_time_column()

    def _load_data(self):
        """Load the CSV data into a pandas DataFrame."""
        try:
            data = pd.read_csv(self.filename)
            print(f"Data loaded successfully from {self.filename}.")
            return data
        except FileNotFoundError:
            print(f"Error: The file {self.filename} was not found.")
            return None

    def _detect_time_column(self):
        """Automatically detect the time column based on common keywords."""
        if self.data is not None:
            for col in self.data.columns:
                if "time" in col.lower() or "(s)" in col.lower():
                    print(f"Detected time column: {col}")
                    return col
            print("Warning: No obvious time column detected.")
        return None

    def basic_statistics(self):
        """Print basic statistics for the numerical columns."""
        if self.data is not None:
            print("Basic Statistics:")
            print(self.data.describe())
        else:
            print("No data available to analyze.")

    def plot_time_series(self, columns=None, title="Time Series Data"):
        """
        Plot time series data for selected columns.

        :param columns: List of columns to plot. If None, all columns except time will be plotted.
        :param title: Title of the plot.
        """
        if self.data is None:
            print("No data available to plot.")
            return

        if self.time_column is None:
            print("Time column is not detected. Cannot plot time series.")
            return

        if columns is None:
            columns = [col for col in self.data.columns if col != self.time_column]

        plt.figure(figsize=(15, 7))
        for column in columns:
            if column in self.data.columns:
                plt.plot(self.data[self.time_column], self.data[column], label=column)

        plt.xlabel(self.time_column)
        plt.ylabel("Value")
        plt.title(title)
        plt.legend()
        plt.grid(which="both", axis="x", linestyle="--")
        plt.grid(
            which="both",
            axis="y",
            linestyle="--",
        )

        y_min, y_max = plt.ylim()
        plt.yticks(np.arange(round(y_min, -1), round(y_max, -1), 10))

        plt.show()


# Example Usage
if __name__ == "__main__":
    # Automatically detects CSV path in your project structure
    filename = os.path.join(PROJECT_ROOT, "logs/left_drivetrain.csv")

    # Initialize the analyzer
    analyzer = TimeSeriesAnalyzer(filename)

    # Show basic statistics
    analyzer.basic_statistics()

    # Plot ALL available columns except the detected time column
    analyzer.plot_time_series(title="Robot Data Overview")

    # # Plot just specific columns if desired
    # analyzer.plot_time_series(columns=['left_speed (cm/s)', 'right_speed (cm/s)'],
    #                           title="Left and Right Speeds Over Time")
