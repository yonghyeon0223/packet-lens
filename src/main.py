from analyser import compute_protocol_distribution


def analyse_example_pcap_file(path: str):
    protocol_distribution = compute_protocol_distribution(path)
    print(protocol_distribution)


if __name__ == "__main__":
    analyse_example_pcap_file("logs/snort-log-01.pcap")
