# =========================================================
# ECHO-X
# Detection Engine - Step 3
# =========================================================

import sys
import os

# Allow Python to find the network module
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from network.digital_twin import DigitalTwin


# =========================================================
# DETECTION ENGINE
# =========================================================

class DetectionEngine:

    def __init__(self, network):

        self.network = network

        self.alerts = []


    # -----------------------------------------------------
    # Analyze Attack Path
    # -----------------------------------------------------

    def analyze_path(self, attack_path):

        print("\n" + "=" * 60)
        print("              ECHO-X DETECTION ENGINE")
        print("=" * 60)

        print("\n[+] Analyzing network activity...")

        risk_score = 0
        reasons = []

        # -----------------------------------------------
        # Rule 1: Compromised Endpoint
        # -----------------------------------------------

        if "Employee PC" in attack_path:

            risk_score += 25

            reasons.append(
                "Compromised employee endpoint detected."
            )


        # -----------------------------------------------
        # Rule 2: Lateral Movement
        # -----------------------------------------------

        if (
            "Web Server" in attack_path
            and "App Server" in attack_path
        ):

            risk_score += 25

            reasons.append(
                "Lateral movement between servers detected."
            )


        # -----------------------------------------------
        # Rule 3: Database Access
        # -----------------------------------------------

        if "Database" in attack_path:

            risk_score += 40

            reasons.append(
                "Unauthorized database access detected."
            )


        # -----------------------------------------------
        # Rule 4: Multiple Systems
        # -----------------------------------------------

        if len(attack_path) >= 4:

            risk_score += 10

            reasons.append(
                "Attack traversed multiple network assets."
            )


        # Make sure score doesn't exceed 100

        risk_score = min(
            risk_score,
            100
        )


        # Determine threat level

        threat_level = self.calculate_threat_level(
            risk_score
        )


        # -----------------------------------------------
        # Display Results
        # -----------------------------------------------

        print("\n" + "-" * 60)

        print("              THREAT ANALYSIS")

        print("-" * 60)

        print(
            f"\nRisk Score: {risk_score}/100"
        )

        print(
            f"Threat Level: {threat_level}"
        )


        print("\nDetected Indicators:")

        for reason in reasons:

            print(
                f"  🚨 {reason}"
            )


        # Save alert

        alert = {

            "attack_path": attack_path,

            "risk_score": risk_score,

            "threat_level": threat_level,

            "indicators": reasons
        }

        self.alerts.append(
            alert
        )


        print("\n" + "-" * 60)

        print(
            "Detection complete."
        )

        print("-" * 60)

        return alert


    # -----------------------------------------------------
    # Calculate Threat Level
    # -----------------------------------------------------

    def calculate_threat_level(
        self,
        risk_score
    ):

        if risk_score >= 80:

            return "CRITICAL"

        elif risk_score >= 60:

            return "HIGH"

        elif risk_score >= 40:

            return "MEDIUM"

        else:

            return "LOW"


# =========================================================
# CREATE DIGITAL TWIN
# =========================================================

network = DigitalTwin()


# =========================================================
# COMPANY DEVICES
# =========================================================

network.add_device(
    "Employee PC",
    "Endpoint",
    40
)

network.add_device(
    "Admin PC",
    "Endpoint",
    75
)

network.add_device(
    "Web Server",
    "Server",
    70
)

network.add_device(
    "App Server",
    "Server",
    80
)

network.add_device(
    "Database",
    "Database",
    95
)


# =========================================================
# NETWORK CONNECTIONS
# =========================================================

network.connect(
    "Employee PC",
    "Web Server"
)

network.connect(
    "Admin PC",
    "App Server"
)

network.connect(
    "Web Server",
    "App Server"
)

network.connect(
    "App Server",
    "Database"
)


# =========================================================
# SIMULATED ATTACK PATH
# =========================================================

attack_path = [

    "Employee PC",

    "Web Server",

    "App Server",

    "Database"
]


# =========================================================
# RUN DETECTION
# =========================================================

detector = DetectionEngine(
    network
)

result = detector.analyze_path(
    attack_path
)