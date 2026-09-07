# =========================================================
# ECHO-X
# Attack Simulation Engine - Step 27
# =========================================================

from network.auto_twin import AutomaticTwinBuilder
from detection.network_risk import NetworkRiskAnalyzer
from detection.threat_detector import ThreatDetector
from detection.attack_path_predictor import AttackPathPredictor


class AttackSimulation:

    def __init__(self, digital_twin):

        self.digital_twin = digital_twin
        self.simulation_results = []

    # =====================================================
    # CALCULATE DEVICE RISK
    # =====================================================

    def calculate_device_risk(self, device):

        security_level = device.security_level

        vulnerability = (
            100 - security_level
        )

        return max(
            vulnerability,
            0
        )

    # =====================================================
    # SIMULATE PATH
    # =====================================================

    def simulate_path(self, path):

        if not path:

            return None

        steps = []
        total_risk = 0

        print("\n")
        print("-" * 70)

        print(
            "              ATTACK SIMULATION"
        )

        print("-" * 70)

        print("\nSimulated Path:")

        print(
            " → ".join(path)
        )

        print("\n")

        # -------------------------------------------------
        # Simulate every device in the path
        # -------------------------------------------------

        for index, device_name in enumerate(
            path,
            start=1
        ):

            device = (
                self.digital_twin.devices.get(
                    device_name
                )
            )

            if not device:

                continue

            device_risk = (
                self.calculate_device_risk(
                    device
                )
            )

            total_risk += device_risk

            if device_risk >= 70:

                status = "HIGH RISK"

            elif device_risk >= 40:

                status = "MEDIUM RISK"

            else:

                status = "LOW RISK"

            step = {

                "step":
                    index,

                "device":
                    device_name,

                "device_type":
                    device.device_type,

                "security_level":
                    device.security_level,

                "risk":
                    device_risk,

                "status":
                    status
            }

            steps.append(
                step
            )

            print(
                f"[Step {index}] "
                f"{device_name}"
            )

            print(
                f"  Type: "
                f"{device.device_type}"
            )

            print(
                f"  Security Level: "
                f"{device.security_level}/100"
            )

            print(
                f"  Simulated Risk: "
                f"{device_risk}/100"
            )

            print(
                f"  Status: "
                f"{status}"
            )

        # -------------------------------------------------
        # Calculate simulation score
        # -------------------------------------------------

        average_risk = round(
            total_risk / len(steps),
            2
        ) if steps else 0

        if average_risk >= 80:

            simulation_level = "CRITICAL"

        elif average_risk >= 60:

            simulation_level = "HIGH"

        elif average_risk >= 40:

            simulation_level = "MEDIUM"

        else:

            simulation_level = "LOW"

        result = {

            "path":
                path,

            "steps":
                steps,

            "average_risk":
                average_risk,

            "simulation_level":
                simulation_level,

            "target_reached":
                True
        }

        self.simulation_results.append(
            result
        )

        # -------------------------------------------------
        # Final simulation result
        # -------------------------------------------------

        print("\n")
        print("=" * 70)

        print(
            "             SIMULATION RESULT"
        )

        print("=" * 70)

        print(
            f"\nPath Length: "
            f"{len(path)} devices"
        )

        print(
            f"Average Simulated Risk: "
            f"{average_risk}/100"
        )

        print(
            f"Simulation Threat Level: "
            f"{simulation_level}"
        )

        print(
            f"Target Reached: "
            f"{'YES' if result['target_reached'] else 'NO'}"
        )

        print("\n⚠️ Simulation completed.")

        print(
            "No real attack traffic was generated."
        )

        print("=" * 70)

        return result

    # =====================================================
    # SIMULATE PREDICTIONS
    # =====================================================

    def simulate_predictions(
        self,
        predictions
    ):

        if not predictions:

            print(
                "\n🟢 No predicted paths to simulate."
            )

            return []

        results = []

        for prediction in predictions:

            path = prediction.get(
                "path",
                []
            )

            if path:

                result = self.simulate_path(
                    path
                )

                if result:

                    result["threat_type"] = (
                        prediction.get(
                            "threat_type",
                            "Unknown"
                        )
                    )

                    result["severity"] = (
                        prediction.get(
                            "severity",
                            "UNKNOWN"
                        )
                    )

                    results.append(
                        result
                    )

        return results


# =========================================================
# MAIN TEST
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)

    print(
        "        ECHO-X ATTACK SIMULATION"
    )

    print(
        "                    STEP 27"
    )

    print("=" * 70)

    print(
        "\n⚠️ This is a DIGITAL TWIN simulation."
    )

    print(
        "No real attack traffic will be generated."
    )

    print(
        "Only use network discovery on authorized networks."
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

        print(
            "\n[1] Building Digital Twin..."
        )

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
                "\n[2] Network Risk Analysis..."
            )

            analyzer = NetworkRiskAnalyzer(
                builder.scanner.devices
            )

            analysis = (
                analyzer.analyze_network()
            )

            if analysis:

                # =================================================
                # STEP 3
                # THREAT DETECTION
                # =================================================

                print(
                    "\n[3] Threat Detection..."
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
                    "\n[4] Attack Path Prediction..."
                )

                predictor = AttackPathPredictor(
                    twin
                )

                predictions = (
                    predictor.predict(
                        threats
                    )
                )

                # =================================================
                # STEP 5
                # ATTACK SIMULATION
                # =================================================

                print(
                    "\n[5] Attack Simulation..."
                )

                simulator = AttackSimulation(
                    twin
                )

                results = (
                    simulator.simulate_predictions(
                        predictions
                    )
                )

                # =================================================
                # FINAL SUMMARY
                # =================================================

                print("\n")
                print("=" * 70)

                print(
                    "           ECHO-X STEP 27 COMPLETE"
                )

                print("=" * 70)

                print(
                    f"\nThreats Detected: "
                    f"{len(threats)}"
                )

                print(
                    f"Paths Predicted: "
                    f"{len(predictions)}"
                )

                print(
                    f"Paths Simulated: "
                    f"{len(results)}"
                )

                if results:

                    print(
                        "\n🔬 Attack simulation completed "
                        "inside the Digital Twin."
                    )

                else:

                    print(
                        "\n🟢 No attack simulation performed."
                    )

                print("\n" + "=" * 70)