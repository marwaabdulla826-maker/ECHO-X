# =========================================================
# ECHO-X
# Attack Path Prediction Engine - Step 26
# =========================================================

from network.auto_twin import AutomaticTwinBuilder
from detection.network_risk import NetworkRiskAnalyzer
from detection.threat_detector import ThreatDetector


class AttackPathPredictor:

    def __init__(self, digital_twin):

        self.digital_twin = digital_twin
        self.predictions = []

    # =====================================================
    # FIND ATTACK PATH
    # =====================================================

    def find_path(self, start, target):

        visited = set()

        queue = [
            (start, [start])
        ]

        while queue:

            current, path = queue.pop(0)

            if current == target:

                return path

            if current in visited:

                continue

            visited.add(current)

            # Connections are stored in DigitalTwin,
            # not inside the Device object.

            connections = (
                self.digital_twin.connections.get(
                    current,
                    []
                )
            )

            for connection in connections:

                if connection not in visited:

                    queue.append(
                        (
                            connection,
                            path + [connection]
                        )
                    )

        return None

    # =====================================================
    # SELECT TARGET
    # =====================================================

    def select_target(self, source):

        devices = list(
            self.digital_twin.devices.keys()
        )

        if not devices:

            return None

        # Prefer Database devices

        for device_name in devices:

            if device_name == source:

                continue

            device = (
                self.digital_twin.devices[
                    device_name
                ]
            )

            if device.device_type == "Database":

                return device_name

        # Then prefer Server devices

        for device_name in devices:

            if device_name == source:

                continue

            device = (
                self.digital_twin.devices[
                    device_name
                ]
            )

            if device.device_type == "Server":

                return device_name

        # Otherwise select another device

        for device_name in devices:

            if device_name != source:

                return device_name

        return None

    # =====================================================
    # PREDICT ATTACK PATH
    # =====================================================

    def predict(self, threats):

        print("\n")
        print("=" * 70)

        print(
            "             ECHO-X ATTACK PATH PREDICTION"
        )

        print("=" * 70)

        if not threats:

            print(
                "\n🟢 No threats available for prediction."
            )

            return []

        self.predictions = []

        for threat in threats:

            source = threat.get(
                "device"
            )

            target = self.select_target(
                source
            )

            if not target:

                print(
                    f"\n⚠️ No target found for {source}"
                )

                continue

            path = self.find_path(
                source,
                target
            )

            if path:

                prediction = {

                    "source":
                        source,

                    "target":
                        target,

                    "path":
                        path,

                    "severity":
                        threat.get(
                            "severity",
                            "UNKNOWN"
                        ),

                    "risk_score":
                        threat.get(
                            "risk_score",
                            0
                        ),

                    "threat_type":
                        threat.get(
                            "threat_type",
                            "Unknown Threat"
                        )
                }

                self.predictions.append(
                    prediction
                )

            else:

                print(
                    f"\n⚠️ No path found from "
                    f"{source} to {target}"
                )

        self.display_predictions()

        return self.predictions

    # =====================================================
    # DISPLAY PREDICTIONS
    # =====================================================

    def display_predictions(self):

        print("\n")
        print("-" * 70)

        print(
            "              PREDICTED ATTACK PATHS"
        )

        print("-" * 70)

        if not self.predictions:

            print(
                "\n🟢 No attack paths could be predicted."
            )

            return

        for index, prediction in enumerate(
            self.predictions,
            start=1
        ):

            print("\n")

            print(
                f"🚨 PREDICTION #{index}"
            )

            print(
                f"Threat Type: "
                f"{prediction['threat_type']}"
            )

            print(
                f"Severity: "
                f"{prediction['severity']}"
            )

            print(
                f"Risk Score: "
                f"{prediction['risk_score']}/100"
            )

            print(
                f"Source: "
                f"{prediction['source']}"
            )

            print(
                f"Target: "
                f"{prediction['target']}"
            )

            print(
                "\nPredicted Attack Path:"
            )

            print(
                " → ".join(
                    prediction["path"]
                )
            )

            print(
                f"\nPath Length: "
                f"{len(prediction['path'])} devices"
            )

        print("\n")
        print("=" * 70)

        print(
            f"Attack Paths Predicted: "
            f"{len(self.predictions)}"
        )

        print("=" * 70)


# =========================================================
# MAIN TEST
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)

    print(
        "        ECHO-X ATTACK PATH PREDICTION"
    )

    print(
        "                    STEP 26"
    )

    print("=" * 70)

    print(
        "\n⚠️ Only use this system on networks "
        "you own or have permission to test."
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

        # =================================================
        # STEP 1
        # BUILD DIGITAL TWIN
        # =================================================

        print("\n[1] Building Digital Twin...")

        builder = AutomaticTwinBuilder(
            network_input
        )

        twin = builder.build()

        if twin:

            # =================================================
            # STEP 2
            # NETWORK RISK ANALYSIS
            # =================================================

            print(
                "\n[2] Analyzing Network Risk..."
            )

            analyzer = NetworkRiskAnalyzer(
                builder.scanner.devices
            )

            analysis = analyzer.analyze_network()

            if analysis:

                # =================================================
                # STEP 3
                # THREAT DETECTION
                # =================================================

                print(
                    "\n[3] Detecting Threats..."
                )

                detector = ThreatDetector(
                    analysis["devices"]
                )

                threats = detector.detect()

                # =================================================
                # STEP 4
                # ATTACK PATH PREDICTION
                # =================================================

                print(
                    "\n[4] Predicting Attack Paths..."
                )

                predictor = AttackPathPredictor(
                    twin
                )

                predictions = predictor.predict(
                    threats
                )

                # =================================================
                # FINAL STATUS
                # =================================================

                print("\n")
                print("=" * 70)

                print(
                    "              ECHO-X STEP 26 COMPLETE"
                )

                print("=" * 70)

                print(
                    f"\nThreats Detected: "
                    f"{len(threats)}"
                )

                print(
                    f"Attack Paths Predicted: "
                    f"{len(predictions)}"
                )

                if predictions:

                    print(
                        "\n🔴 Potential attack paths "
                        "identified in the Digital Twin."
                    )

                else:

                    print(
                        "\n🟢 No attack paths identified."
                    )

                print("\n" + "=" * 70)