# =========================================================
# ECHO-X
# Learning Memory - Step 6
# =========================================================

import json
import os
from datetime import datetime


# =========================================================
# LEARNING MEMORY
# =========================================================

class LearningMemory:

    def __init__(self):

        self.memory_file = os.path.join(
            os.path.dirname(__file__),
            "echo_memory.json"
        )

        self.records = []

        self.load_memory()


    # -----------------------------------------------------
    # Load Previous Memory
    # -----------------------------------------------------

    def load_memory(self):

        if os.path.exists(self.memory_file):

            try:

                with open(
                    self.memory_file,
                    "r"
                ) as file:

                    self.records = json.load(file)

            except (json.JSONDecodeError, OSError):

                self.records = []

        else:

            self.records = []


    # -----------------------------------------------------
    # Save Memory
    # -----------------------------------------------------

    def save_memory(self):

        with open(
            self.memory_file,
            "w"
        ) as file:

            json.dump(
                self.records,
                file,
                indent=4
            )


    # -----------------------------------------------------
    # Save Alias for UI Compatibility
    # -----------------------------------------------------

    def save(self):
        self.save_memory()


    # -----------------------------------------------------
    # Record Security Event
    # -----------------------------------------------------

    def record_event(
        self,
        attack_path,
        threat_level,
        risk_score,
        defense,
        effectiveness,
        blocked
    ):

        event = {

            "timestamp":
                datetime.now().isoformat(),

            "attack_path":
                attack_path,

            "threat_level":
                threat_level,

            "risk_score":
                risk_score,

            "defense":
                defense,

            "effectiveness":
                effectiveness,

            "blocked":
                blocked
        }

        self.records.append(event)

        self.save_memory()

        print("\n🧠 Learning Memory Updated")

        print(
            f"Total Recorded Events: "
            f"{len(self.records)}"
        )


    # -----------------------------------------------------
    # Show Previous Events
    # -----------------------------------------------------

    def show_history(self):

        print("\n")
        print("=" * 65)
        print("              ECHO-X LEARNING MEMORY")
        print("=" * 65)

        if not self.records:

            print("\nNo previous security events.")

            return


        for index, event in enumerate(
            self.records,
            start=1
        ):

            print(
                f"\nEvent #{index}"
            )

            print(
                f"Attack Path: "
                f"{' → '.join(event['attack_path'])}"
            )

            print(
                f"Threat Level: "
                f"{event['threat_level']}"
            )

            print(
                f"Risk Score: "
                f"{event['risk_score']}/100"
            )

            print(
                f"Defense: "
                f"{event['defense']}"
            )

            print(
                f"Effectiveness: "
                f"{event['effectiveness']}%"
            )

            print(
                f"Blocked: "
                f"{'YES' if event['blocked'] else 'NO'}"
            )


        print("\n")
        print("=" * 65)


# =========================================================
# TEST LEARNING MEMORY
# =========================================================

if __name__ == "__main__":

    memory = LearningMemory()

    memory.record_event(

        attack_path=[
            "Employee PC",
            "Web Server",
            "App Server",
            "Database"
        ],

        threat_level="CRITICAL",

        risk_score=100,

        defense="Block Connection",

        effectiveness=94.51,

        blocked=True
    )

    memory.show_history()