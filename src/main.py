import analyser
import graph
from pathlib import Path
import time


def analyse_example_pcap_file(logname: str):
    LOGPATH = f"logs/{logname}.pcap"

    A1 = "protocol_distribution"
    dist = analyser.compute_protocol_distribution(LOGPATH)
    graph.plot_protocol_distribution(dist, f"report/{logname}_{A1}.png")

    A2 = "port_usage_over_time"
    port_usage = analyser.compute_port_usage(LOGPATH)
    graph.plot_port_usage_over_time(port_usage, f"report/{logname}_{A2}.png")


if __name__ == "__main__":
    analyse_example_pcap_file("snort-log-01")
