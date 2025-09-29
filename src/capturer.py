import os
from pathlib import Path
import time

""" NOTE
Make sure you have 
 - a local SSH key pair before running this script
 - a valid list of linux servers in servers.txt
 - ssh connection to the user with sudo privilege
"""

SSH_PUB_PATH = Path.home() / ".ssh" / "id_rsa.pub"
PUB_KEY = SSH_PUB_PATH.read_text().strip()


def get_server_list(config_file):
    with open(config_file, "r") as f:
        content = f.read().strip()
        server_list = []
        for server in content.split("\n"):
            if not server:
                continue
            if len(server.split("@")) != 2:
                continue
            server_list.append(server)
        return server_list


def copy_over_ssh_key(server_list):
    if not len(server_list) or not PUB_KEY:
        return

    dest = "~/.ssh/authorized_keys"

    for server in server_list:
        # check if my SSH key has already been added
        check_cmd = f"ssh {server} \"grep -q -F '{PUB_KEY}' {dest} 2>/dev/null\""
        exit_code = os.system(check_cmd)
        if exit_code == 0:
            print(f"✅ Key already exists on {server}, skipping.")
        else:
            print(f"🔑 Copying key to {server}...")
            cmd = (
                "mkdir -p ~/.ssh && chmod 700 ~/.ssh && "
                f"echo '{PUB_KEY}' >> {dest} && chmod 600 {dest}"
            )

            exit_code = os.system(f'ssh {server} "{cmd}"')
            if exit_code == 0:
                print(f"✅ Key copied successfully to {server}")
            else:
                print(f"❌ Failed to copy key to {server}")


def order_capture(seconds, server_list):
    for server in server_list:
        user = server.split("@")[0]
        print(f"📡 Starting capture on {server}...")
        cmd = (
            f"sudo nohup tcpdump -i any -U "
            f"-w ~/capture_$(date +%F_%H-%M-%S).pcap "
            f"-G {seconds} -W 1 -Z {user} > /dev/null 2>&1 &"
        )
        exit_code = os.system(f'ssh {server} "{cmd}"')


def download_latest_pcap(server_list):
    logs = Path("logs")
    logs.mkdir(exist_ok=True)
    for server in server_list:
        f = f"{server}.pcap"
        scp_cmd = f"scp -p {server}:$(ssh {server} 'sudo ls -t ~/*.pcap | head -n 1') {logs/f}"
        os.system(scp_cmd)


def capture_all(capture_time, capture=True):
    server_list = get_server_list(config_file="servers.txt")
    if not capture:
        return server_list

    copy_over_ssh_key(server_list=server_list)
    order_capture(capture_time, server_list)
    print(f"⏳ waiting for caputre to complete... {capture_time} seconds")
    time.sleep(capture_time + 1)
    download_latest_pcap(server_list=server_list)
    return server_list
