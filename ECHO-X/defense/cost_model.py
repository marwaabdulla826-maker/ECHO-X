# =========================================================
# ECHO-X
# Defense Cost Model - Step 11
# =========================================================


class DefenseCostModel:

    def __init__(self):

        self.defense_costs = {

            "Block Connection": {
                "operational_cost": 40,
                "description":
                    "Blocks network communication "
                    "and may interrupt services."
            },

            "Isolate Employee PC": {
                "operational_cost": 15,
                "description":
                    "Isolates the compromised endpoint "
                    "with limited business impact."
            },

            "Disable Account": {
                "operational_cost": 10,
                "description":
                    "Disables the affected account "
                    "with low operational impact."
            },

            "Isolate + Disable": {
                "operational_cost": 25,
                "description":
                    "Combines endpoint isolation "
                    "and account disabling."
            }
        }

    def get_cost(self, defense_name):

        defense = self.defense_costs.get(
            defense_name
        )

        if defense is None:

            return 100

        return defense["operational_cost"]

    def get_description(self, defense_name):

        defense = self.defense_costs.get(
            defense_name
        )

        if defense is None:

            return "Unknown defense strategy."

        return defense["description"]

    def calculate_final_score(
        self,
        effectiveness,
        historical_effectiveness,
        blocked,
        defense_name
    ):

        operational_cost = self.get_cost(
            defense_name
        )

        score = 0

        # Current defense effectiveness
        score += (
            effectiveness * 0.50
        )

        # Historical performance
        score += (
            historical_effectiveness * 0.25
        )

        # Reward defenses that completely block the attack
        if blocked:

            score += 25

        # Penalize operational impact
        score -= (
            operational_cost * 0.25
        )

        return round(
            score,
            2
        )

    def evaluate(
        self,
        defense_result,
        historical_effectiveness
    ):

        defense_name = (
            defense_result["defense"]
        )

        effectiveness = (
            defense_result["effectiveness"]
        )

        blocked = (
            defense_result["blocked"]
        )

        operational_cost = (
            self.get_cost(
                defense_name
            )
        )

        final_score = (
            self.calculate_final_score(

                effectiveness,

                historical_effectiveness,

                blocked,

                defense_name
            )
        )

        return {

            "defense":
                defense_name,

            "effectiveness":
                effectiveness,

            "historical_effectiveness":
                historical_effectiveness,

            "blocked":
                blocked,

            "operational_cost":
                operational_cost,

            "final_score":
                final_score
        }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    model = DefenseCostModel()

    test_defense = {

        "defense":
            "Block Connection",

        "effectiveness":
            94.51,

        "blocked":
            True
    }

    result = model.evaluate(

        test_defense,

        historical_effectiveness=94.51
    )

    print("\n")

    print("=" * 65)

    print(
        "             ECHO-X DEFENSE COST MODEL"
    )

    print("=" * 65)

    print(
        f"\nDefense: "
        f"{result['defense']}"
    )

    print(
        f"Effectiveness: "
        f"{result['effectiveness']}%"
    )

    print(
        f"Historical Effectiveness: "
        f"{result['historical_effectiveness']}%"
    )

    print(
        f"Operational Cost: "
        f"{result['operational_cost']}/100"
    )

    print(
        f"Attack Blocked: "
        f"{'YES' if result['blocked'] else 'NO'}"
    )

    print(
        f"Final Score: "
        f"{result['final_score']}"
    )

    print("\n")

    print(
        "✓ Defense cost calculated"
    )

    print(
        "✓ Operational impact considered"
    )

    print(
        "✓ Final defense score generated"
    )

    print("\n")

    print("=" * 65)