# =========================================================
# ECHO-X
# Attack Scenario Engine - Step 9
# =========================================================

import sys
import os


# =========================================================
# PROJECT PATH
# =========================================================

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
# ATTACK SCENARIO ENGINE
# =========================================================

class AttackScenarioEngine:

    def __init__(self, network):

        self.network = network


    # -----------------------------------------------------
    # Get Available Attack Scenarios
    # -----------------------------------------------------

    def get_scenarios(self):

        scenarios = [

            {
                "id": 1,

                "name":
                    "Employee Endpoint Compromise",

                "attacker":
                    "Employee PC",

                "target":
                    "Database",

                "description":
                    "Attacker compromises an employee "
                    "endpoint and attempts lateral movement."
            },


            {
                "id": 2,

                "name":
                    "Web Server Attack",

                "attacker":
                    "Web Server",

                "target":
                    "Database",

                "description":
                    "Attacker gains access to the web server "
                    "and attempts to reach the database."
            },


            {
                "id": 3,

                "name":
                    "Admin Infrastructure Attack",

                "attacker":
                    "Admin PC",

                "target":
                    "Database",

                "description":
                    "Attacker compromises an administrative "
                    "endpoint and attempts privileged movement."
            }

        ]

        return scenarios


    # -----------------------------------------------------
    # Simulate Attack Scenario
    # -----------------------------------------------------

    def simulate_scenario(
        self,
        scenario
    ):

        attack_path = self.find_path(

            scenario["attacker"],

            scenario["target"]
        )


        result = {

            "id":
                scenario["id"],

            "name":
                scenario["name"],

            "attacker":
                scenario["attacker"],

            "target":
                scenario["target"],

            "description":
                scenario["description"],

            "path":
                attack_path
        }


        return result


    # -----------------------------------------------------
    # Find Attack Path
    # -----------------------------------------------------

    def find_path(
        self,
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


            visited.add(current)


            for neighbor in self.network.connections.get(
                current,
                []
            ):

                if neighbor not in visited:

                    queue.append(

                        path + [neighbor]

                    )


        return None


    # -----------------------------------------------------
    # Display Available Scenarios
    # -----------------------------------------------------

    def show_scenarios(self):

        print("\n")

        print(
            "=" * 65
        )

        print(
            "             ECHO-X ATTACK SCENARIOS"
        )

        print(
            "=" * 65
        )


        scenarios = self.get_scenarios()


        for scenario in scenarios:

            print(
                f"\n[{scenario['id']}] "
                f"{scenario['name']}"
            )

            print(
                f"Attacker: "
                f"{scenario['attacker']}"
            )

            print(
                f"Target: "
                f"{scenario['target']}"
            )

            print(
                f"Description: "
                f"{scenario['description']}"
            )


        print("\n")

        print(
            "=" * 65
        )


# =========================================================
# CREATE DIGITAL TWIN
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
# TEST ATTACK SCENARIOS
# =========================================================

if __name__ == "__main__":

    network = create_test_network()


    scenario_engine = AttackScenarioEngine(
        network
    )


    # -----------------------------------------------------
    # Display Scenarios
    # -----------------------------------------------------

    scenario_engine.show_scenarios()


    # -----------------------------------------------------
    # Test Every Scenario
    # -----------------------------------------------------

    print("\n")

    print(
        "=" * 65
    )

    print(
        "             ECHO-X SCENARIO TEST"
    )

    print(
        "=" * 65
    )


    scenarios = (
        scenario_engine.get_scenarios()
    )


    for scenario in scenarios:

        result = (
            scenario_engine.simulate_scenario(
                scenario
            )
        )


        print(
            f"\nScenario {result['id']}: "
            f"{result['name']}"
        )


        if result["path"]:

            print(
                "Attack Path:"
            )

            print(
                " → ".join(
                    result["path"]
                )
            )

        else:

            print(
                "❌ No attack path found."
            )


    print("\n")

    print(
        "=" * 65
    )

    print(
        "✓ Scenario testing complete"
    )

    print(
        "=" * 65
    )