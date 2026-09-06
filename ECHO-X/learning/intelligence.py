# =========================================================
# ECHO-X
# Real Learning & Adaptation Engine - Step 18
# =========================================================

from learning.memory import LearningMemory


class IntelligenceEngine:

    def __init__(self):

        self.memory = LearningMemory()

    # =====================================================
    # GET HISTORICAL PERFORMANCE
    # =====================================================

    def get_defense_history(self):

        history = {}

        # LearningMemory stores events inside self.records
        for event in self.memory.records:

            defense = event.get(
                "defense"
            )

            if defense not in history:

                history[defense] = {

                    "uses": 0,

                    "successful": 0,

                    "blocked": 0,

                    "effectiveness_total": 0
                }

            history[defense]["uses"] += 1

            history[defense][
                "effectiveness_total"
            ] += event.get(
                "effectiveness",
                0
            )

            if event.get(
                "blocked",
                False
            ):

                history[defense][
                    "blocked"
                ] += 1

            if event.get(
                "effectiveness",
                0
            ) > 0:

                history[defense][
                    "successful"
                ] += 1

        return history

    # =====================================================
    # GET BEST DEFENSE
    # =====================================================

    def get_best_defense(self):

        history = self.get_defense_history()

        if not history:

            return None

        best_defense = None

        best_score = -1

        for defense, data in history.items():

            uses = data["uses"]

            if uses == 0:

                continue

            average_effectiveness = (
                data["effectiveness_total"]
                / uses
            )

            block_rate = (
                data["blocked"]
                / uses
            ) * 100

            # -------------------------------------------------
            # LEARNING SCORE
            # -------------------------------------------------

            learning_score = (

                average_effectiveness * 0.60

                + block_rate * 0.40
            )

            if learning_score > best_score:

                best_score = learning_score

                best_defense = {

                    "defense":
                        defense,

                    "uses":
                        uses,

                    "successful":
                        data["successful"],

                    "blocked":
                        data["blocked"],

                    "average_effectiveness":
                        round(
                            average_effectiveness,
                            2
                        ),

                    "block_rate":
                        round(
                            block_rate,
                            2
                        ),

                    "learning_score":
                        round(
                            learning_score,
                            2
                        )
                }

        return best_defense

    # =====================================================
    # ADAPTATION RECOMMENDATION
    # =====================================================

    def get_adaptive_recommendation(
        self,
        defense_results
    ):

        history = self.get_defense_history()

        recommendations = []

        for result in defense_results:

            defense = result[
                "defense"
            ]

            current_effectiveness = (
                result[
                    "effectiveness"
                ]
            )

            historical_effectiveness = 0

            historical_uses = 0

            historical_block_rate = 0

            if defense in history:

                data = history[
                    defense
                ]

                historical_uses = (
                    data["uses"]
                )

                if historical_uses > 0:

                    historical_effectiveness = (

                        data[
                            "effectiveness_total"
                        ]
                        / historical_uses
                    )

                    historical_block_rate = (

                        data[
                            "blocked"
                        ]
                        / historical_uses
                    ) * 100

            # -------------------------------------------------
            # ADAPTIVE SCORE
            # -------------------------------------------------

            adaptive_score = (

                current_effectiveness * 0.45

                + historical_effectiveness * 0.30

                + historical_block_rate * 0.25
            )

            recommendations.append({

                "defense":
                    defense,

                "current_effectiveness":
                    round(
                        current_effectiveness,
                        2
                    ),

                "historical_effectiveness":
                    round(
                        historical_effectiveness,
                        2
                    ),

                "historical_uses":
                    historical_uses,

                "historical_block_rate":
                    round(
                        historical_block_rate,
                        2
                    ),

                "adaptive_score":
                    round(
                        adaptive_score,
                        2
                    )
            })

        if not recommendations:

            return None

        best = max(
            recommendations,
            key=lambda x:
                x["adaptive_score"]
        )

        return {

            "selected_defense":
                best["defense"],

            "adaptive_score":
                best["adaptive_score"],

            "recommendations":
                recommendations
        }

    # =====================================================
    # DISPLAY LEARNING
    # =====================================================

    def show_learning(
        self,
        result
    ):

        print("\n")
        print("=" * 70)
        print(
            "              ECHO-X LEARNING ENGINE"
        )
        print("=" * 70)

        print(
            "\n🧠 Historical Intelligence"
        )

        for item in result[
            "recommendations"
        ]:

            print(
                "\nDefense:",
                item["defense"]
            )

            print(
                "Current Effectiveness:",
                f"{item['current_effectiveness']}%"
            )

            print(
                "Historical Effectiveness:",
                f"{item['historical_effectiveness']}%"
            )

            print(
                "Historical Uses:",
                item["historical_uses"]
            )

            print(
                "Historical Block Rate:",
                f"{item['historical_block_rate']}%"
            )

            print(
                "Adaptive Score:",
                item["adaptive_score"]
            )

        print(
            "\n" + "-" * 70
        )

        print(
            "🧠 ADAPTIVE RECOMMENDATION:",
            result["selected_defense"]
        )

        print(
            "Adaptive Score:",
            result["adaptive_score"]
        )

        print(
            "=" * 70
        )