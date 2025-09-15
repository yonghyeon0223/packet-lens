import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def plot_protocol_distribution(protocol_counter, save_path):
    sorted_items = sorted(protocol_counter.items(), key=lambda x: x[1], reverse=True)
    protocols = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    plt.figure(figsize=(12, 8))
    bars = plt.barh(protocols, counts, color="skyblue")
    plt.xlabel("Packet Count")
    plt.title("Protocol Distribution")
    plt.gca().invert_yaxis()  # Highest count on top

    # Add count labels to bars
    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_width() + 5,
            bar.get_y() + bar.get_height() / 2,
            " " + str(count),
            va="center",
        )
    plt.savefig(save_path)


def plot_port_usage_over_time(df: pd.DataFrame, save_path):
    df["time_bin"] = df["time"].dt.floor("1T")
    unique_counts = df.groupby("time_bin")["port"].nunique().reset_index()
    print(unique_counts)

    plt.figure(figsize=(12, 8))
    plt.plot(
        unique_counts["time_bin"],
        unique_counts["port"],
        marker="o",
        color="steelblue",
        linewidth=2,
    )
    plt.xlabel("Time")
    plt.ylabel("Unique Ports Contacted")
    plt.title("Unique Ports Contacted per 1-Minute Window")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
    plt.savefig(save_path)
