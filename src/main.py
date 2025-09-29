import capturer
import analyser
import graph
import os


def visualize_example_pcap_file(logname: str, port_interval):
    LOGPATH = f"logs/{logname}.pcap"
    fig_save_path = f"report/{logname}"
    os.makedirs(f"{fig_save_path}", exist_ok=True)

    A1 = "protocol_distribution"
    dist = analyser.compute_protocol_distribution(LOGPATH)
    graph.plot_protocol_distribution(dist, f"{fig_save_path}/{A1}.png")

    A2 = "port_usage_over_time"
    port_usage = analyser.compute_port_usage(LOGPATH)
    graph.plot_port_usage_over_time(port_usage, f"{fig_save_path}/{A2}.png")

    A3 = "port_usage_by_ip_addr"
    graph.plot_port_usage_by_ip_addr(
        port_usage, f"{fig_save_path}/{A3}.png", interval=port_interval
    )

    A4 = "top_used_keywords"
    top_words = analyser.analyse_tcp_payload(LOGPATH)
    graph.heatmap_tcp_payload(top_words, f"{fig_save_path}/{A4}.png")


if __name__ == "__main__":
    server_list = capturer.capture_all(capture_time=600, capture=False)

    for server in server_list:
        visualize_example_pcap_file(server, 3000)

    visualize_example_pcap_file("snort-log-01", 3000)
