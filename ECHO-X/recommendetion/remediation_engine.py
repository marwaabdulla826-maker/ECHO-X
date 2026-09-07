# =========================================================
# ECHO-X
# Security Recommendations & Remediation Engine
# Step 40
# =========================================================

class RemediationEngine:

    def __init__(self, threats):

        self.threats = threats

        self.recommendations = []


    def generate_recommendations(self):

        self.recommendations = []

        for threat in self.threats:

            port = threat.get("port")
            severity = threat.get("severity", "LOW")
            device = threat.get("device", "Unknown")
            ip = threat.get("ip", "Unknown")
            threat_type = threat.get(
                "threat_type",
                "Unknown Threat"
            )

            if port == 21:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "CRITICAL",
                    "action": "Disable FTP service",
                    "recommendation":
                        "Disable FTP if it is not required. "
                        "If file transfer is necessary, "
                        "use secure alternatives such as SFTP.",
                    "reason":
                        "FTP can transmit credentials and "
                        "data without adequate encryption."
                }

            elif port == 23:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "CRITICAL",
                    "action": "Disable Telnet",
                    "recommendation":
                        "Disable Telnet and replace it "
                        "with SSH for secure remote access.",
                    "reason":
                        "Telnet transmits communication "
                        "without encryption."
                }

            elif port == 445:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "HIGH",
                    "action": "Restrict SMB exposure",
                    "recommendation":
                        "Restrict SMB access using firewall "
                        "rules and allow access only from "
                        "trusted systems.",
                    "reason":
                        "Exposed SMB services can increase "
                        "the attack surface of Windows hosts."
                }

            elif port == 3389:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "HIGH",
                    "action": "Secure RDP access",
                    "recommendation":
                        "Restrict RDP to trusted networks "
                        "and use strong authentication.",
                    "reason":
                        "Exposed RDP can increase the risk "
                        "of unauthorized remote access."
                }

            elif port == 3306:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "HIGH",
                    "action": "Restrict database access",
                    "recommendation":
                        "Allow MySQL access only from "
                        "authorized application hosts.",
                    "reason":
                        "Database services should not be "
                        "directly exposed to untrusted networks."
                }

            elif port == 5432:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "HIGH",
                    "action": "Restrict PostgreSQL access",
                    "recommendation":
                        "Restrict PostgreSQL connections "
                        "to authorized application systems.",
                    "reason":
                        "Direct database exposure increases "
                        "the attack surface."
                }

            else:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "MEDIUM",
                    "action": "Review exposed service",
                    "recommendation":
                        "Review the exposed service and "
                        "restrict access to trusted systems.",
                    "reason":
                        "Unnecessary exposed services "
                        "increase the network attack surface."
                }

            self.recommendations.append(
                recommendation
            )

        return self.recommendations


    def get_priority_summary(self):

        summary = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }

        for recommendation in self.recommendations:

            priority = recommendation.get(
                "priority",
                "LOW"
            )

            if priority in summary:

                summary[priority] += 1

        return summary


    def display_recommendations(self):

        print("\n")
        print("=" * 75)
        print("       ECHO-X SECURITY REMEDIATION ENGINE")
        print("=" * 75)

        if not self.recommendations:

            print("\nNo security recommendations required.")
            return

        for index, recommendation in enumerate(
            self.recommendations,
            start=1
        ):

            print(
                f"\nRecommendation #{index}"
            )

            print(
                "Device:",
                recommendation["device"]
            )

            print(
                "IP:",
                recommendation["ip"]
            )

            print(
                "Threat:",
                recommendation["threat"]
            )

            print(
                "Severity:",
                recommendation["severity"]
            )

            print(
                "Priority:",
                recommendation["priority"]
            )

            print(
                "Action:",
                recommendation["action"]
            )

            print(
                "Recommendation:",
                recommendation["recommendation"]
            )

            print(
                "Reason:",
                recommendation["reason"]
            )

        summary = self.get_priority_summary()

        print("\n")
        print("=" * 75)
        print("REMEDIATION PRIORITY SUMMARY")
        print("=" * 75)

        for priority, count in summary.items():

            print(
                f"{priority}: {count}"
            )


if __name__ == "__main__":

    test_threats = [
        {
            "device": "DESKTOP-EH8RMSN",
            "ip": "192.168.100.64",
            "port": 445,
            "threat_type": "SMB Exposure",
            "severity": "HIGH",
            "risk_score": 25
        }
    ]

    engine = RemediationEngine(
        test_threats
    )

    engine.generate_recommendations()

    engine.display_recommendations()