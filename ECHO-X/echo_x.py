# =========================================================
# ECHO-X
# Autonomous Adaptive Cyber Defense System
# Step 19 - Autonomous Attack/Defense Loop
# =========================================================

from network.digital_twin import DigitalTwin
from simulator.attack import AttackSimulator
from simulator.scenarios import AttackScenarioEngine
from detection.detector import DetectionEngine
from defense.defense_engine import DefenseEngine
from defense.executor import DefenseExecutor
from defense.autonomous_loop import AutonomousDefenseLoop
from learning.memory import LearningMemory
from learning.intelligence import IntelligenceEngine
from decision.adaptive_decision import AdaptiveDecisionEngine


# =========================================================
# CREATE DIGITAL TWIN
# =========================================================

def create_network():

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
# RUN ATTACK SCENARIO
# =========================================================

def run_scenario(network, scenario):

    print("\n")
    print("=" * 70)

    print(
        f"              SCENARIO {scenario['id']}"
    )

    print(
        f"              {scenario['name']}"
    )

    print("=" * 70)

    print(
        f"\nAttacker: {scenario['attacker']}"
    )

    print(
        f"Target: {scenario['target']}"
    )

    print(
        f"Description: {scenario['description']}"
    )

    # =====================================================
    # 1. ATTACK SIMULATION
    # =====================================================

    simulator = AttackSimulator(network)

    attack_path = simulator.find_attack_path(
        scenario["attacker"],
        scenario["target"]
    )

    if attack_path is None:

        print("\n❌ No attack path found.")

        return None

    print("\n🚨 Attack Path:")

    print(
        " → ".join(attack_path)
    )

    # =====================================================
    # 2. DETECTION
    # =====================================================

    print("\n[1] Detection Engine")

    detector = DetectionEngine(network)

    detection_result = detector.analyze_path(
        attack_path
    )

    print(
        f"Risk Score: "
        f"{detection_result['risk_score']}/100"
    )

    print(
        f"Threat Level: "
        f"{detection_result['threat_level']}"
    )

    # =====================================================
    # 3. DEFENSE SIMULATION
    # =====================================================

    print("\n[2] Defense Simulation")

    defense_engine = DefenseEngine(network)

    defenses = [
        "Block Connection",
        "Isolate Employee PC",
        "Disable Account",
        "Isolate + Disable"
    ]

    defense_results = []

    for defense in defenses:

        result = defense_engine.simulate_defense(
            attack_path,
            defense
        )

        defense_results.append(result)

    print(
        "✓ Defense strategies simulated"
    )

    # =====================================================
    # 4. HISTORICAL INTELLIGENCE
    # =====================================================

    print("\n[3] Historical Intelligence")

    intelligence = IntelligenceEngine()

    historical_best = (
        intelligence.get_best_defense()
    )

    if historical_best is not None:

        print(
            f"Previous Best Defense: "
            f"{historical_best['defense']}"
        )

        print(
            f"Historical Effectiveness: "
            f"{historical_best['average_effectiveness']}%"
        )

        print(
            f"Historical Block Rate: "
            f"{historical_best['block_rate']}%"
        )

    else:

        print(
            "No historical intelligence available."
        )

    # =====================================================
    # 5. REAL LEARNING
    # =====================================================

    print("\n[4] Real Learning & Adaptation")

    learning_result = (
        intelligence.get_adaptive_recommendation(
            defense_results
        )
    )

    if learning_result is not None:

        intelligence.show_learning(
            learning_result
        )

    # =====================================================
    # 6. ADAPTIVE DECISION
    # =====================================================

    print("\n[5] Adaptive Decision Engine")

    adaptive_engine = AdaptiveDecisionEngine(
        intelligence
    )

    # =====================================================
    # 7. AUTONOMOUS DEFENSE LOOP
    # =====================================================

    print("\n[6] Autonomous Defense Loop")

    autonomous_loop = AutonomousDefenseLoop(
        defense_engine,
        intelligence,
        adaptive_engine
    )

    autonomous_result = (
        autonomous_loop.run_cycle(
            attack_path,
            defense_results
        )
    )

    # =====================================================
    # 8. LEARNING MEMORY
    # =====================================================

    print("\n[7] Learning Memory")

    memory = LearningMemory()

    memory.record_event(
        attack_path=attack_path,

        threat_level=(
            detection_result["threat_level"]
        ),

        risk_score=(
            detection_result["risk_score"]
        ),

        defense=(
            autonomous_result.get(
                "defense",
                "Unknown"
            )
        ),

        effectiveness=(
            autonomous_result.get(
                "confidence",
                0
            )
        ),

        blocked=(
            autonomous_result.get(
                "blocked",
                False
            )
        )
    )

    print(
        "✓ Autonomous security event stored"
    )

    # =====================================================
    # SCENARIO RESULT
    # =====================================================

    print("\n")
    print("-" * 70)

    print(
        "              SCENARIO RESULT"
    )

    print("-" * 70)

    print(
        f"\n🚨 Threat: "
        f"{detection_result['threat_level']}"
    )

    print(
        f"📊 Risk: "
        f"{detection_result['risk_score']}/100"
    )

    print(
        f"🤖 Defense: "
        f"{autonomous_result.get('defense', 'Unknown')}"
    )

    print(
        f"🧠 Confidence: "
        f"{autonomous_result.get('confidence', 0)}%"
    )

    print(
        f"🔒 Blocked: "
        f"{'YES' if autonomous_result.get('blocked', False) else 'NO'}"
    )

    print(
        f"✅ Status: "
        f"{autonomous_result.get('status', 'UNKNOWN')}"
    )

    print("-" * 70)

    return {

        "scenario": scenario["name"],

        "threat_level": (
            detection_result["threat_level"]
        ),

        "risk_score": (
            detection_result["risk_score"]
        ),

        "defense": (
            autonomous_result.get(
                "defense",
                "Unknown"
            )
        ),

        "confidence": (
            autonomous_result.get(
                "confidence",
                0
            )
        ),

        "blocked": (
            autonomous_result.get(
                "blocked",
                False
            )
        ),

        "status": (
            autonomous_result.get(
                "status",
                "UNKNOWN"
            )
        )
    }


# =========================================================
# RUN ECHO-X
# =========================================================

def run_echo_x():

    print("\n")
    print("=" * 70)

    print(
        "                       ECHO-X"
    )

    print(
        "        AUTONOMOUS ADAPTIVE CYBER DEFENSE"
    )

    print(
        "                     SYSTEM"
    )

    print("=" * 70)

    print(
        "\n[+] Initializing Digital Twin..."
    )

    network = create_network()

    print(
        "✓ Virtual company network created"
    )

    scenario_engine = (
        AttackScenarioEngine(network)
    )

    scenarios = (
        scenario_engine.get_scenarios()
    )

    print(
        f"\n✓ {len(scenarios)} attack scenarios loaded"
    )

    results = []

    for scenario in scenarios:

        result = run_scenario(
            network,
            scenario
        )

        if result is not None:

            results.append(result)

    # =====================================================
    # FINAL SUMMARY
    # =====================================================

    print("\n")
    print("=" * 70)

    print(
        "              ECHO-X FINAL SUMMARY"
    )

    print("=" * 70)

    print(
        f"\nTotal Scenarios Tested: "
        f"{len(results)}"
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print("\n")

        print(
            f"Scenario {index}:"
        )

        print(
            f"  Threat: "
            f"{result['threat_level']}"
        )

        print(
            f"  Risk: "
            f"{result['risk_score']}/100"
        )

        print(
            f"  Defense: "
            f"{result['defense']}"
        )

        print(
            f"  Confidence: "
            f"{result['confidence']}%"
        )

        print(
            f"  Blocked: "
            f"{'YES' if result['blocked'] else 'NO'}"
        )

        print(
            f"  Status: "
            f"{result['status']}"
        )

    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    print("\n")
    print("=" * 70)

    print(
        "              ECHO-X SYSTEM STATUS"
    )

    print("=" * 70)

    print(
        "\n✓ Multiple attacks simulated"
    )

    print(
        "✓ Attack paths analyzed"
    )

    print(
        "✓ Threat levels calculated"
    )

    print(
        "✓ Defense strategies simulated"
    )

    print(
        "✓ Historical intelligence consulted"
    )

    print(
        "✓ Real learning applied"
    )

    print(
        "✓ Adaptive decisions generated"
    )

    print(
        "✓ Autonomous defense executed"
    )

    print(
        "✓ Attacks re-evaluated"
    )

    print(
        "✓ Security events stored"
    )

    print(
        "\n🤖 ECHO-X operated autonomously."
    )

    print(
        "🛡️ Threat response completed."
    )

    print("=" * 70)


# =========================================================
# START SYSTEM
# =========================================================

if __name__ == "__main__":

    run_echo_x()