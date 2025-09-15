import subprocess
from collections import Counter
import pandas as pd


def compute_protocol_distribution(path: str) -> Counter:
    try:
        cmd = ["tshark", "-r", path, "-T", "fields", "-e", "_ws.col.Protocol"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running tshark: {e}")
        return Counter

    protocols = result.stdout.strip().split("\n")
    protocol_counter = Counter(protocols)
    return protocol_counter


def compute_port_usage(path: str) -> pd.DataFrame:
    try:
        cmd1 = ["tshark", "-r", path, "-T", "fields", "-e", "frame.time_epoch"]
        cmd2 = ["-e", "ip.src", "-e", "tcp.dstport", "-e", "udp.dstport"]
        result = subprocess.run(cmd1 + cmd2, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running tshark: {e}")
        return pd.DataFrame()

    rows = []
    lines = result.stdout.strip().split("\n")
    for line in lines:
        try:
            ts, src_ip, tcp_port, udp_port = line.split("\t")
            port = int(tcp_port if tcp_port else udp_port)
            rows.append((float(ts), src_ip, port))
        except Exception as e:
            continue
    df = pd.DataFrame(rows, columns=["timestamp", "src_ip", "port"])
    df["time"] = pd.to_datetime(df["timestamp"], unit="s")
    return df
