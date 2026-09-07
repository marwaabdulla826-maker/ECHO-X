# =========================================================
# ECHO-X
# Attack Simulator - Step 2
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
# ATTACK SIMULATOR
# =========================================================

class AttackSimulator:

    def __init__(self, network):

        self.network = network

        self.attack_path = []

        self.attack_log = []


    # -----------------------------------------------------
    # Start Attack
    # -----------------------------------------------------

    def start_attack(self, start_device, target_device):

        print("\n" + "=" * 60)
        print("              ECHO-X ATTACK SIMULATOR")
        print("=" * 60)

        print(f"\n🎯 Starting Point : {start_device}")
        print(f"🎯 Target         : {target_device}")

        print("\n[+] Initializing attack simulation...")

        # Check devices exist

        if start_device not in self.network.devices:

            print(
                f"\n❌ Device not found: {start_device}"
            )

            return

        if target_device not in self.network.devices:

            print(
                f"\n❌ Device not found: {target_device}"
            )

            return

        # Find attack path

        path = self.find_attack_path(
            start_device,
            target_device
        )

        if not path:

            print(
                "\n❌ No possible attack path found."
            )

            return

        self.attack_path = path

        # Execute simulation

        self.simulate_attack(path)


    # -----------------------------------------------------
    # Find Path Through Network
    # -----------------------------------------------------

    def find_attack_path(
        self,
        start_device,
        target_device
    ):

        visited = set()

        queue = [
            [start_device]
        ]

        while queue:

            path = queue.pop(0)

            current_device = path[-1]

            if current_device == target_device:

                return path

            if current_device in visited:

                continue

            visited.add(current_device)

            neighbors = self.network.connections.get(
                current_device,
                []
            )

            for neighbor in neighbors:

                if neighbor not in visited:

                    new_path = path + [neighbor]

                    queue.append(new_path)

        return None


    # -----------------------------------------------------
    # Simulate Attack
    # -----------------------------------------------------

    def simulate_attack(self, path):

        print("\n" + "-" * 60)

        print("              ATTACK PATH DETECTED")

        print("-" * 60)

        print()

        for index, device in enumerate(path):

            step = index + 1

            print(
                f"Step {step}: "
                f"Attacker reached → {device}"
            )

            self.attack_log.append(
                {
                    "step": step,
                    "device": device,
                    "status": "REACHED"
                }
            )

        print("\n" + "-" * 60)

        print("              ATTACK COMPLETE")

        print("-" * 60)

        print(
            f"\nTotal systems traversed: "
            f"{len(path)}"
        )

        print(
            f"Attack path length: "
            f"{len(path) - 1}"
        )

        print(
            f"\nAttack Path:\n"
            f"{' → '.join(path)}"
        )

        print("\n⚠️ The target environment was reached.")

        print("=" * 60)


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
# CREATE ATTACK SIMULATOR
# =========================================================

attacker = AttackSimulator(
    network
)


# =========================================================
# RUN SIMULATION
# =========================================================

attacker.start_attack(
    "Employee PC",
    "Database"
)