# =========================================================
# ECHO-X
# Network Discovery Scanner - Step 22
# =========================================================

import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


class NetworkScanner:

    def __init__(self, network):

        self.network = network
        self.devices = []

    # =====================================================
    # CHECK HOST
    # =====================================================

    def check_host(self, ip):

        ip = str(ip)

        common_ports = [
            22,      # SSH
            80,      # HTTP
            443,     # HTTPS
            445,     # SMB
            3389,    # RDP
            8080     # HTTP alternative
        ]

        open_ports = []

        for port in common_ports:

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(0.2)

            try:

                result = sock.connect_ex(
                    (ip, port)
                )

                if result == 0:

                    open_ports.append(
                        port
                    )

            except:

                pass

            finally:

                sock.close()

        # -------------------------------------------------
        # Determine whether host is active
        # -------------------------------------------------

        if open_ports:

            hostname = self.get_hostname(
                ip
            )

            return {

                "ip":
                    ip,

                "hostname":
                    hostname,

                "open_ports":
                    open_ports
            }

        return None

    # =====================================================
    # GET HOSTNAME
    # =====================================================

    def get_hostname(self, ip):

        try:

            hostname = socket.gethostbyaddr(
                ip
            )[0]

            return hostname

        except:

            return "Unknown"

    # =====================================================
    # DISCOVER NETWORK
    # =====================================================

    def discover(self):

        print("\n")
        print("=" * 70)

        print(
            "             ECHO-X NETWORK DISCOVERY"
        )

        print("=" * 70)

        print(
            f"\nTarget Network: "
            f"{self.network}"
        )

        print(
            f"Scan Time: "
            f"{datetime.now().isoformat()}"
        )

        # -------------------------------------------------
        # Validate network
        # -------------------------------------------------

        try:

            network = ipaddress.ip_network(
                self.network,
                strict=False
            )

        except ValueError:

            print(
                "\n❌ Invalid network."
            )

            return []

        hosts = list(
            network.hosts()
        )

        print(
            f"\nHosts to check: "
            f"{len(hosts)}"
        )

        print(
            "\n🔍 Discovering active hosts..."
        )

        # -------------------------------------------------
        # Parallel discovery
        # -------------------------------------------------

        with ThreadPoolExecutor(
            max_workers=50
        ) as executor:

            results = executor.map(
                self.check_host,
                hosts
            )

        self.devices = [
            result
            for result in results
            if result is not None
        ]

        # -------------------------------------------------
        # Results
        # -------------------------------------------------

        print("\n")
        print("-" * 70)

        print(
            "              DISCOVERY RESULTS"
        )

        print("-" * 70)

        if not self.devices:

            print(
                "\nNo active hosts detected."
            )

        else:

            print(
                f"\nDevices Found: "
                f"{len(self.devices)}"
            )

            for device in self.devices:

                print("\n")

                print(
                    f"IP: "
                    f"{device['ip']}"
                )

                print(
                    f"Hostname: "
                    f"{device['hostname']}"
                )

                if device["open_ports"]:

                    print(
                        "Open Ports: "
                        + ", ".join(
                            str(port)
                            for port
                            in device["open_ports"]
                        )
                    )

                else:

                    print(
                        "Open Ports: None"
                    )

        print("\n")
        print("-" * 70)

        return self.devices


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)

    print(
        "        ECHO-X NETWORK DISCOVERY"
    )

    print(
        "                    STEP 22"
    )

    print("=" * 70)

    print(
        "\n⚠️ Only scan networks you own or have permission to test."
    )

    network_input = input(
        "\nEnter authorized network (example: 192.168.1.0/24): "
    ).strip()

    if not network_input:

        print(
            "\n❌ No network provided."
        )

    else:

        scanner = NetworkScanner(
            network_input
        )

        scanner.discover()