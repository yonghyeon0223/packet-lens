import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import BoundaryNorm
import pandas as pd
import seaborn as sns


def plot_protocol_distribution(protocol_counter, save_path):
    sorted_items = sorted(protocol_counter.items(), key=lambda x: x[1], reverse=True)
    protocols = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    plt.figure(figsize=(12, 10))
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
    plt.tight_layout()
    plt.savefig(save_path)


def plot_port_usage_over_time(df: pd.DataFrame, save_path):
    df["time_bin"] = df["time"].dt.floor("1T")
    unique_counts = df.groupby("time_bin")["port"].nunique().reset_index()

    plt.figure(figsize=(12, 10))
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
    plt.savefig(save_path)


def plot_port_usage_by_ip_addr(df: pd.DataFrame, save_path, interval=1000):
    top_ips = df["src_ip"].value_counts().nlargest(30).index
    df2 = df[df["src_ip"].isin(top_ips)].copy()

    df2["port_range"] = (df2["port"] // interval) * interval
    df2["port_range_label"] = (
        df2["port_range"].astype(str)
        + "-"
        + (df2["port_range"] + interval - 1).astype(str)
    )

    pivot_df = df2.groupby(["src_ip", "port_range_label"]).size().unstack(fill_value=0)
    pivot_df = pivot_df[
        sorted(pivot_df.columns, key=lambda x: int(str(x).split("-")[0]))
    ]

    bounds = [0, 1, 10, 100, 1000, pivot_df.to_numpy().max()]
    norm = BoundaryNorm(bounds, ncolors=256)

    plt.figure(figsize=(12, 10))
    sns.heatmap(pivot_df, cmap="Blues", linewidths=0.5, norm=norm)

    plt.title("Unique Port Range Contacted per IP-address")
    plt.xlabel("Destination Port")
    plt.ylabel("Source IP")
    plt.tight_layout()
    plt.savefig(save_path)
