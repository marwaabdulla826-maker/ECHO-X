# =========================================================
# ECHO-X
# Network Discovery Scanner - REAL NETWORK MODE
# =========================================================

import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


class NetworkScanner:

    def __init__(self, network):

        self.network = network
        self.devices = []
        self.demo_mode = False

    # =====================================================
    # CHECK HOST
    # =====================================================

    def check_host(self, ip):

        ip = str(ip)

        common_ports = [
            21,      # FTP
            22,      # SSH
            23,      # Telnet
            25,      # SMTP
            53,      # DNS
            80,      # HTTP
            110,     # POP3
            143,     # IMAP
            443,     # HTTPS
            445,     # SMB
            3306,    # MySQL
            3389,    # RDP
            5432,    # PostgreSQL
            8080     # HTTP Alternative
        ]

        open_ports = []

        for port in common_ports:

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(0.5)

            try:

                result = sock.connect_ex(
                    (ip, port)
                )

                if result == 0:

                    open_ports.append(port)

            except Exception:

                pass

            finally:

                sock.close()

        # -------------------------------------------------
        # Host considered active only if a scanned port
        # responds.
        # -------------------------------------------------

        if open_ports:

            hostname = self.get_hostname(ip)

            return {
                "ip": ip,
                "hostname": hostname,
                "open_ports": open_ports,
                "scan_source": "REAL"
            }

        return None

    # =====================================================
    # GET HOSTNAME
    # =====================================================

    def get_hostname(self, ip):

        try:

            hostname = socket.gethostbyaddr(ip)[0]

            return hostname

        except Exception:

            return "Unknown"

    # =====================================================
    # DISCOVER NETWORK
    # =====================================================

    def discover(self):

        print("\n")
        print("=" * 70)

        print(
            "             ECHO-X REAL NETWORK DISCOVERY"
        )

        print("=" * 70)

        print(
            f"\nTarget Network: {self.network}"
        )

        print(
            f"Scan Time: {datetime.now().isoformat()}"
        )

        # -------------------------------------------------
        # Reset previous results
        # -------------------------------------------------

        self.devices = []
        self.demo_mode = False

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

        hosts = list(network.hosts())

        print(
            f"\nHosts to check: {len(hosts)}"
        )

        # -------------------------------------------------
        # Prevent extremely large scans
        # -------------------------------------------------

        if len(hosts) > 1024:

            print(
                "\n⚠️ Network is too large."
            )

            print(
                "Please use a smaller authorized network."
            )

            return []

        if not hosts:

            print(
                "\n❌ No usable hosts found."
            )

            return []

        # -------------------------------------------------
        # REAL NETWORK SCAN
        # -------------------------------------------------

        print(
            "\n🔍 Scanning authorized network..."
        )

        print(
            "📡 Checking real hosts and common services..."
        )

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
        # NO DEMO FALLBACK
        # -------------------------------------------------

        if not self.devices:

            print("\n")
            print("-" * 70)

            print(
                "              REAL SCAN RESULT"
            )

            print("-" * 70)

            print(
                "\n⚠️ No active hosts detected."
            )

            print(
                "No simulated devices were added."
            )

            print(
                "The result contains only real scan data."
            )

            print("-" * 70)

            return []

        # -------------------------------------------------
        # RESULTS
        # -------------------------------------------------

        print("\n")
        print("-" * 70)

        print(
            "              REAL DISCOVERY RESULTS"
        )

        print("-" * 70)

        print(
            "\n🔴 REAL NETWORK DATA"
        )

        print(
            f"\nDevices Found: {len(self.devices)}"
        )

        for device in self.devices:

            print("\n")

            print(
                f"IP: {device['ip']}"
            )

            print(
                f"Hostname: {device['hostname']}"
            )

            if device["open_ports"]:

                print(
                    "Open Ports: "
                    + ", ".join(
                        str(port)
                        for port in device["open_ports"]
                    )
                )

            else:

                print(
                    "Open Ports: None"
                )

            print(
                "Source: REAL"
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
        "        ECHO-X REAL NETWORK DISCOVERY"
    )

    print("=" * 70)

    print(
        "\n⚠️ Only scan networks you own "
        "or have permission to test."
    )

    network_input = input(
        "\nEnter authorized network "
        "(example: 192.168.1.0/24): "
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

