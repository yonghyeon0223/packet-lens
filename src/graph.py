import matplotlib.pyplot as plt


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
    plt.savefig(save_path, dpi=600, bbox_inches="tight")
