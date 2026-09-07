# =========================================================
# ECHO-X
# Learning Analytics Engine - Step 31
# =========================================================

from learning.memory import LearningMemory


class LearningAnalytics:

    def __init__(self):

        self.memory = LearningMemory()

        self.records = self.memory.records

    # =====================================================
    # GET TOTAL STATISTICS
    # =====================================================

    def get_total_statistics(self):

        total_events = len(
            self.records
        )

        blocked_events = 0

        effectiveness_total = 0

        successful_events = 0

        for event in self.records:

            if event.get(
                "blocked",
                False
            ):

                blocked_events += 1

            effectiveness = event.get(
                "effectiveness",
                0
            )

            effectiveness_total += effectiveness

            if effectiveness > 0:

                successful_events += 1

        if total_events > 0:

            block_rate = round(
                (
                    blocked_events
                    /
                    total_events
                ) * 100,
                2
            )

            average_effectiveness = round(
                effectiveness_total
                /
                total_events,
                2
            )

            success_rate = round(
                (
                    successful_events
                    /
                    total_events
                ) * 100,
                2
            )

        else:

            block_rate = 0

            average_effectiveness = 0

            success_rate = 0

        return {

            "total_events":
                total_events,

            "blocked_events":
                blocked_events,

            "successful_events":
                successful_events,

            "block_rate":
                block_rate,

            "average_effectiveness":
                average_effectiveness,

            "success_rate":
                success_rate
        }

    # =====================================================
    # ANALYZE DEFENSES
    # =====================================================

    def analyze_defenses(self):

        defense_data = {}

        for event in self.records:

            defense = event.get(
                "defense",
                "Unknown"
            )

            if defense not in defense_data:

                defense_data[defense] = {

                    "uses": 0,

                    "blocked": 0,

                    "successful": 0,

                    "effectiveness_total": 0
                }

            defense_data[
                defense
            ]["uses"] += 1

            effectiveness = event.get(
                "effectiveness",
                0
            )

            defense_data[
                defense
            ]["effectiveness_total"] += (
                effectiveness
            )

            if event.get(
                "blocked",
                False
            ):

                defense_data[
                    defense
                ]["blocked"] += 1

            if effectiveness > 0:

                defense_data[
                    defense
                ]["successful"] += 1

        results = []

        for defense, data in defense_data.items():

            uses = data["uses"]

            if uses > 0:

                average_effectiveness = round(
                    data[
                        "effectiveness_total"
                    ]
                    /
                    uses,
                    2
                )

                block_rate = round(
                    (
                        data["blocked"]
                        /
                        uses
                    ) * 100,
                    2
                )

                success_rate = round(
                    (
                        data["successful"]
                        /
                        uses
                    ) * 100,
                    2
                )

            else:

                average_effectiveness = 0

                block_rate = 0

                success_rate = 0

            # -------------------------------------------------
            # LEARNING SCORE
            # -------------------------------------------------

            learning_score = round(

                average_effectiveness
                * 0.60

                + block_rate
                * 0.40,

                2
            )

            results.append({

                "defense":
                    defense,

                "uses":
                    uses,

                "blocked":
                    data["blocked"],

                "successful":
                    data["successful"],

                "average_effectiveness":
                    average_effectiveness,

                "block_rate":
                    block_rate,

                "success_rate":
                    success_rate,

                "learning_score":
                    learning_score
            })

        # Highest learning score first

        results.sort(
            key=lambda x:
                x["learning_score"],
            reverse=True
        )

        return results

    # =====================================================
    # BEST DEFENSE
    # =====================================================

    def get_best_defense(self):

        defenses = (
            self.analyze_defenses()
        )

        if not defenses:

            return None

        return defenses[0]

    # =====================================================
    # LEARNING TREND
    # =====================================================

    def calculate_learning_trend(self):

        if len(self.records) < 2:

            return {

                "trend":
                    "INSUFFICIENT DATA",

                "change":
                    0
            }

        # -------------------------------------------------
        # Split history into two periods
        # -------------------------------------------------

        midpoint = len(
            self.records
        ) // 2

        first_half = (
            self.records[
                :midpoint
            ]
        )

        second_half = (
            self.records[
                midpoint:
            ]
        )

        first_effectiveness = 0

        second_effectiveness = 0

        # -------------------------------------------------
        # First half
        # -------------------------------------------------

        for event in first_half:

            first_effectiveness += event.get(
                "effectiveness",
                0
            )

        if first_half:

            first_average = (
                first_effectiveness
                /
                len(first_half)
            )

        else:

            first_average = 0

        # -------------------------------------------------
        # Second half
        # -------------------------------------------------

        for event in second_half:

            second_effectiveness += event.get(
                "effectiveness",
                0
            )

        if second_half:

            second_average = (
                second_effectiveness
                /
                len(second_half)
            )

        else:

            second_average = 0

        change = round(
            second_average
            -
            first_average,
            2
        )

        if change > 1:

            trend = "IMPROVING"

        elif change < -1:

            trend = "DECLINING"

        else:

            trend = "STABLE"

        return {

            "trend":
                trend,

            "change":
                change,

            "first_average":
                round(
                    first_average,
                    2
                ),

            "second_average":
                round(
                    second_average,
                    2
                )
        }

    # =====================================================
    # GET LATEST EVENT
    # =====================================================

    def get_latest_event(self):

        if not self.records:

            return None

        return self.records[-1]

    # =====================================================
    # GENERATE ANALYTICS
    # =====================================================

    def generate_report(self):

        statistics = (
            self.get_total_statistics()
        )

        defenses = (
            self.analyze_defenses()
        )

        best_defense = (
            self.get_best_defense()
        )

        trend = (
            self.calculate_learning_trend()
        )

        latest_event = (
            self.get_latest_event()
        )

        return {

            "statistics":
                statistics,

            "defenses":
                defenses,

            "best_defense":
                best_defense,

            "trend":
                trend,

            "latest_event":
                latest_event
        }

    # =====================================================
    # DISPLAY ANALYTICS
    # =====================================================

    def display_report(self):

        report = (
            self.generate_report()
        )

        statistics = (
            report["statistics"]
        )

        print("\n")
        print("=" * 70)

        print(
            "          ECHO-X LEARNING ANALYTICS"
        )

        print("=" * 70)

        # =================================================
        # OVERALL STATISTICS
        # =================================================

        print("\n")
        print(
            "📊 OVERALL LEARNING STATISTICS"
        )

        print("-" * 70)

        print(
            f"Total Events: "
            f"{statistics['total_events']}"
        )

        print(
            f"Successful Events: "
            f"{statistics['successful_events']}"
        )

        print(
            f"Blocked Events: "
            f"{statistics['blocked_events']}"
        )

        print(
            f"Success Rate: "
            f"{statistics['success_rate']}%"
        )

        print(
            f"Block Rate: "
            f"{statistics['block_rate']}%"
        )

        print(
            f"Average Effectiveness: "
            f"{statistics['average_effectiveness']}%"
        )

        # =================================================
        # DEFENSE PERFORMANCE
        # =================================================

        print("\n")
        print(
            "🛡️ DEFENSE PERFORMANCE"
        )

        print("-" * 70)

        if not report["defenses"]:

            print(
                "No defense history available."
            )

        else:

            for item in report["defenses"]:

                print("\n")

                print(
                    f"Defense: "
                    f"{item['defense']}"
                )

                print(
                    f"Uses: "
                    f"{item['uses']}"
                )

                print(
                    f"Successful: "
                    f"{item['successful']}"
                )

                print(
                    f"Blocked: "
                    f"{item['blocked']}"
                )

                print(
                    f"Average Effectiveness: "
                    f"{item['average_effectiveness']}%"
                )

                print(
                    f"Success Rate: "
                    f"{item['success_rate']}%"
                )

                print(
                    f"Block Rate: "
                    f"{item['block_rate']}%"
                )

                print(
                    f"Learning Score: "
                    f"{item['learning_score']}"
                )

        # =================================================
        # BEST DEFENSE
        # =================================================

        print("\n")
        print(
            "🏆 BEST HISTORICAL DEFENSE"
        )

        print("-" * 70)

        if report["best_defense"]:

            best = report[
                "best_defense"
            ]

            print(
                f"Defense: "
                f"{best['defense']}"
            )

            print(
                f"Learning Score: "
                f"{best['learning_score']}"
            )

            print(
                f"Average Effectiveness: "
                f"{best['average_effectiveness']}%"
            )

            print(
                f"Block Rate: "
                f"{best['block_rate']}%"
            )

        else:

            print(
                "No historical defense available."
            )

        # =================================================
        # LEARNING TREND
        # =================================================

        print("\n")
        print(
            "📈 LEARNING TREND"
        )

        print("-" * 70)

        trend = report[
            "trend"
        ]

        print(
            f"Trend: "
            f"{trend['trend']}"
        )

        if "change" in trend:

            print(
                f"Effectiveness Change: "
                f"{trend['change']}%"
            )

        if "first_average" in trend:

            print(
                f"Earlier Average: "
                f"{trend['first_average']}%"
            )

            print(
                f"Recent Average: "
                f"{trend['second_average']}%"
            )

        # =================================================
        # LATEST EVENT
        # =================================================

        print("\n")
        print(
            "🧠 LATEST LEARNING EVENT"
        )

        print("-" * 70)

        latest = report[
            "latest_event"
        ]

        if latest:

            print(
                f"Defense: "
                f"{latest.get('defense', 'Unknown')}"
            )

            print(
                f"Effectiveness: "
                f"{latest.get('effectiveness', 0)}%"
            )

            print(
                f"Blocked: "
                f"{'YES' if latest.get('blocked', False) else 'NO'}"
            )

            print(
                f"Threat Level: "
                f"{latest.get('threat_level', 'UNKNOWN')}"
            )

        else:

            print(
                "No learning events available."
            )

        print("\n")
        print("=" * 70)

        print(
            "ECHO-X STEP 31 COMPLETE"
        )

        print("=" * 70)

        return report


# =========================================================
# MAIN TEST
# =========================================================

if __name__ == "__main__":

    analytics = LearningAnalytics()

    analytics.display_report()