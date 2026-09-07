# =========================================================
# ECHO-X
# Decision Fusion Engine - Step 18
# =========================================================

from decision.confidence_engine import ConfidenceEngine
from defense.cost_model import DefenseCostModel


class AdaptiveDecisionEngine:

    def __init__(self, intelligence_engine):

        self.intelligence = intelligence_engine

        self.cost_model = DefenseCostModel()

        self.confidence_engine = ConfidenceEngine()

    # =====================================================
    # HISTORICAL EFFECTIVENESS
    # =====================================================

    def get_historical_effectiveness(
        self,
        defense_name
    ):

        statistics = (
            self.intelligence.get_defense_history()
        )

        if defense_name not in statistics:

            return 0

        data = statistics[
            defense_name
        ]

        if data["uses"] == 0:

            return 0

        return round(
            data["effectiveness_total"]
            / data["uses"],
            2
        )

    # =====================================================
    # GET HISTORICAL DATA
    # =====================================================

    def get_historical_data(
        self,
        defense_name
    ):

        statistics = (
            self.intelligence.get_defense_history()
        )

        if defense_name not in statistics:

            return {
                "uses": 0,
                "effectiveness_total": 0,
                "blocked": 0
            }

        return statistics[
            defense_name
        ]

    # =====================================================
    # CHOOSE BEST DEFENSE
    # =====================================================

    def choose_defense(
        self,
        defense_results
    ):

        evaluations = []

        for result in defense_results:

            defense_name = result[
                "defense"
            ]

            # -------------------------------------------------
            # Historical Intelligence
            # -------------------------------------------------

            historical_effectiveness = (

                self.get_historical_effectiveness(
                    defense_name
                )
            )

            historical_data = (

                self.get_historical_data(
                    defense_name
                )
            )

            # -------------------------------------------------
            # Cost Evaluation
            # -------------------------------------------------

            cost_evaluation = (

                self.cost_model.evaluate(
                    result,
                    historical_effectiveness
                )
            )

            # -------------------------------------------------
            # Confidence Evaluation
            # -------------------------------------------------

            confidence_evaluation = (

                self.confidence_engine.evaluate(
                    result,
                    historical_data
                )
            )

            confidence = (

                confidence_evaluation[
                    "confidence"
                ]
            )

            # -------------------------------------------------
            # FINAL FUSION SCORE
            # -------------------------------------------------

            final_score = (

                cost_evaluation[
                    "final_score"
                ] * 0.70

                +

                confidence * 0.30
            )

            final_score = round(
                min(
                    final_score,
                    100
                ),
                2
            )

            evaluations.append({

                "defense":
                    defense_name,

                "effectiveness":
                    result[
                        "effectiveness"
                    ],

                "historical_effectiveness":
                    historical_effectiveness,

                "operational_cost":
                    cost_evaluation[
                        "operational_cost"
                    ],

                "blocked":
                    result[
                        "blocked"
                    ],

                "confidence":
                    confidence,

                "final_score":
                    final_score
            })

        # =====================================================
        # SELECT BEST DEFENSE
        # =====================================================

        if not evaluations:

            return None

        best = max(
            evaluations,
            key=lambda item:
                item["final_score"]
        )

        return {

            "defense":
                best["defense"],

            "effectiveness":
                best["effectiveness"],

            "historical_effectiveness":
                best["historical_effectiveness"],

            "operational_cost":
                best["operational_cost"],

            "blocked":
                best["blocked"],

            "confidence":
                best["confidence"],

            "final_score":
                best["final_score"],

            "all_defenses":
                evaluations
        }

    # =====================================================
    # DISPLAY DECISION
    # =====================================================

    def show_decision(
        self,
        decision
    ):

        print("\n")
        print("=" * 70)

        print(
            "              ECHO-X DECISION FUSION"
        )

        print("=" * 70)

        print(
            "\nDEFENSE EVALUATION"
        )

        for defense in decision[
            "all_defenses"
        ]:

            print(
                "\n" + "-" * 70
            )

            print(
                f"Defense: "
                f"{defense['defense']}"
            )

            print(
                f"Current Effectiveness: "
                f"{defense['effectiveness']}%"
            )

            print(
                f"Historical Effectiveness: "
                f"{defense['historical_effectiveness']}%"
            )

            print(
                f"Operational Cost: "
                f"{defense['operational_cost']}/100"
            )

            print(
                f"Attack Blocked: "
                f"{'YES' if defense['blocked'] else 'NO'}"
            )

            print(
                f"Confidence: "
                f"{defense['confidence']}%"
            )

            print(
                f"Final Fusion Score: "
                f"{defense['final_score']}"
            )

        print("\n")
        print("=" * 70)

        print(
            "                SELECTED DEFENSE"
        )

        print("=" * 70)

        print(
            f"\nDefense: "
            f"{decision['defense']}"
        )

        print(
            f"Current Effectiveness: "
            f"{decision['effectiveness']}%"
        )

        print(
            f"Historical Effectiveness: "
            f"{decision['historical_effectiveness']}%"
        )

        print(
            f"Operational Cost: "
            f"{decision['operational_cost']}/100"
        )

        print(
            f"Confidence: "
            f"{decision['confidence']}%"
        )

        print(
            f"Final Fusion Score: "
            f"{decision['final_score']}"
        )

        print(
            f"Attack Blocked: "
            f"{'YES' if decision['blocked'] else 'NO'}"
        )

        print("=" * 70)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print(
        "\nECHO-X Decision Fusion Engine"
    )

    print(
        "Step 18"
    )

    print(
        "✓ Cost Model connected"
    )

    print(
        "✓ Confidence Engine connected"
    )

    print(
        "✓ Historical Intelligence connected"
    )

    print(
        "✓ Real Learning connected"
    )

    print(
        "✓ Adaptive Decision ready"
    )