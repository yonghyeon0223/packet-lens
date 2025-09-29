import analyser
import graph


def analyse_example_pcap_file(logname: str, port_interval):
    LOGPATH = f"logs/{logname}.pcap"

    A1 = "protocol_distribution"
    dist = analyser.compute_protocol_distribution(LOGPATH)
    graph.plot_protocol_distribution(dist, f"report/{logname}_{A1}.png")

    A2 = "port_usage_over_time"
    port_usage = analyser.compute_port_usage(LOGPATH)
    graph.plot_port_usage_over_time(port_usage, f"report/{logname}_{A2}.png")

    A3 = "port_usage_by_ip_addr"
    graph.plot_port_usage_by_ip_addr(
        port_usage, f"report/{logname}_{A3}.png", interval=port_interval
    )

    A4 = "top_used_keywords"
    top_words = analyser.analyse_tcp_payload(LOGPATH)
    graph.heatmap_tcp_payload(top_words, f"report/{logname}_{A4}.png")


if __name__ == "__main__":
    analyse_example_pcap_file("snort-log-01", 2000)
    # analyse_example_pcap_file("pgsql-jdbc", 20)
