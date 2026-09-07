# =========================================================
# ECHO-X
# Autonomous Attack/Defense Loop - Step 19
# =========================================================

from defense.executor import DefenseExecutor


class AutonomousDefenseLoop:

    def __init__(
        self,
        defense_engine,
        intelligence_engine,
        adaptive_engine
    ):

        self.defense_engine = defense_engine

        self.intelligence = intelligence_engine

        self.adaptive_engine = adaptive_engine

        self.executor = DefenseExecutor(
            defense_engine
        )

    # =====================================================
    # RUN AUTONOMOUS DEFENSE CYCLE
    # =====================================================

    def run_cycle(
        self,
        attack_path,
        defense_results
    ):

        print("\n")
        print("=" * 70)

        print(
            "          ECHO-X AUTONOMOUS DEFENSE LOOP"
        )

        print("=" * 70)

        print("\n🚨 Threat detected")

        print(
            "Attack Path:"
        )

        print(
            " → ".join(attack_path)
        )

        # =================================================
        # CYCLE 1
        # =================================================

        print("\n")
        print("-" * 70)

        print(
            "                DEFENSE CYCLE 1"
        )

        print("-" * 70)

        # -------------------------------------------------
        # SELECT BEST DEFENSE
        # -------------------------------------------------

        decision = (
            self.adaptive_engine.choose_defense(
                defense_results
            )
        )

        if decision is None:

            print(
                "\n❌ No defense available."
            )

            return {
                "status": "NO DEFENSE",
                "blocked": False
            }

        print(
            f"\n🤖 Selected Defense: "
            f"{decision['defense']}"
        )

        print(
            f"🧠 Confidence: "
            f"{decision['confidence']}%"
        )

        print(
            f"📊 Fusion Score: "
            f"{decision['final_score']}"
        )

        # -------------------------------------------------
        # FIND SELECTED DEFENSE RESULT
        # -------------------------------------------------

        selected_defense = None

        for result in defense_results:

            if (
                result["defense"]
                == decision["defense"]
            ):

                selected_defense = result

                break

        if selected_defense is None:

            print(
                "\n❌ Selected defense result not found."
            )

            return {
                "status": "ERROR",
                "blocked": False
            }

        # -------------------------------------------------
        # EXECUTE DEFENSE
        # -------------------------------------------------

        execution = self.executor.execute(
            attack_path,
            selected_defense
        )

        # -------------------------------------------------
        # RE-EVALUATE ATTACK
        # -------------------------------------------------

        reevaluation = (
            self.executor.reevaluate_attack(
                attack_path
            )
        )

        # =================================================
        # CHECK RESULT
        # =================================================

        if reevaluation["status"] == "THREAT NEUTRALIZED":

            print("\n")
            print("=" * 70)

            print(
                "🛡️ AUTONOMOUS DEFENSE SUCCESSFUL"
            )

            print(
                "Threat was neutralized."
            )

            print("=" * 70)

            return {

                "status":
                    "THREAT NEUTRALIZED",

                "blocked":
                    execution["blocked"],

                "defense":
                    decision["defense"],

                "confidence":
                    decision["confidence"],

                "fusion_score":
                    decision["final_score"]
            }

        # =================================================
        # THREAT STILL ACTIVE
        # =================================================

        print("\n")
        print(
            "⚠️ Threat still active."
        )

        print(
            "🔄 Autonomous loop will continue."
        )

        return {

            "status":
                "THREAT STILL ACTIVE",

            "blocked":
                False,

            "defense":
                decision["defense"],

            "confidence":
                decision["confidence"],

            "fusion_score":
                decision["final_score"]
        }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)

    print(
        "        ECHO-X AUTONOMOUS DEFENSE LOOP"
    )

    print(
        "                    STEP 19"
    )

    print("=" * 70)

    print(
        "\n✓ Autonomous loop module created"
    )

    print(
        "✓ Defense Executor connected"
    )

    print(
        "✓ Adaptive Decision Engine ready"
    )

    print(
        "✓ Autonomous defense cycle ready"
    )