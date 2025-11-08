import pandas as pd
import matplotlib.pyplot as plt


def plot_motor_data(
    csv_files: list[str],
    output_pdf: str = "motor_data.pdf",
    output_png_prefix: str | None = None,
):
    # Create figure with subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Motor Power Relationship Data", fontsize=16)

    colors = ["blue", "orange", "green", "red", "purple", "brown", "pink"]

    for idx, csv_file in enumerate(csv_files):
        # Load CSV
        df = pd.read_csv(csv_file)

        # Ensure expected columns exist
        expected_cols = ["input_power", "speed", "torque", "efficiency", "output_power"]
        for col in expected_cols:
            if col not in df.columns:
                raise ValueError(f"Missing expected column in {csv_file}: {col}")

        label = csv_file.split("/")[-1]  # Use filename as legend label
        color = colors[idx % len(colors)]  # Cycle through colors

        # Common marker settings
        marker_style = dict(marker="o", markersize=2, linewidth=1)

        # Plot Speed vs Input Power
        axs[0, 0].plot(
            df["input_power"], df["speed"], label=label, color=color, **marker_style
        )
        axs[0, 0].set_title("Speed vs Input Power")
        axs[0, 0].set_xlabel("Input Power")
        axs[0, 0].set_ylabel("Speed (%)")

        # Plot Torque vs Input Power
        axs[0, 1].plot(
            df["input_power"], df["torque"], label=label, color=color, **marker_style
        )
        axs[0, 1].set_title("Torque vs Input Power")
        axs[0, 1].set_xlabel("Input Power")
        axs[0, 1].set_ylabel("Torque (Nm)")

        # Plot Efficiency vs Input Power
        axs[1, 0].plot(
            df["input_power"], df["efficiency"], label=label, color=color, **marker_style
        )
        axs[1, 0].set_title("Efficiency vs Input Power")
        axs[1, 0].set_xlabel("Input Power")
        axs[1, 0].set_ylabel("Efficiency (%)")

        # Plot Output Power vs Input Power
        axs[1, 1].plot(
            df["input_power"], df["output_power"], label=label, color=color, **marker_style
        )
        axs[1, 1].set_title("Output Power vs Input Power")
        axs[1, 1].set_xlabel("Input Power")
        axs[1, 1].set_ylabel("Output Power (W)")

    # Add legends
    for ax in axs.flat:
        ax.legend(fontsize=8)

    plt.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))

    # Save as PDF
    plt.savefig(output_pdf, format="pdf")
    print(f"Plot saved to {output_pdf}")

    # Save each subplot as high-resolution PNGs if requested
    if output_png_prefix:
        subplot_titles = ["speed", "torque", "efficiency", "output_power"]
        for ax, title in zip(axs.flat, subplot_titles):
            fig_individual, ax_individual = plt.subplots(figsize=(6, 4), dpi=300)
            for line in ax.get_lines():
                ax_individual.plot(
                    line.get_xdata(),
                    line.get_ydata(),
                    label=line.get_label(),
                    color=line.get_color(),
                    marker="o",
                    markersize=2,
                    linewidth=1,
                )
            ax_individual.set_title(ax.get_title())
            ax_individual.set_xlabel(ax.get_xlabel())
            ax_individual.set_ylabel(ax.get_ylabel())
            ax_individual.legend(fontsize=8)
            plt.tight_layout()
            plt.show()
            filename = f"{output_png_prefix}_{title}.png"
            fig_individual.savefig(filename, dpi=300)
            plt.close(fig_individual)
            print(f"Saved {filename}")


if __name__ == "__main__":
    # Example: compare two log files and export as PDF + individual PNGs
    plot_motor_data(
        [
            f"/home/derek/PycharmProjects/VEX-3773P-2025-2026/logs/friction_tests/GREEN_{i*100}G.csv" for i in range(1, 31)
        ],
        output_pdf="/home/derek/PycharmProjects/VEX-3773P-2025-2026/logs/competition_drivetrain.pdf",
        output_png_prefix="/home/derek/PycharmProjects/VEX-3773P-2025-2026/logs/competition_drivetrain",
    )
