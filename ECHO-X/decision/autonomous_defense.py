# =========================================================
# ECHO-X
# AUTONOMOUS DEFENSE ENGINE
#
# Detect → Analyze → Predict → Simulate
# → Decide → Defend → Verify → Learn
# =========================================================

from defense.defense_engine import DefenseEngine
from defense.cost_model import DefenseCostModel
from decision.confidence_engine import ConfidenceEngine
from learning.memory import LearningMemory

from network.auto_twin import AutomaticTwinBuilder
from detection.network_risk import NetworkRiskAnalyzer
from detection.threat_detector import ThreatDetector
from detection.attack_path_predictor import AttackPathPredictor
from simulator.attack_simulator import AttackSimulation


class AutonomousDefense:

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self, digital_twin):

        self.digital_twin = digital_twin

        self.defense_engine = (
            DefenseEngine(digital_twin)
            if digital_twin
            else None
        )

        self.cost_model = DefenseCostModel()
        self.confidence_engine = ConfidenceEngine()
        self.learning_memory = LearningMemory()

        self.selected_defense = None
        self.execution_result = None
        self.verification_result = None
        self.feedback_result = None
        self.updated_learning = None

    # =====================================================
    # ATTACK SOURCE
    # =====================================================

    def get_attack_source(self, attack_path):

        if not attack_path:
            return None

        return attack_path[0]

    # =====================================================
    # ATTACK TARGET
    # =====================================================

    def get_attack_target(self, attack_path):

        if not attack_path:
            return None

        return attack_path[-1]

    # =====================================================
    # CONTEXTUAL DEFENSE NAME
    # =====================================================

    def get_contextual_defense_name(
        self,
        defense_name,
        attack_path
    ):

        source = self.get_attack_source(
            attack_path
        )

        if not source:
            return defense_name

        if defense_name == "Isolate Employee PC":
            return f"Isolate {source}"

        if defense_name == "Disable Account":
            return f"Disable {source} Account"

        if defense_name == "Isolate + Disable":
            return f"Isolate + Disable {source}"

        return defense_name

    # =====================================================
    # NORMALIZE DEFENSE RESULTS
    # =====================================================

    def _get_valid_defense_results(
        self,
        attack_path
    ):

        if not self.defense_engine:
            return []

        results = getattr(
            self.defense_engine,
            "results",
            []
        )

        valid_results = []

        for result in results:

            # Already a dictionary
            if isinstance(result, dict):

                valid_results.append(result)

                continue

            # Old DefenseEngine versions may store
            # only the defense name as a string.
            if isinstance(result, str):

                try:

                    simulated = (
                        self.defense_engine.simulate_defense(
                            attack_path,
                            result
                        )
                    )

                    if isinstance(
                        simulated,
                        dict
                    ):
                        valid_results.append(
                            simulated
                        )

                except Exception:

                    continue

        return valid_results

    # =====================================================
    # HISTORICAL DATA
    # =====================================================

    def get_historical_data(
        self,
        defense_name
    ):

        records = getattr(
            self.learning_memory,
            "records",
            []
        )

        uses = 0
        effectiveness_total = 0
        blocked = 0

        for record in records:

            if not isinstance(
                record,
                dict
            ):
                continue

            if record.get(
                "defense"
            ) != defense_name:

                continue

            uses += 1

            effectiveness_total += float(
                record.get(
                    "effectiveness",
                    0
                )
            )

            if record.get(
                "blocked",
                False
            ):
                blocked += 1

        if uses > 0:

            historical_effectiveness = (
                effectiveness_total
                / uses
            )

            historical_block_rate = (
                blocked
                / uses
                * 100
            )

        else:

            historical_effectiveness = 0
            historical_block_rate = 0

        return {
            "uses": uses,
            "effectiveness_total":
                effectiveness_total,
            "historical_effectiveness":
                historical_effectiveness,
            "historical_block_rate":
                historical_block_rate,
            "blocked":
                blocked
        }

    # =====================================================
    # CHOOSE DEFENSE
    # =====================================================

    def choose_defense(
        self,
        attack_path
    ):

        if not attack_path:
            return None

        if not self.defense_engine:
            return None

        # Evaluate all available defenses
        self.defense_engine.evaluate_defenses(
            attack_path
        )

        defense_results = (
            self._get_valid_defense_results(
                attack_path
            )
        )

        if not defense_results:
            return None

        evaluations = []

        for defense_result in defense_results:

            defense_name = defense_result.get(
                "defense",
                "Unknown"
            )

            display_name = defense_result.get(
                "display_name",
                self.get_contextual_defense_name(
                    defense_name,
                    attack_path
                )
            )

            current_effectiveness = float(
                defense_result.get(
                    "effectiveness",
                    0
                )
            )

            blocked = bool(
                defense_result.get(
                    "blocked",
                    False
                )
            )

            historical_data = (
                self.get_historical_data(
                    defense_name
                )
            )

            historical_effectiveness = float(
                historical_data.get(
                    "historical_effectiveness",
                    0
                )
            )

            historical_block_rate = float(
                historical_data.get(
                    "historical_block_rate",
                    0
                )
            )

            historical_uses = int(
                historical_data.get(
                    "uses",
                    0
                )
            )

            # -------------------------------------------------
            # OPERATIONAL COST
            # -------------------------------------------------

            operational_cost = 0

            try:

                if hasattr(
                    self.cost_model,
                    "get_cost"
                ):

                    operational_cost = float(
                        self.cost_model.get_cost(
                            defense_name
                        )
                    )

                elif hasattr(
                    self.cost_model,
                    "costs"
                ):

                    operational_cost = float(
                        self.cost_model.costs.get(
                            defense_name,
                            0
                        )
                    )

                elif hasattr(
                    self.cost_model,
                    "defense_costs"
                ):

                    operational_cost = float(
                        self.cost_model.defense_costs.get(
                            defense_name,
                            0
                        )
                    )

            except Exception:

                operational_cost = 0

            # -------------------------------------------------
            # COST SCORE
            # -------------------------------------------------

            cost_score = 0

            cost_score += (
                current_effectiveness
                * 0.50
            )

            cost_score += (
                historical_effectiveness
                * 0.25
            )

            if blocked:

                cost_score += 25

            cost_score -= (
                operational_cost
                * 0.25
            )

            # -------------------------------------------------
            # CONFIDENCE
            # -------------------------------------------------

            confidence = 0

            try:

                confidence_result = (
                    self.confidence_engine.evaluate(
                        defense_result,
                        historical_data
                    )
                )

                if isinstance(
                    confidence_result,
                    dict
                ):

                    confidence = float(
                        confidence_result.get(
                            "confidence",
                            confidence_result.get(
                                "score",
                                0
                            )
                        )
                    )

                else:

                    confidence = float(
                        confidence_result
                    )

            except Exception:

                # Fallback confidence calculation
                # if the current ConfidenceEngine
                # has a different interface.

                confidence = (
                    current_effectiveness
                    * 0.40
                    + historical_effectiveness
                    * 0.30
                    + (20 if blocked else 0)
                    + min(
                        historical_uses * 10,
                        100
                    )
                    * 0.10
                )

            # -------------------------------------------------
            # FUSION SCORE
            # -------------------------------------------------

            fusion_score = (
                cost_score * 0.70
                + confidence * 0.30
            )

            evaluation = {

                "defense":
                    defense_name,

                "display_name":
                    display_name,

                "effectiveness":
                    current_effectiveness,

                "historical_effectiveness":
                    historical_effectiveness,

                "historical_uses":
                    historical_uses,

                "historical_block_rate":
                    historical_block_rate,

                "operational_cost":
                    operational_cost,

                "blocked":
                    blocked,

                "confidence":
                    confidence,

                "cost_score":
                    cost_score,

                "fusion_score":
                    fusion_score,

                "risk_before":
                    defense_result.get(
                        "risk_before",
                        0
                    ),

                "risk_after":
                    defense_result.get(
                        "risk_after",
                        0
                    ),

                "risk_reduction":
                    defense_result.get(
                        "risk_reduction",
                        0
                    )
            }

            evaluations.append(
                evaluation
            )

        if not evaluations:
            return None

        # -----------------------------------------------------
        # SELECT HIGHEST FUSION SCORE
        # -----------------------------------------------------

        best_defense = max(
            evaluations,
            key=lambda item:
                item.get(
                    "fusion_score",
                    0
                )
        )

        self.selected_defense = (
            best_defense
        )

        print("\n")
        print("=" * 70)
        print("           ADAPTIVE DEFENSE DECISION")
        print("=" * 70)

        for item in evaluations:

            print(
                f"\nDefense: "
                f"{item['display_name']}"
            )

            print(
                f"Current Effectiveness: "
                f"{item['effectiveness']:.2f}%"
            )

            print(
                f"Historical Effectiveness: "
                f"{item['historical_effectiveness']:.2f}%"
            )

            print(
                f"Historical Uses: "
                f"{item['historical_uses']}"
            )

            print(
                f"Operational Cost: "
                f"{item['operational_cost']:.2f}"
            )

            print(
                f"Confidence: "
                f"{item['confidence']:.2f}"
            )

            print(
                f"Fusion Score: "
                f"{item['fusion_score']:.2f}"
            )

        print("\n" + "-" * 70)

        print(
            f"BEST DEFENSE: "
            f"{best_defense['display_name']}"
        )

        print(
            f"Fusion Score: "
            f"{best_defense['fusion_score']:.2f}"
        )

        print("=" * 70)

        return best_defense

    # =====================================================
    # EXECUTE DEFENSE
    # =====================================================

    def execute_defense(
        self,
        attack_path,
        selected_defense
    ):

        if not attack_path:
            return None

        if not selected_defense:
            return None

        source = self.get_attack_source(
            attack_path
        )

        target = self.get_attack_target(
            attack_path
        )

        defense_name = selected_defense.get(
            "defense"
        )

        display_name = selected_defense.get(
            "display_name",
            defense_name
        )

        blocked = False

        # -------------------------------------------------
        # BLOCK CONNECTION
        # -------------------------------------------------

        if defense_name == "Block Connection":

            try:

                self.defense_engine.block_connection(
                    self.digital_twin,
                    attack_path
                )

            except TypeError:

                self.defense_engine.block_connection(
                    self.digital_twin
                )

        # -------------------------------------------------
        # ISOLATE DEVICE
        # -------------------------------------------------

        elif defense_name == "Isolate Employee PC":

            self.defense_engine.isolate_device(
                self.digital_twin,
                source
            )

        # -------------------------------------------------
        # DISABLE ACCOUNT
        # -------------------------------------------------

        elif defense_name == "Disable Account":

            self.defense_engine.disable_device(
                self.digital_twin,
                source
            )

        # -------------------------------------------------
        # ISOLATE + DISABLE
        # -------------------------------------------------

        elif defense_name == "Isolate + Disable":

            self.defense_engine.isolate_device(
                self.digital_twin,
                source
            )

            self.defense_engine.disable_device(
                self.digital_twin,
                source
            )

        # -------------------------------------------------
        # VERIFY PATH
        # -------------------------------------------------

        remaining_path = self.find_path(
            self.digital_twin,
            source,
            target
        )

        if not remaining_path:

            blocked = True

            status = "SUCCESS"

            success = True

            verified = True

            neutralized = True

        else:

            blocked = False

            status = "PARTIAL"

            success = False

            verified = False

            neutralized = False

        result = {

            "defense":
                defense_name,

            "display_name":
                display_name,

            "source":
                source,

            "target":
                target,

            "blocked":
                blocked,

            "remaining_path":
                remaining_path,

            "status":
                status,

            "success":
                success,

            "verified":
                verified,

            "neutralized":
                neutralized
        }

        self.execution_result = result

        print("\n")
        print("=" * 70)
        print("              DEFENSE EXECUTION")
        print("=" * 70)

        print(
            f"\nDefense: "
            f"{display_name}"
        )

        print(
            f"Source: "
            f"{source}"
        )

        print(
            f"Target: "
            f"{target}"
        )

        print(
            f"Status: "
            f"{status}"
        )

        print(
            f"Blocked: "
            f"{'YES' if blocked else 'NO'}"
        )

        if remaining_path:

            print(
                f"Remaining Path: "
                f"{' → '.join(map(str, remaining_path))}"
            )

        else:

            print(
                "Remaining Path: NONE"
            )

        print("=" * 70)

        return result

    # =====================================================
    # FIND PATH
    # =====================================================

    def find_path(
        self,
        network,
        start,
        target
    ):

        if not network:
            return []

        if not start or not target:
            return []

        connections = getattr(
            network,
            "connections",
            {}
        )

        queue = [
            [start]
        ]

        visited = set()

        while queue:

            path = queue.pop(
                0
            )

            current = path[-1]

            if current == target:

                return path

            if current in visited:

                continue

            visited.add(
                current
            )

            neighbors = []

            if isinstance(
                connections,
                dict
            ):

                neighbors = connections.get(
                    current,
                    []
                )

            elif isinstance(
                connections,
                list
            ):

                for connection in connections:

                    if not isinstance(
                        connection,
                        (list, tuple)
                    ):
                        continue

                    if len(connection) < 2:
                        continue

                    a = connection[0]
                    b = connection[1]

                    if a == current:
                        neighbors.append(b)

                    elif b == current:
                        neighbors.append(a)

            for neighbor in neighbors:

                if neighbor not in visited:

                    queue.append(
                        path + [neighbor]
                    )

        return []

    # =====================================================
    # VERIFY DEFENSE
    # =====================================================

    def verify_defense(
        self,
        attack_path
    ):

        if not attack_path:

            return None

        source = self.get_attack_source(
            attack_path
        )

        target = self.get_attack_target(
            attack_path
        )

        before = list(
            attack_path
        )

        after = self.find_path(
            self.digital_twin,
            source,
            target
        )

        neutralized = not bool(
            after
        )

        verified = neutralized

        if neutralized:

            status = "VERIFIED"

        else:

            status = "ACTIVE"

        result = {

            "before":
                before,

            "after":
                after,

            "status":
                status,

            "neutralized":
                neutralized,

            "verified":
                verified,

            "blocked":
                neutralized
        }

        self.verification_result = result

        print("\n")
        print("=" * 70)
        print("               DEFENSE VERIFICATION")
        print("=" * 70)

        print(
            f"\nStatus: "
            f"{status}"
        )

        print(
            f"Neutralized: "
            f"{'YES' if neutralized else 'NO'}"
        )

        if after:

            print(
                "Attack path remains active:"
            )

            print(
                " → ".join(
                    map(
                        str,
                        after
                    )
                )
            )

        else:

            print(
                "Attack path successfully neutralized."
            )

        print("=" * 70)

        return result

    # =====================================================
    # RECORD FEEDBACK / LEARNING
    # =====================================================

    def record_feedback(
        self,
        attack_path,
        threat,
        selected_defense,
        execution_result
    ):

        if not selected_defense:
            return None

        if not execution_result:
            return None

        actual_blocked = bool(
            execution_result.get(
                "blocked",
                False
            )
        )

        verified = bool(
            execution_result.get(
                "verified",
                False
            )
        )

        neutralized = bool(
            execution_result.get(
                "neutralized",
                False
            )
        )

        simulated_effectiveness = float(
            selected_defense.get(
                "effectiveness",
                0
            )
        )

        if verified or actual_blocked:

            actual_effectiveness = 100.0

        else:

            actual_effectiveness = (
                simulated_effectiveness
            )

        if isinstance(
            threat,
            dict
        ):

            threat_level = threat.get(
                "severity",
                threat.get(
                    "threat_level",
                    "UNKNOWN"
                )
            )

            risk_score = threat.get(
                "risk_score",
                0
            )

        else:

            threat_level = "UNKNOWN"
            risk_score = 0

        defense_name = selected_defense.get(
            "defense",
            "Unknown"
        )

        display_name = selected_defense.get(
            "display_name",
            defense_name
        )

        event = {

            "timestamp":
                __import__(
                    "datetime"
                ).datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "attack_path":
                list(attack_path),

            "threat_level":
                threat_level,

            "risk_score":
                risk_score,

            "defense":
                defense_name,

            "display_name":
                display_name,

            "simulated_effectiveness":
                simulated_effectiveness,

            "effectiveness":
                actual_effectiveness,

            "blocked":
                actual_blocked,

            "verified":
                verified,

            "neutralized":
                neutralized,

            "execution_status":
                execution_result.get(
                    "status",
                    "UNKNOWN"
                ),

            "verification_status":
                (
                    "VERIFIED"
                    if verified
                    else "NOT VERIFIED"
                )
        }

        # -------------------------------------------------
        # SAVE EVENT
        # -------------------------------------------------

        self.learning_memory.records.append(
            event
        )

        # IMPORTANT:
        # LearningMemory uses save_memory()
        # NOT save()

        self.learning_memory.save_memory()

        self.feedback_result = event

        print("\n")
        print("=" * 70)
        print("             LEARNING FEEDBACK")
        print("=" * 70)

        print(
            f"\nDefense: "
            f"{display_name}"
        )

        print(
            f"Effectiveness: "
            f"{actual_effectiveness:.2f}%"
        )

        print(
            f"Blocked: "
            f"{'YES' if actual_blocked else 'NO'}"
        )

        print(
            f"Verified: "
            f"{'YES' if verified else 'NO'}"
        )

        print(
            "\n🧠 Learning memory updated."
        )

        print("=" * 70)

        return event

    # =====================================================
    # UPDATED LEARNING
    # =====================================================

    def show_updated_learning(
        self,
        defense_name
    ):

        historical_data = (
            self.get_historical_data(
                defense_name
            )
        )

        self.updated_learning = (
            historical_data
        )

        print("\n")
        print("=" * 70)
        print("              UPDATED LEARNING MODEL")
        print("=" * 70)

        print(
            f"\nDefense: "
            f"{defense_name}"
        )

        print(
            f"Updated Historical Uses: "
            f"{historical_data['uses']}"
        )

        print(
            f"Updated Historical Effectiveness: "
            f"{historical_data['historical_effectiveness']:.2f}%"
        )

        print(
            f"Updated Historical Block Rate: "
            f"{historical_data['historical_block_rate']:.2f}%"
        )

        print(
            "\n🧠 ECHO-X has learned from "
            "the latest defense execution."
        )

        print("=" * 70)

        return historical_data

    # =====================================================
    # COMPLETE DEFENSE CYCLE
    # =====================================================

    def run_defense_cycle(
        self,
        attack_path,
        threat
    ):

        print("\n")
        print("=" * 70)
        print("        ECHO-X AUTONOMOUS DEFENSE CYCLE")
        print("=" * 70)

        if not attack_path:

            print(
                "\n❌ Cannot start defense cycle."
            )

            return None

        if not threat:

            print(
                "\n❌ No threat information available."
            )

            return None

        # -------------------------------------------------
        # STEP 1 — DECIDE
        # -------------------------------------------------

        selected_defense = (
            self.choose_defense(
                attack_path
            )
        )

        if not selected_defense:

            print(
                "\n❌ No defense could be selected."
            )

            return None

        # -------------------------------------------------
        # STEP 2 — DEFEND
        # -------------------------------------------------

        execution_result = (
            self.execute_defense(
                attack_path,
                selected_defense
            )
        )

        if not execution_result:

            return None

        # -------------------------------------------------
        # STEP 3 — VERIFY
        # -------------------------------------------------

        verification = (
            self.verify_defense(
                attack_path
            )
        )

        # -------------------------------------------------
        # STEP 4 — LEARN
        # -------------------------------------------------

        feedback = (
            self.record_feedback(
                attack_path,
                threat,
                selected_defense,
                execution_result
            )
        )

        # -------------------------------------------------
        # STEP 5 — UPDATE LEARNING
        # -------------------------------------------------

        updated_learning = (
            self.show_updated_learning(
                selected_defense.get(
                    "defense",
                    "Unknown"
                )
            )
        )

        # -------------------------------------------------
        # FINAL SUMMARY
        # -------------------------------------------------

        print("\n")
        print("=" * 70)
        print("       🧠 AUTONOMOUS DEFENSE CYCLE COMPLETE")
        print("=" * 70)

        print(
            f"\nSelected Defense: "
            f"{selected_defense.get('display_name', 'Unknown')}"
        )

        print(
            f"Fusion Score: "
            f"{selected_defense.get('fusion_score', 0):.2f}"
        )

        print(
            f"Execution: "
            f"{execution_result.get('status', 'UNKNOWN')}"
        )

        print(
            f"Verification: "
            f"{verification.get('status', 'UNKNOWN') if verification else 'UNKNOWN'}"
        )

        print(
            f"Learning: "
            f"{'UPDATED' if feedback else 'NOT UPDATED'}"
        )

        print("=" * 70)

        return {

            "selected_defense":
                selected_defense,

            "execution":
                execution_result,

            "verification":
                verification,

            "feedback":
                feedback,

            "updated_learning":
                updated_learning
        }


# =========================================================
# STEP 30 — FULL AUTONOMOUS PIPELINE
# =========================================================

def run_step_30(
    network_input
):

    print("\n")
    print("=" * 70)
    print("              ECHO-X STEP 30")
    print("       FULL AUTONOMOUS DEFENSE PIPELINE")
    print("=" * 70)

    # =====================================================
    # 1 — BUILD DIGITAL TWIN
    # =====================================================

    print("\n[1] Building Automatic Digital Twin...")

    builder = AutomaticTwinBuilder(
        network_input
    )

    twin = builder.build()

    if not twin:

        print(
            "❌ Digital Twin creation failed."
        )

        return None

    # =====================================================
    # 2 — NETWORK RISK ANALYSIS
    # =====================================================

    print("\n[2] Analyzing Network Risk...")

    devices = getattr(
        builder.scanner,
        "devices",
        []
    )

    analyzer = NetworkRiskAnalyzer(
        devices
    )

    analysis = (
        analyzer.analyze_network()
    )

    # =====================================================
    # 3 — THREAT DETECTION
    # =====================================================

    print("\n[3] Detecting Threats...")

    threat_detector = ThreatDetector(
        analysis.get(
            "devices",
            devices
        )
    )

    threats = (
        threat_detector.detect()
    )

    # =====================================================
    # 4 — ATTACK PATH PREDICTION
    # =====================================================

    print("\n[4] Predicting Attack Paths...")

    predictor = AttackPathPredictor(
        twin
    )

    predictions = (
        predictor.predict(
            threats
        )
    )

    # =====================================================
    # 5 — ATTACK SIMULATION
    # =====================================================

    print("\n[5] Simulating Attacks...")

    simulator = AttackSimulation(
        twin
    )

    simulation_results = (
        simulator.simulate_predictions(
            predictions
        )
    )

    # =====================================================
    # 6 — SELECT ATTACK PATH
    # =====================================================

    attack_path = []

    if predictions:

        first_prediction = predictions[0]

        if isinstance(
            first_prediction,
            dict
        ):

            attack_path = (
                first_prediction.get(
                    "path",
                    []
                )
            )

    # =====================================================
    # 7 — SELECT THREAT
    # =====================================================

    threat = None

    if threats:

        threat = threats[0]

    # =====================================================
    # 8 — AUTONOMOUS DEFENSE
    # =====================================================

    selected_defense = None
    execution = None
    verification = None
    feedback = None
    updated_learning = None

    if attack_path and threat:

        print(
            "\n[6] Starting Autonomous Defense..."
        )

        autonomous_defense = (
            AutonomousDefense(
                twin
            )
        )

        cycle_result = (
            autonomous_defense.run_defense_cycle(
                attack_path,
                threat
            )
        )

        if cycle_result:

            selected_defense = (
                cycle_result.get(
                    "selected_defense"
                )
            )

            execution = (
                cycle_result.get(
                    "execution"
                )
            )

            verification = (
                cycle_result.get(
                    "verification"
                )
            )

            feedback = (
                cycle_result.get(
                    "feedback"
                )
            )

            updated_learning = (
                cycle_result.get(
                    "updated_learning"
                )
            )

    # =====================================================
    # FINAL RESULT
    # =====================================================

    print("\n")
    print("=" * 70)
    print("             ECHO-X STEP 30 COMPLETE")
    print("=" * 70)

    return {

        "threats":
            threats,

        "predictions":
            predictions,

        "simulation_results":
            simulation_results,

        "selected_defense":
            selected_defense,

        "execution":
            execution,

        "verification":
            verification,

        "feedback":
            feedback,

        "updated_learning":
            updated_learning
    }


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    test_network = (
        "192.168.100.0/24"
    )

    result = run_step_30(
        test_network
    )

    print("\n")
    print("=" * 70)
    print("                  FINAL RESULT")
    print("=" * 70)

    if result:

        print(
            f"\nThreats: "
            f"{len(result.get('threats', []))}"
        )

        print(
            f"Predictions: "
            f"{len(result.get('predictions', []))}"
        )

        selected = result.get(
            "selected_defense"
        )

        if selected:

            print(
                f"Selected Defense: "
                f"{selected.get('display_name', 'Unknown')}"
            )

        execution = result.get(
            "execution"
        )

        if execution:

            print(
                f"Execution Status: "
                f"{execution.get('status', 'UNKNOWN')}"
            )

        verification = result.get(
            "verification"
        )

        if verification:

            print(
                f"Verification: "
                f"{verification.get('status', 'UNKNOWN')}"
            )

        feedback = result.get(
            "feedback"
        )

        print(
            f"Learning Updated: "
            f"{'YES' if feedback else 'NO'}"
        )

    else:

        print(
            "\n❌ ECHO-X pipeline failed."
        )

    print("=" * 70)