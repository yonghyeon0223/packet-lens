import subprocess
from collections import Counter
import time


def compute_protocol_distribution(path: str) -> Counter:
    print("🚀 Starting protocol distribution analysis using tshark...")
    start_time = time.time()

    try:
        cmd = ["tshark", "-r", path, "-T", "fields", "-e", "_ws.col.Protocol"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running tshark: {e}")
        return Counter()

    protocols = result.stdout.strip().split("\n")
    protocol_counter = Counter(protocols)
    print(f"✅ Analysis complete in {(time.time() - start_time):.2f} seconds.")
    return protocol_counter
