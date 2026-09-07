# =========================================================
# ECHO-X
# Autonomous Defense Executor - Step 17
# =========================================================

class DefenseExecutor:

    def __init__(self, defense_engine):
        self.defense_engine = defense_engine

    # =====================================================
    # STEP 17
    # ATTACK RE-EVALUATION
    # =====================================================

    def reevaluate_attack(
        self,
        attack_path
    ):
        print("\n")
        print("=" * 70)
        print("              ECHO-X ATTACK RE-EVALUATION")
        print("=" * 70)

        print("\nBEFORE:")
        print(" → ".join(attack_path))

        remaining_path = self.defense_engine.find_path(
            self.defense_engine.network,
            attack_path[0],
            attack_path[-1]
        )

        print("\nAFTER:")

        if remaining_path is None:

            print("No Attack Path")

            status = "THREAT NEUTRALIZED"

        else:

            print(" → ".join(remaining_path))

            status = "THREAT STILL ACTIVE"

        print("\nSTATUS:")
        print(status)

        print("\n" + "=" * 70)

        return {
            "before_path": attack_path,
            "after_path": remaining_path,
            "status": status
        }

    # =====================================================
    # STEP 16
    # DEFENSE EXECUTION
    # =====================================================

    def execute(
        self,
        attack_path,
        selected_defense
    ):
        print("\n")
        print("=" * 70)
        print("              ECHO-X DEFENSE EXECUTION")
        print("=" * 70)

        print(
            f"\nSelected Defense: "
            f"{selected_defense['defense']}"
        )

        print(
            f"Attack Source: "
            f"{attack_path[0]}"
        )

        print(
            f"Target: "
            f"{attack_path[-1]}"
        )

        # -------------------------------------------------
        # Execute Selected Defense
        # -------------------------------------------------

        if selected_defense["defense"] == "Block Connection":

            self.defense_engine.block_connection(
                self.defense_engine.network,
                attack_path
            )

        elif selected_defense["defense"] == "Isolate Employee PC":

            self.defense_engine.isolate_device(
                self.defense_engine.network,
                attack_path[0]
            )

        elif selected_defense["defense"] == "Disable Account":

            self.defense_engine.disable_device(
                self.defense_engine.network,
                attack_path[0]
            )

        elif selected_defense["defense"] == "Isolate + Disable":

            self.defense_engine.isolate_device(
                self.defense_engine.network,
                attack_path[0]
            )

            self.defense_engine.disable_device(
                self.defense_engine.network,
                attack_path[0]
            )

        # -------------------------------------------------
        # Verify Attack Path
        # -------------------------------------------------

        remaining_path = self.defense_engine.find_path(
            self.defense_engine.network,
            attack_path[0],
            attack_path[-1]
        )

        print("\n[+] Verifying defense...")

        if remaining_path is None:

            blocked = True

            print(
                "🛡️ Attack successfully blocked."
            )

        else:

            blocked = False

            print(
                "⚠️ Attack path still exists."
            )

            print("Remaining Path:")

            print(
                " → ".join(remaining_path)
            )

        # -------------------------------------------------
        # Execution Result
        # -------------------------------------------------

        print("\n")
        print("-" * 70)
        print("              EXECUTION RESULT")
        print("-" * 70)

        print(
            f"\nDefense: "
            f"{selected_defense['defense']}"
        )

        print(
            f"Execution Status: "
            f"{'SUCCESS' if blocked else 'PARTIAL'}"
        )

        print(
            f"Attack Blocked: "
            f"{'YES' if blocked else 'NO'}"
        )

        print("-" * 70)

        return {
            "defense": selected_defense["defense"],
            "attack_source": attack_path[0],
            "target": attack_path[-1],
            "blocked": blocked,
            "remaining_path": remaining_path,
            "status": "SUCCESS" if blocked else "PARTIAL"
        }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    from network.digital_twin import DigitalTwin
    from defense.defense_engine import DefenseEngine

    network = DigitalTwin()

    network.add_device(
        "Employee PC",
        "Endpoint",
        40
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
        "Web Server",
        "App Server"
    )

    network.connect(
        "App Server",
        "Database"
    )

    defense_engine = DefenseEngine(
        network
    )

    executor = DefenseExecutor(
        defense_engine
    )

    attack_path = [
        "Employee PC",
        "Web Server",
        "App Server",
        "Database"
    ]

    selected_defense = {
        "defense": "Block Connection"
    }

    # -----------------------------------------------------
    # STEP 16
    # Execute Defense
    # -----------------------------------------------------

    execution_result = executor.execute(
        attack_path,
        selected_defense
    )

    # -----------------------------------------------------
    # STEP 17
    # Re-Evaluate Attack
    # -----------------------------------------------------

    reevaluation_result = executor.reevaluate_attack(
        attack_path
    )