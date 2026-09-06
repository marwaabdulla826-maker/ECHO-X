# =========================================================
# ECHO-X
# Threat Detection Engine - Step 25
# =========================================================

from scanner.network_scanner import NetworkScanner
from detection.network_risk import NetworkRiskAnalyzer


class ThreatDetector:

    def __init__(self, network_results):

        self.network_results = network_results
        self.threats = []

    # =====================================================
    # DETECT THREATS
    # =====================================================

    def detect(self):

        print("\n")
        print("=" * 70)
        print("              ECHO-X THREAT DETECTION")
        print("=" * 70)

        if not self.network_results:

            print(
                "\n❌ No network analysis results."
            )

            return []

        self.threats = []

        for device in self.network_results:

            ip = device.get(
                "ip",
                "Unknown"
            )

            hostname = device.get(
                "hostname",
                "Unknown"
            )

            risk_score = device.get(
                "risk_score",
                0
            )

            findings = device.get(
                "findings",
                []
            )

            # -------------------------------------------------
            # Analyze findings
            # -------------------------------------------------

            for finding in findings:

                severity = finding.get(
                    "severity",
                    "LOW"
                )

                port = finding.get(
                    "port",
                    "Unknown"
                )

                message = finding.get(
                    "finding",
                    "Unknown security finding"
                )

                # ---------------------------------------------
                # HIGH severity
                # ---------------------------------------------

                if severity == "HIGH":

                    threat = {

                        "device":
                            hostname,

                        "ip":
                            ip,

                        "port":
                            port,

                        "threat_type":
                            self.identify_threat(port),

                        "severity":
                            "HIGH",

                        "risk_score":
                            risk_score,

                        "description":
                            message
                    }

                    self.threats.append(
                        threat
                    )

                # ---------------------------------------------
                # MEDIUM severity
                # ---------------------------------------------

                elif severity == "MEDIUM":

                    threat = {

                        "device":
                            hostname,

                        "ip":
                            ip,

                        "port":
                            port,

                        "threat_type":
                            "Unknown / Unclassified Service",

                        "severity":
                            "MEDIUM",

                        "risk_score":
                            risk_score,

                        "description":
                            message
                    }

                    self.threats.append(
                        threat
                    )

        self.display_results()

        return self.threats

    # =====================================================
    # IDENTIFY THREAT
    # =====================================================

    def identify_threat(
        self,
        port
    ):

        threat_map = {

            21:
                "FTP Exposure",

            23:
                "Telnet Exposure",

            445:
                "SMB Exposure",

            3389:
                "RDP Exposure",

            3306:
                "MySQL Exposure",

            5432:
                "PostgreSQL Exposure"
        }

        return threat_map.get(
            port,
            "Potential Service Exposure"
        )

    # =====================================================
    # DISPLAY
    # =====================================================

    def display_results(self):

        print("\n")
        print("-" * 70)
        print("              DETECTED THREATS")
        print("-" * 70)

        if not self.threats:

            print(
                "\n🟢 No significant threats detected."
            )

            print(
                "\nECHO-X Security Status: SAFE"
            )

            return

        print(
            f"\nThreats Detected: "
            f"{len(self.threats)}"
        )

        for index, threat in enumerate(
            self.threats,
            start=1
        ):

            print("\n")
            print(
                f"🚨 THREAT #{index}"
            )

            print(
                f"Device: "
                f"{threat['device']}"
            )

            print(
                f"IP Address: "
                f"{threat['ip']}"
            )

            print(
                f"Port: "
                f"{threat['port']}"
            )

            print(
                f"Threat Type: "
                f"{threat['threat_type']}"
            )

            print(
                f"Severity: "
                f"{threat['severity']}"
            )

            print(
                f"Risk Score: "
                f"{threat['risk_score']}/100"
            )

            print(
                f"Description: "
                f"{threat['description']}"
            )

        print("\n")
        print("=" * 70)

        print(
            "              ECHO-X THREAT SUMMARY"
        )

        print("=" * 70)

        high = sum(
            1
            for threat in self.threats
            if threat["severity"] == "HIGH"
        )

        medium = sum(
            1
            for threat in self.threats
            if threat["severity"] == "MEDIUM"
        )

        print(
            f"\nHIGH Threats: "
            f"{high}"
        )

        print(
            f"MEDIUM Threats: "
            f"{medium}"
        )

        print(
            f"Total Threats: "
            f"{len(self.threats)}"
        )

        print("\n🔴 ECHO-X Security Status: THREAT DETECTED")

        print("=" * 70)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)

    print(
        "        ECHO-X THREAT DETECTION"
    )

    print(
        "                    STEP 25"
    )

    print("=" * 70)

    print(
        "\n⚠️ Only scan networks you own "
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

        # -------------------------------------------------
        # Network Discovery
        # -------------------------------------------------

        scanner = NetworkScanner(
            network_input
        )

        devices = scanner.discover()

        # -------------------------------------------------
        # Network Risk Analysis
        # -------------------------------------------------

        analyzer = NetworkRiskAnalyzer(
            devices
        )

        analysis = analyzer.analyze_network()

        if analysis:

            # -------------------------------------------------
            # Threat Detection
            # -------------------------------------------------

            detector = ThreatDetector(
                analysis["devices"]
            )

            detector.detect()