# =========================================================
# ECHO-X
# Context-Aware Defense Engine - Step 15
# =========================================================

import sys
import os
import copy

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from network.digital_twin import DigitalTwin


class DefenseEngine:

    def __init__(self, network):

        self.network = network

        self.results = []


    # =====================================================
    # IDENTIFY ATTACK SOURCE
    # =====================================================

    def get_attack_source(
        self,
        attack_path
    ):

        if not attack_path:

            return None

        return attack_path[0]


    # =====================================================
    # IDENTIFY ATTACK TARGET
    # =====================================================

    def get_attack_target(
        self,
        attack_path
    ):

        if not attack_path:

            return None

        return attack_path[-1]


    # =====================================================
    # CONTEXT-AWARE DEFENSE NAME
    # =====================================================

    def get_contextual_defense_name(
        self,
        defense_name,
        attack_source
    ):

        if defense_name == "Isolate Employee PC":

            return f"Isolate {attack_source}"

        if defense_name == "Disable Account":

            return f"Disable {attack_source} Account"

        if defense_name == "Isolate + Disable":

            return f"Isolate + Disable {attack_source}"

        return defense_name


    # =====================================================
    # BLOCK CONNECTION
    # =====================================================

    def block_connection(
        self,
        network,
        attack_path
    ):

        if len(attack_path) < 2:

            return


        source = attack_path[0]

        next_device = attack_path[1]


        # Remove connection from source
        if (
            next_device
            in
            network.connections.get(
                source,
                []
            )
        ):

            network.connections[
                source
            ].remove(
                next_device
            )


        # Remove reverse connection
        if (
            source
            in
            network.connections.get(
                next_device,
                []
            )
        ):

            network.connections[
                next_device
            ].remove(
                source
            )


    # =====================================================
    # SIMULATE DEFENSE
    # =====================================================

    def simulate_defense(
        self,
        attack_path,
        defense_name
    ):

        simulated_network = copy.deepcopy(
            self.network
        )


        # Calculate risk before defense
        risk_before = self.calculate_risk(
            attack_path,
            simulated_network
        )


        # Identify attack source
        attack_source = self.get_attack_source(
            attack_path
        )


        # Identify attack target
        attack_target = self.get_attack_target(
            attack_path
        )


        if attack_source is None:

            return {

                "defense":
                    defense_name,

                "display_name":
                    defense_name,

                "attack_source":
                    None,

                "target":
                    attack_target,

                "risk_before":
                    risk_before,

                "risk_after":
                    risk_before,

                "risk_reduction":
                    0,

                "effectiveness":
                    0,

                "blocked":
                    False
            }


        # Context-aware display name
        display_name = (
            self.get_contextual_defense_name(
                defense_name,
                attack_source
            )
        )


        # =================================================
        # DEFENSE 1
        # =================================================

        if defense_name == "Block Connection":

            self.block_connection(
                simulated_network,
                attack_path
            )


        # =================================================
        # DEFENSE 2
        # =================================================

        elif defense_name == "Isolate Employee PC":

            self.isolate_device(
                simulated_network,
                attack_source
            )


        # =================================================
        # DEFENSE 3
        # =================================================

        elif defense_name == "Disable Account":

            self.disable_device(
                simulated_network,
                attack_source
            )


        # =================================================
        # DEFENSE 4
        # =================================================

        elif defense_name == "Isolate + Disable":

            self.isolate_device(
                simulated_network,
                attack_source
            )

            self.disable_device(
                simulated_network,
                attack_source
            )


        # =================================================
        # CHECK REMAINING ATTACK PATH
        # =================================================

        remaining_path = self.find_path(

            simulated_network,

            attack_source,

            attack_target
        )


        if remaining_path:

            risk_after = self.calculate_risk(

                remaining_path,

                simulated_network
            )

            blocked = False

        else:

            risk_after = 5

            blocked = True


        # =================================================
        # CALCULATE EFFECTIVENESS
        # =================================================

        risk_reduction = max(

            0,

            risk_before - risk_after
        )


        if risk_before > 0:

            effectiveness = round(

                (
                    risk_reduction
                    /
                    risk_before
                )
                * 100,

                2
            )

        else:

            effectiveness = 0


        result = {

            # Internal name
            "defense":
                defense_name,

            # Context-aware name for display
            "display_name":
                display_name,

            "attack_source":
                attack_source,

            "target":
                attack_target,

            "risk_before":
                risk_before,

            "risk_after":
                risk_after,

            "risk_reduction":
                risk_reduction,

            "effectiveness":
                effectiveness,

            "blocked":
                blocked,

            "remaining_path":
                remaining_path
        }


        return result


    # =====================================================
    # ISOLATE DEVICE
    # =====================================================

    def isolate_device(
        self,
        network,
        device_name
    ):

        if device_name not in network.devices:

            return


        # Remove all outgoing connections
        network.connections[
            device_name
        ] = []


        # Remove incoming connections
        for device in network.connections:

            if (
                device_name
                in
                network.connections[
                    device
                ]
            ):

                network.connections[
                    device
                ].remove(
                    device_name
                )


        # Mark device as compromised
        network.devices[
            device_name
        ].compromised = True


    # =====================================================
    # DISABLE DEVICE / ACCOUNT
    # =====================================================

    def disable_device(
        self,
        network,
        device_name
    ):

        if device_name not in network.devices:

            return


        # Mark device as no longer compromised
        network.devices[
            device_name
        ].compromised = False


    # =====================================================
    # FIND ATTACK PATH
    # =====================================================

    def find_path(
        self,
        network,
        start,
        target
    ):

        queue = [
            [start]
        ]

        visited = set()


        while queue:

            path = queue.pop(0)

            current = path[-1]


            if current == target:

                return path


            if current in visited:

                continue


            visited.add(
                current
            )


            for neighbor in network.connections.get(

                current,

                []
            ):

                if neighbor not in visited:

                    queue.append(

                        path + [neighbor]
                    )


        return None


    # =====================================================
    # RISK CALCULATION
    # =====================================================

    def calculate_risk(
        self,
        attack_path,
        network
    ):

        risk = 0


        for device_name in attack_path:

            device = network.devices.get(
                device_name
            )


            if device:

                # Lower security means higher risk
                vulnerability = (
                    100
                    -
                    device.security_level
                )

                risk += (
                    vulnerability
                    * 0.40
                )


        # Longer attack paths increase risk
        risk += (
            len(attack_path)
            * 5
        )


        return min(

            round(risk),

            100
        )


    # =====================================================
    # EVALUATE ALL DEFENSES
    # =====================================================

    def evaluate_defenses(
        self,
        attack_path
    ):

        print("\n")

        print(
            "=" * 70
        )

        print(
            "        ECHO-X CONTEXT-AWARE DEFENSE"
        )

        print(
            "=" * 70
        )


        attack_source = (
            self.get_attack_source(
                attack_path
            )
        )


        attack_target = (
            self.get_attack_target(
                attack_path
            )
        )


        print(
            f"\n🚨 Attack Source:"
            f" {attack_source}"
        )


        print(
            f"🎯 Target:"
            f" {attack_target}"
        )


        print(
            "\nAttack Path:"
        )


        print(
            " → ".join(
                attack_path
            )
        )


        defenses = [

            "Block Connection",

            "Isolate Employee PC",

            "Disable Account",

            "Isolate + Disable"
        ]


        self.results = []


        for defense in defenses:

            result = (
                self.simulate_defense(

                    attack_path,

                    defense
                )
            )


            self.results.append(
                result
            )


        # =================================================
        # DISPLAY RESULTS
        # =================================================

        print(
            "\n" + "-" * 70
        )


        print(
            "              DEFENSE COMPARISON"
        )


        print(
            "-" * 70
        )


        for result in self.results:

            print(
                f"\n🛡️ {result['display_name']}"
            )


            print(
                f"   Internal Strategy:"
                f" {result['defense']}"
            )


            print(
                f"   Attack Source:"
                f" {result['attack_source']}"
            )


            print(
                f"   Risk Before:"
                f" {result['risk_before']}/100"
            )


            print(
                f"   Risk After:"
                f" {result['risk_after']}/100"
            )


            print(
                f"   Risk Reduction:"
                f" {result['risk_reduction']}"
            )


            print(
                f"   Effectiveness:"
                f" {result['effectiveness']}%"
            )


            print(
                f"   Attack Blocked:"
                f" {'YES' if result['blocked'] else 'NO'}"
            )


        # =================================================
        # SELECT BEST DEFENSE
        # =================================================

        best_defense = max(

            self.results,

            key=lambda result:
                (
                    result["blocked"],

                    result["effectiveness"]
                )
        )


        print(
            "\n" + "=" * 70
        )


        print(
            "🏆 BEST DEFENSE"
        )


        print(
            "=" * 70
        )


        print(
            f"\nDefense:"
            f" {best_defense['display_name']}"
        )


        print(
            f"Internal Strategy:"
            f" {best_defense['defense']}"
        )


        print(
            f"Attack Source:"
            f" {best_defense['attack_source']}"
        )


        print(
            f"Effectiveness:"
            f" {best_defense['effectiveness']}%"
        )


        print(
            f"Attack Blocked:"
            f" {'YES' if best_defense['blocked'] else 'NO'}"
        )


        print(
            "\n" + "=" * 70
        )


        return best_defense


# =========================================================
# TEST NETWORK
# =========================================================

def create_test_network():

    network = DigitalTwin()


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


    return network


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    network = create_test_network()


    engine = DefenseEngine(
        network
    )


    test_path = [

        "Admin PC",

        "App Server",

        "Database"
    ]


    engine.evaluate_defenses(
        test_path
    )