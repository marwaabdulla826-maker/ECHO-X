# =========================================================
# ECHO-X
# Confidence Engine - Step 13
# =========================================================


class ConfidenceEngine:

    def __init__(self):

        # Weights used to calculate confidence
        self.weights = {

            "current_performance": 0.40,

            "historical_performance": 0.30,

            "attack_blocked": 0.20,

            "historical_experience": 0.10
        }


    # =====================================================
    # CALCULATE CONFIDENCE
    # =====================================================

    def calculate_confidence(
        self,
        current_effectiveness,
        historical_effectiveness,
        blocked,
        historical_uses
    ):

        # Current defense performance
        current_score = (
            current_effectiveness
        )


        # Historical defense performance
        historical_score = (
            historical_effectiveness
        )


        # Block status
        blocked_score = 100 if blocked else 0


        # Historical experience
        if historical_uses >= 10:

            experience_score = 100

        elif historical_uses > 0:

            experience_score = (
                historical_uses * 10
            )

        else:

            experience_score = 0


        # =================================================
        # WEIGHTED CONFIDENCE
        # =================================================

        confidence = (

            current_score
            *
            self.weights[
                "current_performance"
            ]

            +

            historical_score
            *
            self.weights[
                "historical_performance"
            ]

            +

            blocked_score
            *
            self.weights[
                "attack_blocked"
            ]

            +

            experience_score
            *
            self.weights[
                "historical_experience"
            ]
        )


        return round(
            min(
                confidence,
                100
            ),
            2
        )


    # =====================================================
    # EVALUATE DEFENSE
    # =====================================================

    def evaluate(
        self,
        defense_result,
        historical_data
    ):

        current_effectiveness = (
            defense_result[
                "effectiveness"
            ]
        )


        blocked = (
            defense_result[
                "blocked"
            ]
        )


        historical_effectiveness = 0

        historical_uses = 0


        if historical_data:

            historical_uses = (
                historical_data.get(
                    "uses",
                    0
                )
            )


            effectiveness_total = (
                historical_data.get(
                    "effectiveness_total",
                    0
                )
            )


            if historical_uses > 0:

                historical_effectiveness = (

                    effectiveness_total
                    /
                    historical_uses
                )


        confidence = (
            self.calculate_confidence(

                current_effectiveness,

                historical_effectiveness,

                blocked,

                historical_uses
            )
        )


        return {

            "defense":
                defense_result[
                    "defense"
                ],

            "confidence":
                confidence,

            "current_effectiveness":
                current_effectiveness,

            "historical_effectiveness":
                round(
                    historical_effectiveness,
                    2
                ),

            "historical_uses":
                historical_uses,

            "blocked":
                blocked
        }


    # =====================================================
    # DISPLAY CONFIDENCE
    # =====================================================

    def show_confidence(
        self,
        result
    ):

        print("\n")

        print(
            "=" * 65
        )

        print(
            "              ECHO-X CONFIDENCE"
        )

        print(
            "=" * 65
        )


        print(
            f"\nDefense:"
            f" {result['defense']}"
        )


        print(
            f"Current Effectiveness:"
            f" {result['current_effectiveness']}%"
        )


        print(
            f"Historical Effectiveness:"
            f" {result['historical_effectiveness']}%"
        )


        print(
            f"Historical Uses:"
            f" {result['historical_uses']}"
        )


        print(
            f"Attack Blocked:"
            f" {'YES' if result['blocked'] else 'NO'}"
        )


        print(
            f"\n🧠 Confidence Score:"
            f" {result['confidence']}%"
        )


        print(
            "\n" + "=" * 65
        )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    engine = ConfidenceEngine()


    test_defense = {

        "defense":
            "Block Connection",

        "effectiveness":
            93.59,

        "blocked":
            True
    }


    test_history = {

        "uses":
            5,

        "effectiveness_total":
            470.40
    }


    result = engine.evaluate(

        test_defense,

        test_history
    )


    engine.show_confidence(
        result
    )