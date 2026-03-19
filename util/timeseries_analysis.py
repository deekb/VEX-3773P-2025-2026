import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from deploy.Constants import LOCAL_LOGS_DIRECTORY

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 0)


class TimeSeriesAnalyzer:
    def __init__(self, filenames: dict):
        """
        Initialize with multiple datasets.

        :param filenames: dict like {"left": path1, "right": path2}
        """
        self.datasets = self._load_multiple(filenames)
        self.time_column = self._detect_time_column()

    def _load_multiple(self, filenames):
        """Load multiple CSV files into a dictionary of DataFrames."""
        datasets = {}
        for name, file in filenames.items():
            try:
                df = pd.read_csv(file)
                datasets[name] = df
                print(f"Loaded '{name}' from {file}")
            except FileNotFoundError:
                print(f"Error: {file} not found.")
        return datasets

    def _detect_time_column(self):
        """Detect a shared time column from the first dataset."""
        if not self.datasets:
            return None

        sample_df = next(iter(self.datasets.values()))

        for col in sample_df.columns:
            if "time" in col.lower() or "input" in col.lower():
                print(f"Detected time column: {col}")
                return col

        print("Warning: No obvious time column detected.")
        return None

    def basic_statistics(self):
        """Print statistics for each dataset."""
        if not self.datasets:
            print("No data available.")
            return

        for name, df in self.datasets.items():
            print(f"\n=== Statistics for {name} ===")
            print(df.describe())

    def plot_time_series(self, columns=None, title="Time Series Comparison"):
        """
        Plot multiple datasets on the same axes.

        :param columns: list of columns to plot (default: all except time)
        :param title: plot title
        """
        if not self.datasets:
            print("No data available.")
            return

        if self.time_column is None:
            print("Time column not detected.")
            return

        sample_df = next(iter(self.datasets.values()))

        if columns is None:
            columns = [col for col in sample_df.columns if col != self.time_column]

        plt.figure(figsize=(15, 7))

        for dataset_name, df in self.datasets.items():
            if self.time_column not in df.columns:
                print(f"Skipping {dataset_name}: no time column.")
                continue

            # Sort by time to avoid jagged plots
            df = df.sort_values(by=self.time_column)

            for column in columns:
                if column in df.columns:
                    plt.plot(
                        df[self.time_column],
                        df[column],
                        label=f"{dataset_name} - {column}"
                    )

        plt.xlabel(self.time_column)
        plt.ylabel("Value")
        plt.title(title)
        plt.legend()
        plt.grid(which="both", linestyle="--")

        # Better Y tick spacing
        y_min, y_max = plt.ylim()
        try:
            plt.yticks(np.arange(round(y_min, -1), round(y_max, -1), 10))
        except ValueError:
            pass  # fallback if range is too small

        plt.tight_layout()
        plt.show()

    def plot_subplots(self, columns=None, title="Time Series Subplots"):
        """
        Plot each column in its own subplot for easier comparison.
        """
        if not self.datasets or self.time_column is None:
            print("Missing data or time column.")
            return

        sample_df = next(iter(self.datasets.values()))

        if columns is None:
            columns = [col for col in sample_df.columns if col != self.time_column]

        num_cols = len(columns)
        fig, axes = plt.subplots(num_cols, 1, figsize=(15, 4 * num_cols), sharex=True)

        if num_cols == 1:
            axes = [axes]

        for i, column in enumerate(columns):
            ax = axes[i]

            for dataset_name, df in self.datasets.items():
                if column in df.columns and self.time_column in df.columns:
                    df = df.sort_values(by=self.time_column)
                    ax.plot(
                        df[self.time_column],
                        df[column],
                        label=dataset_name
                    )

            ax.set_title(column)
            ax.grid(True)
            ax.legend()

        axes[-1].set_xlabel(self.time_column)
        fig.suptitle(title)
        plt.tight_layout()
        plt.show()


# =========================
# Example Usage
# =========================
if __name__ == "__main__":
    # files = {
    #     "left": os.path.join(LOCAL_LOGS_DIRECTORY, "left_drivetrain.csv"),
    #     "right": os.path.join(LOCAL_LOGS_DIRECTORY, "right_drivetrain.csv"),
    # }

    files = {
        "left0": os.path.join(LOCAL_LOGS_DIRECTORY, "left_0_drivetrain.csv"),
        "left1": os.path.join(LOCAL_LOGS_DIRECTORY, "left_1_drivetrain.csv"),
        "left2": os.path.join(LOCAL_LOGS_DIRECTORY, "left_2_drivetrain.csv"),
        "right0": os.path.join(LOCAL_LOGS_DIRECTORY, "right_0_drivetrain.csv"),
        "right1": os.path.join(LOCAL_LOGS_DIRECTORY, "right_1_drivetrain.csv"),
        "right2": os.path.join(LOCAL_LOGS_DIRECTORY, "right_2_drivetrain.csv"),
    }

    analyzer = TimeSeriesAnalyzer(files)

    # Stats for each dataset
    analyzer.basic_statistics()

    # Combined plot (all columns)
    analyzer.plot_time_series(title="Left vs Right Drivetrain")

    # Optional: cleaner comparison view
    analyzer.plot_subplots(title="Subplot Comparison")