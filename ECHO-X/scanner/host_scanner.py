# =========================================================
# ECHO-X
# Host Security Scanner - Step 21
# =========================================================

import socket
from datetime import datetime


class HostScanner:

    def __init__(self, target):

        self.target = target
        self.ip_address = None
        self.results = []

    # =====================================================
    # RESOLVE TARGET
    # =====================================================

    def resolve_target(self):

        try:

            self.ip_address = socket.gethostbyname(
                self.target
            )

            return True

        except socket.gaierror:

            return False

    # =====================================================
    # CHECK HOST REACHABILITY
    # =====================================================

    def check_reachability(self):

        if not self.ip_address:

            return {
                "status": "UNKNOWN",
                "message": "Host could not be resolved."
            }

        try:

            socket.create_connection(
                (self.ip_address, 80),
                timeout=2
            ).close()

            return {
                "status": "REACHABLE",
                "message": "Host is reachable."
            }

        except:

            try:

                socket.create_connection(
                    (self.ip_address, 443),
                    timeout=2
                ).close()

                return {
                    "status": "REACHABLE",
                    "message": "Host is reachable."
                }

            except:

                return {
                    "status": "UNREACHABLE",
                    "message": "Host could not be reached on HTTP/HTTPS."
                }

    # =====================================================
    # SCAN COMMON PORTS
    # =====================================================

    def scan_ports(self):

        common_ports = {

            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            8080: "HTTP-Proxy"
        }

        open_ports = []

        for port, service in common_ports.items():

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(0.5)

            try:

                result = sock.connect_ex(
                    (
                        self.ip_address,
                        port
                    )
                )

                if result == 0:

                    open_ports.append({

                        "port": port,

                        "service": service

                    })

            except:

                pass

            finally:

                sock.close()

        return open_ports

    # =====================================================
    # RISK ANALYSIS
    # =====================================================

    def calculate_risk(
        self,
        open_ports
    ):

        risk = 0

        dangerous_services = {

            21: 15,
            23: 30,
            445: 25,
            3389: 20
        }

        for port in open_ports:

            port_number = port["port"]

            if port_number in dangerous_services:

                risk += dangerous_services[
                    port_number
                ]

            else:

                risk += 5

        return min(
            risk,
            100
        )

    # =====================================================
    # THREAT LEVEL
    # =====================================================

    def get_threat_level(
        self,
        risk
    ):

        if risk >= 80:

            return "CRITICAL"

        elif risk >= 60:

            return "HIGH"

        elif risk >= 40:

            return "MEDIUM"

        else:

            return "LOW"

    # =====================================================
    # FULL SCAN
    # =====================================================

    def scan(self):

        print("\n")
        print("=" * 70)

        print(
            "              ECHO-X HOST SECURITY SCANNER"
        )

        print("=" * 70)

        print(
            f"\nTarget: {self.target}"
        )

        print(
            f"Scan Time: {datetime.now().isoformat()}"
        )

        # -------------------------------------------------
        # Resolve
        # -------------------------------------------------

        print("\n[1] Resolving Host...")

        if not self.resolve_target():

            print(
                "❌ Unable to resolve target."
            )

            return None

        print(
            f"IP Address: {self.ip_address}"
        )

        # -------------------------------------------------
        # Reachability
        # -------------------------------------------------

        print("\n[2] Checking Reachability...")

        reachability = (
            self.check_reachability()
        )

        print(
            f"Status: "
            f"{reachability['status']}"
        )

        # -------------------------------------------------
        # Port Scan
        # -------------------------------------------------

        print("\n[3] Scanning Common Ports...")

        open_ports = self.scan_ports()

        if open_ports:

            print(
                "\nOpen Ports:"
            )

            for port in open_ports:

                print(
                    f"  {port['port']} "
                    f"→ {port['service']}"
                )

        else:

            print(
                "No common open ports detected."
            )

        # -------------------------------------------------
        # Risk
        # -------------------------------------------------

        risk = self.calculate_risk(
            open_ports
        )

        threat_level = (
            self.get_threat_level(
                risk
            )
        )

        # -------------------------------------------------
        # Results
        # -------------------------------------------------

        result = {

            "target":
                self.target,

            "ip_address":
                self.ip_address,

            "reachability":
                reachability,

            "open_ports":
                open_ports,

            "risk_score":
                risk,

            "threat_level":
                threat_level,

            "timestamp":
                datetime.now().isoformat()
        }

        self.results = result

        # -------------------------------------------------
        # Final Report
        # -------------------------------------------------

        print("\n")
        print("-" * 70)

        print(
            "              ECHO-X SCAN RESULT"
        )

        print("-" * 70)

        print(
            f"\nTarget: "
            f"{self.target}"
        )

        print(
            f"IP Address: "
            f"{self.ip_address}"
        )

        print(
            f"Open Ports: "
            f"{len(open_ports)}"
        )

        print(
            f"Risk Score: "
            f"{risk}/100"
        )

        print(
            f"Threat Level: "
            f"{threat_level}"
        )

        print("-" * 70)

        return result


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)

    print(
        "        ECHO-X HOST SECURITY SCANNER"
    )

    print(
        "                    STEP 21"
    )

    print("=" * 70)

    target = input(
        "\nEnter an authorized host/domain to scan: "
    ).strip()

    if not target:

        print(
            "\n❌ No target provided."
        )

    else:

        scanner = HostScanner(
            target
        )

        scanner.scan()