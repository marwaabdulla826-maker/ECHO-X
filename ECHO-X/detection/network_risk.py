# =========================================================
# ECHO-X
# Network Risk Analysis Engine - Step 24
# =========================================================

from scanner.network_scanner import NetworkScanner


class NetworkRiskAnalyzer:

    def __init__(self, devices):

        self.devices = devices

    # =====================================================
    # ANALYZE DEVICE
    # =====================================================

    def analyze_device(self, device):

        risk = 0
        findings = []

        ip = device.get(
            "ip",
            "Unknown"
        )

        hostname = device.get(
            "hostname",
            "Unknown"
        )

        open_ports = device.get(
            "open_ports",
            []
        )

        # -------------------------------------------------
        # Port-based risk
        # -------------------------------------------------

        risky_ports = {

            21: (
                15,
                "FTP service exposed"
            ),

            23: (
                30,
                "Telnet service exposed"
            ),

            445: (
                25,
                "SMB service exposed"
            ),

            3389: (
                20,
                "RDP service exposed"
            ),

            3306: (
                20,
                "MySQL service exposed"
            ),

            5432: (
                20,
                "PostgreSQL service exposed"
            )
        }

        normal_ports = {

            22: (
                5,
                "SSH service detected"
            ),

            80: (
                5,
                "HTTP service detected"
            ),

            443: (
                2,
                "HTTPS service detected"
            ),

            8080: (
                5,
                "Alternative HTTP service detected"
            )
        }

        # -------------------------------------------------
        # Analyze ports
        # -------------------------------------------------

        for port in open_ports:

            if port in risky_ports:

                score, message = (
                    risky_ports[port]
                )

                risk += score

                findings.append({
                    "port": port,
                    "severity": "HIGH",
                    "finding": message
                })

            elif port in normal_ports:

                score, message = (
                    normal_ports[port]
                )

                risk += score

                findings.append({
                    "port": port,
                    "severity": "LOW",
                    "finding": message
                })

            else:

                risk += 5

                findings.append({
                    "port": port,
                    "severity": "MEDIUM",
                    "finding":
                        f"Unknown service on port {port}"
                })

        risk = min(
            risk,
            100
        )

        threat_level = (
            self.get_threat_level(
                risk
            )
        )

        return {

            "ip":
                ip,

            "hostname":
                hostname,

            "open_ports":
                open_ports,

            "risk_score":
                risk,

            "threat_level":
                threat_level,

            "findings":
                findings
        }

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
    # ANALYZE NETWORK
    # =====================================================

    def analyze_network(self):

        print("\n")
        print("=" * 70)

        print(
            "             ECHO-X NETWORK RISK ANALYSIS"
        )

        print("=" * 70)

        if not self.devices:

            print(
                "\n❌ No devices available for analysis."
            )

            return None

        results = []

        total_risk = 0

        # -------------------------------------------------
        # Analyze each device
        # -------------------------------------------------

        for device in self.devices:

            result = self.analyze_device(
                device
            )

            results.append(
                result
            )

            total_risk += (
                result["risk_score"]
            )

        # -------------------------------------------------
        # Network Risk
        # -------------------------------------------------

        network_risk = round(
            total_risk
            / len(results),
            2
        )

        network_threat = (
            self.get_threat_level(
                network_risk
            )
        )

        # -------------------------------------------------
        # Display results
        # -------------------------------------------------

        for result in results:

            print("\n")
            print(
                "-" * 70
            )

            print(
                f"Device: "
                f"{result['hostname']}"
            )

            print(
                f"IP: "
                f"{result['ip']}"
            )

            print(
                f"Open Ports: "
                f"{result['open_ports']}"
            )

            print(
                f"Risk Score: "
                f"{result['risk_score']}/100"
            )

            print(
                f"Threat Level: "
                f"{result['threat_level']}"
            )

            if result["findings"]:

                print(
                    "\nSecurity Findings:"
                )

                for finding in result[
                    "findings"
                ]:

                    print(
                        f"  [{finding['severity']}] "
                        f"Port {finding['port']}: "
                        f"{finding['finding']}"
                    )

        # -------------------------------------------------
        # Final network result
        # -------------------------------------------------

        print("\n")
        print("=" * 70)

        print(
            "             OVERALL NETWORK RISK"
        )

        print("=" * 70)

        print(
            f"\nDevices Analyzed: "
            f"{len(results)}"
        )

        print(
            f"Average Network Risk: "
            f"{network_risk}/100"
        )

        print(
            f"Network Threat Level: "
            f"{network_threat}"
        )

        print("=" * 70)

        return {

            "devices":
                results,

            "network_risk":
                network_risk,

            "network_threat":
                network_threat
        }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)

    print(
        "        ECHO-X NETWORK RISK ANALYSIS"
    )

    print(
        "                    STEP 24"
    )

    print("=" * 70)

    print(
        "\n⚠️ Only analyze networks you own "
        "or have permission to test."
    )

    network_input = input(
        "\nEnter authorized network "
        "(example: 192.168.100.0/24): "
    ).strip()

    if not network_input:

        print(
            "\n❌ No network provided."
        )

    else:

        scanner = NetworkScanner(
            network_input
        )

        devices = scanner.discover()

        analyzer = NetworkRiskAnalyzer(
            devices
        )

        analyzer.analyze_network()