# =========================================================
# ECHO-X
# Autonomous Adaptive Cyber Defense Dashboard
#
# Detect → Analyze → Predict → Simulate
# → Learn → Decide → Defend → Verify → Learn Again
# =========================================================
import sys
import os

# Add the project root directory to the Python path so Streamlit can locate project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your project modules below
# ... rest of your imports and code

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# =========================================================
# ECHO-X MODULES
# =========================================================

from learning.analytics import LearningAnalytics
from learning.memory import LearningMemory

from scanner.network_scanner import NetworkScanner

from detection.network_risk import NetworkRiskAnalyzer
from detection.threat_detector import ThreatDetector
from detection.attack_path_predictor import AttackPathPredictor

from network.auto_twin import AutomaticTwinBuilder

from simulator.attack_simulator import AttackSimulation

from decision.autonomous_defense import AutonomousDefense

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ECHO-X Cyber Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 17px;
        opacity: 0.75;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .status-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 10px;
    }

    .metric-label {
        font-size: 14px;
        opacity: 0.7;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def make_arrow_safe_dataframe(rows):

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    for column in df.columns:

        if df[column].dtype == "object":

            df[column] = (
                df[column]
                .fillna("")
                .astype(str)
            )

    return df

def safe_number(value, default=0):

    try:
        return float(value)

    except (TypeError, ValueError):

        return default

def format_percent(value):

    try:
        return f"{float(value):.2f}%"

    except (TypeError, ValueError):

        return "0.00%"

def get_defense_result():

    return st.session_state.get(
        "defense_result",
        {}
    )

def get_verification_result():

    return st.session_state.get(
        "verification_result",
        {}
    )

def get_feedback_result():

    return st.session_state.get(
        "feedback_result",
        {}
    )

# =========================================================
# SESSION STATE
# =========================================================

defaults = {

    "scan_completed": False,

    "devices": [],

    "analysis": {},

    "threats": [],

    "predictions": [],

    "simulation_results": [],

    "twin": None,

    "defense_result": {},

    "verification_result": {},

    "feedback_result": {},

    "updated_learning": {},

    "defense_cycle_completed": False,

    "last_scan_time": None
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🛡️ ECHO-X</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Autonomous Adaptive Cyber Defense System
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "⚙️ ECHO-X Control Center"
)

st.sidebar.markdown(
    "### Authorized Network"
)

network_input = st.sidebar.text_input(
    "Network Range",
    value="192.168.100.0/24",
    help=(
        "Enter only a network that you own "
        "or have explicit permission to test."
    )
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### Defense Pipeline"
)

st.sidebar.markdown(
    """
    1. 🔎 Detect
    2. 📊 Analyze
    3. 🎯 Predict
    4. 🧪 Simulate
    5. 🧠 Learn
    6. 🤖 Decide
    7. 🛡️ Defend
    8. ✅ Verify
    9. 🔄 Learn Again
    """
)

st.sidebar.markdown("---")

st.sidebar.warning(
    "Defense actions are applied only inside "
    "the Digital Twin."
)

# =========================================================
# SCAN BUTTON
# =========================================================

scan_button = st.sidebar.button(
    "🔍 Scan Authorized Network",
    width="stretch"
)

# =========================================================
# NETWORK SCAN
# =========================================================

if scan_button:

    if not network_input.strip():

        st.error(
            "❌ Please enter an authorized network."
        )

        st.stop()

    with st.spinner(
        "Scanning authorized network..."
    ):

        try:

            # -------------------------------------------------
            # NETWORK DISCOVERY
            # -------------------------------------------------

            scanner = NetworkScanner(
                network_input.strip()
            )

            devices = scanner.discover()

            # Prevent None from breaking the pipeline
            if devices is None:
                devices = []

            # -------------------------------------------------
            # NETWORK RISK ANALYSIS
            # -------------------------------------------------

            analyzer = NetworkRiskAnalyzer(
                devices
            )

            analysis = analyzer.analyze_network()

            # Prevent None analysis result
            if analysis is None:
                analysis = {}

            # Make sure analysis is a dictionary
            if not isinstance(analysis, dict):
                analysis = {}

            # Use discovered devices if analyzer does not
            # return its own device list
            analyzed_devices = analysis.get(
                "devices",
                devices
            )

            if analyzed_devices is None:
                analyzed_devices = devices

            analysis["devices"] = analyzed_devices

            # -------------------------------------------------
            # THREAT DETECTION
            # -------------------------------------------------

            detector = ThreatDetector(
                analyzed_devices
            )

            threats = detector.detect()

            if threats is None:
                threats = []

            # -------------------------------------------------
            # DIGITAL TWIN
            # -------------------------------------------------

            builder = AutomaticTwinBuilder(
                network_input.strip()
            )

            twin = builder.build()

            # -------------------------------------------------
            # ATTACK PATH PREDICTION
            # -------------------------------------------------

            predictions = []

            if threats and twin:

                predictor = AttackPathPredictor(
                    twin
                )

                predictions = predictor.predict(
                    threats
                )

                if predictions is None:
                    predictions = []

            # -------------------------------------------------
            # ATTACK SIMULATION
            # -------------------------------------------------

            simulation_results = []

            if predictions and twin:

                simulator = AttackSimulation(
                    twin
                )

                simulation_results = (
                    simulator.simulate_predictions(
                        predictions
                    )
                )

                if simulation_results is None:
                    simulation_results = []

            # -------------------------------------------------
            # SAVE SESSION STATE
            # -------------------------------------------------

            st.session_state.devices = devices

            st.session_state.analysis = analysis

            st.session_state.threats = threats

            st.session_state.predictions = predictions

            st.session_state.simulation_results = (
                simulation_results
            )

            st.session_state.twin = twin

            st.session_state.scan_completed = True

            st.session_state.last_scan_time = (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            # -------------------------------------------------
            # RESET DEFENSE STATE
            # -------------------------------------------------

            st.session_state.defense_result = {}

            st.session_state.verification_result = {}

            st.session_state.feedback_result = {}

            st.session_state.updated_learning = {}

            st.session_state.defense_cycle_completed = False

            st.success(
                "✅ Network scan and analysis completed."
            )

        except Exception as error:

            st.error(
                f"❌ Scan failed: {error}"
            )

# =========================================================
# EMPTY STATE
# =========================================================

if not st.session_state.scan_completed:

    st.info(
        "👈 Enter an authorized network and click "
        "**Scan Authorized Network** to start ECHO-X."
    )

    st.stop()

# =========================================================
# LOAD SESSION DATA
# =========================================================

devices = st.session_state.devices

analysis = st.session_state.analysis

threats = st.session_state.threats

predictions = st.session_state.predictions

simulation_results = (
    st.session_state.simulation_results
)

twin = st.session_state.twin

# =========================================================
# EXECUTIVE METRICS
# =========================================================

st.markdown(
    '<div class="section-title">📊 Security Posture</div>',
    unsafe_allow_html=True
)

network_risk = safe_number(
    analysis.get(
        "network_risk",
        analysis.get(
            "risk_score",
            0
        )
    )
)

security_score = max(
    0,
    min(
        100,
        100 - network_risk
    )
)

if security_score >= 80:

    posture = "SECURE"

elif security_score >= 60:

    posture = "MODERATE"

elif security_score >= 40:

    posture = "ELEVATED"

else:

    posture = "CRITICAL"

threat_count = len(threats)

path_count = len(predictions)

device_count = len(devices)

metric1, metric2, metric3, metric4 = (
    st.columns(4)
)

with metric1:

    st.metric(
        "Devices",
        device_count
    )

with metric2:

    st.metric(
        "Threats",
        threat_count
    )

with metric3:

    st.metric(
        "Predicted Paths",
        path_count
    )

with metric4:

    st.metric(
        "Network Risk",
        f"{network_risk:.1f}/100"
    )

st.markdown(
    f"""
    <div class="status-card">
    <b>Security Posture:</b> {posture}
    &nbsp;&nbsp; | &nbsp;&nbsp;
    <b>Security Score:</b> {security_score:.1f}/100
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# NETWORK SECURITY MONITORING
# =========================================================

st.markdown(
    '<div class="section-title">🌐 Network Security Monitoring</div>',
    unsafe_allow_html=True
)

device_rows = []

for device in devices:

    if isinstance(device, dict):

        device_name = device.get(
            "hostname",
            device.get(
                "name",
                "Unknown Device"
            )
        )

        ip = device.get(
            "ip",
            device.get(
                "ip_address",
                "Unknown"
            )
        )

        ports = device.get(
            "ports",
            []
        )

        risk = device.get(
            "risk_score",
            device.get(
                "risk",
                0
            )
        )

    else:

        device_name = str(device)

        ip = "Unknown"

        ports = []

        risk = 0

    if isinstance(ports, list):

        port_text = ", ".join(
            str(port)
            for port in ports
        )

    else:

        port_text = str(ports)

    device_rows.append(
        {
            "Device": device_name,
            "IP Address": ip,
            "Open Ports": port_text,
            "Risk": risk
        }
    )

device_df = make_arrow_safe_dataframe(
    device_rows
)

if not device_df.empty:

    st.dataframe(
        device_df,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No discovered devices available."
    )

# =========================================================
# SECURITY FINDINGS
# =========================================================

st.markdown(
    '<div class="section-title">🚨 Security Findings</div>',
    unsafe_allow_html=True
)

finding_rows = []

for device in devices:

    if not isinstance(device, dict):

        continue

    device_name = device.get(
        "hostname",
        device.get(
            "name",
            "Unknown"
        )
    )

    ip = device.get(
        "ip",
        device.get(
            "ip_address",
            "Unknown"
        )
    )

    ports = device.get(
        "ports",
        []
    )

    risk = safe_number(
        device.get(
            "risk_score",
            device.get(
                "risk",
                0
            )
        )
    )

    if not isinstance(ports, list):

        ports = [ports]

    for port in ports:

        if str(port) == "445":

            finding_rows.append(
                {
                    "Finding":
                        "SMB Exposure",

                    "Severity":
                        "HIGH",

                    "Risk":
                        risk if risk else 25,

                    "Device":
                        device_name,

                    "IP Address":
                        ip,

                    "Port":
                        445
                }
            )

if not finding_rows and threats:

    for threat in threats:

        finding_rows.append(
            {
                "Finding":
                    threat.get(
                        "type",
                        threat.get(
                            "name",
                            "Detected Threat"
                        )
                    ),

                "Severity":
                    threat.get(
                        "severity",
                        "UNKNOWN"
                    ),

                "Risk":
                    threat.get(
                        "risk_score",
                        0
                    ),

                "Device":
                    threat.get(
                        "source",
                        "Unknown"
                    ),

                "IP Address":
                    threat.get(
                        "ip",
                        "Unknown"
                    ),

                "Port":
                    threat.get(
                        "port",
                        "N/A"
                    )
            }
        )

finding_df = make_arrow_safe_dataframe(
    finding_rows
)

if not finding_df.empty:

    st.dataframe(
        finding_df,
        width="stretch",
        hide_index=True
    )

else:

    st.success(
        "🟢 No significant security findings detected."
    )

# =========================================================
# THREAT DETECTION
# =========================================================

st.markdown(
    '<div class="section-title">🎯 Threat Detection</div>',
    unsafe_allow_html=True
)

if threats:

    threat_rows = []

    for index, threat in enumerate(
        threats,
        start=1
    ):

        threat_rows.append(
            {
                "Threat ID":
                    f"T-{index:03d}",

                "Threat":
                    threat.get(
                        "type",
                        threat.get(
                            "name",
                            "Detected Threat"
                        )
                    ),

                "Severity":
                    threat.get(
                        "severity",
                        "UNKNOWN"
                    ),

                "Risk Score":
                    threat.get(
                        "risk_score",
                        0
                    ),

                "Source":
                    threat.get(
                        "source",
                        "Unknown"
                    ),

                "Target":
                    threat.get(
                        "target",
                        "Unknown"
                    )
            }
        )

    threat_df = make_arrow_safe_dataframe(
        threat_rows
    )

    st.dataframe(
        threat_df,
        width="stretch",
        hide_index=True
    )

else:

    st.success(
        "🟢 No threats detected."
    )

# =========================================================
# ATTACK PATH INTELLIGENCE
# =========================================================

st.markdown(
    '<div class="section-title">🧭 Attack Path Intelligence</div>',
    unsafe_allow_html=True
)

if predictions:

    path_rows = []

    for index, prediction in enumerate(
        predictions,
        start=1
    ):

        path = prediction.get(
            "path",
            []
        )

        path_rows.append(
            {
                "Path ID":
                    f"P-{index:03d}",

                "Attack Path":
                    " → ".join(
                        str(node)
                        for node in path
                    ),

                "Path Length":
                    len(path),

                "Risk":
                    prediction.get(
                        "risk_score",
                        prediction.get(
                            "risk",
                            0
                        )
                    ),

                "Threat":
                    prediction.get(
                        "threat",
                        prediction.get(
                            "severity",
                            "UNKNOWN"
                        )
                    )
            }
        )

    path_df = make_arrow_safe_dataframe(
        path_rows
    )

    st.dataframe(
        path_df,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No attack paths predicted."
    )

# =========================================================
# ATTACK SIMULATION
# =========================================================

st.markdown(
    '<div class="section-title">🧪 Attack Simulation</div>',
    unsafe_allow_html=True
)

if simulation_results:

    simulation_rows = []

    for index, result in enumerate(
        simulation_results,
        start=1
    ):

        if isinstance(result, dict):

            simulation_rows.append(
                {
                    "Simulation":
                        f"S-{index:03d}",

                    "Path":
                        " → ".join(
                            str(x)
                            for x in result.get(
                                "path",
                                []
                            )
                        ),

                    "Risk":
                        result.get(
                            "risk_score",
                            result.get(
                                "risk",
                                0
                            )
                        ),

                    "Status":
                        result.get(
                            "status",
                            "COMPLETED"
                        )
                }
            )

        else:

            simulation_rows.append(
                {
                    "Simulation":
                        f"S-{index:03d}",

                    "Path":
                        str(result),

                    "Risk":
                        0,

                    "Status":
                        "COMPLETED"
                }
            )

    simulation_df = (
        make_arrow_safe_dataframe(
            simulation_rows
        )
    )

    if not simulation_df.empty:

        st.dataframe(
            simulation_df,
            width="stretch",
            hide_index=True
        )

else:

    st.info(
        "No attack simulations completed."
    )

# =========================================================
# INTERACTIVE ATTACK PATH VISUALIZATION
# =========================================================

st.markdown(
    '<div class="section-title">📈 Interactive Attack Path Visualization</div>',
    unsafe_allow_html=True
)

if predictions:

    selected_path_index = st.selectbox(
        "Select predicted attack path",
        range(
            len(predictions)
        ),
        format_func=lambda index:
            f"Path {index + 1}"
    )

    selected_prediction = (
        predictions[
            selected_path_index
        ]
    )

    selected_path = (
        selected_prediction.get(
            "path",
            []
        )
    )

    if selected_path:

        x_values = list(
            range(
                len(selected_path)
            )
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=x_values,

                y=[
                    1
                    for _ in selected_path
                ],

                mode="lines+markers+text",

                text=[
                    str(node)
                    for node in selected_path
                ],

                textposition="top center",

                line=dict(
                    width=3
                ),

                marker=dict(
                    size=14
                )
            )
        )

        fig.update_layout(
            title="Predicted Attack Path",

            xaxis_title="Attack Sequence",

            yaxis=dict(
                visible=False,
                range=[
                    0.5,
                    1.5
                ]
            ),

            height=350,

            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

# =========================================================
# AUTONOMOUS DEFENSE
# =========================================================
# =========================================================
# SECURITY RECOMMENDATIONS & REMEDIATION
# Step 40
# =========================================================

class RemediationEngine:

    def __init__(self, threats):
        self.threats = threats
        self.recommendations = []

    def generate_recommendations(self):

        self.recommendations = []

        for threat in self.threats:

            port = threat.get("port")
            severity = threat.get("severity", "LOW")
            device = threat.get("device", "Unknown")
            ip = threat.get("ip", "Unknown")
            threat_type = threat.get(
                "threat_type",
                "Unknown Threat"
            )

            if port == 21:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "CRITICAL",
                    "action": "Disable FTP service",
                    "recommendation":
                        "Disable FTP if it is not required. "
                        "If file transfer is necessary, "
                        "use secure alternatives such as SFTP.",
                    "reason":
                        "FTP can transmit credentials and "
                        "data without adequate encryption."
                }

            elif port == 23:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "CRITICAL",
                    "action": "Disable Telnet",
                    "recommendation":
                        "Disable Telnet and replace it "
                        "with SSH for secure remote access.",
                    "reason":
                        "Telnet transmits communication "
                        "without encryption."
                }

            elif port == 445:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "HIGH",
                    "action": "Restrict SMB exposure",
                    "recommendation":
                        "Restrict SMB access using firewall "
                        "rules and allow access only from "
                        "trusted systems.",
                    "reason":
                        "Exposed SMB services can increase "
                        "the attack surface of Windows hosts."
                }

            elif port == 3389:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "HIGH",
                    "action": "Secure RDP access",
                    "recommendation":
                        "Restrict RDP access to trusted "
                        "sources and enforce strong authentication.",
                    "reason":
                        "Exposed RDP services can increase "
                        "the risk of unauthorized remote access."
                }

            elif port == 3306:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "HIGH",
                    "action": "Restrict database access",
                    "recommendation":
                        "Restrict MySQL access to trusted "
                        "hosts and avoid exposing the database "
                        "directly to untrusted networks.",
                    "reason":
                        "Exposed database services increase "
                        "the attack surface."
                }

            elif port == 5432:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "HIGH",
                    "action": "Restrict PostgreSQL access",
                    "recommendation":
                        "Restrict PostgreSQL access to "
                        "trusted systems and networks.",
                    "reason":
                        "Directly exposed database services "
                        "increase security risk."
                }

            else:

                recommendation = {
                    "device": device,
                    "ip": ip,
                    "threat": threat_type,
                    "severity": severity,
                    "priority": "MEDIUM",
                    "action": "Review exposed service",
                    "recommendation":
                        "Review the exposed service and "
                        "restrict access if it is not required.",
                    "reason":
                        "Unnecessary exposed services "
                        "increase the attack surface."
                }

            self.recommendations.append(
                recommendation
            )

        return self.recommendations


# =========================================================
# DISPLAY SECURITY RECOMMENDATIONS
# =========================================================

st.markdown(
    '<div class="section-title">🛠️ Security Recommendations & Remediation</div>',
    unsafe_allow_html=True
)

if threats:

    remediation_engine = RemediationEngine(threats)

    recommendations = (
        remediation_engine.generate_recommendations()
    )

    if recommendations:

        for recommendation in recommendations:

            priority = recommendation.get(
                "priority",
                "MEDIUM"
            )

            if priority == "CRITICAL":
                st.error(
                    f"🔴 CRITICAL — "
                    f"{recommendation.get('action', 'Security Action')}"
                )

            elif priority == "HIGH":
                st.warning(
                    f"🟠 HIGH — "
                    f"{recommendation.get('action', 'Security Action')}"
                )

            else:
                st.info(
                    f"🔵 MEDIUM — "
                    f"{recommendation.get('action', 'Security Action')}"
                )

            st.markdown(
                f"""
                **Device:** `{recommendation.get('device', 'Unknown')}`

                **IP Address:** `{recommendation.get('ip', 'Unknown')}`

                **Threat:** `{recommendation.get('threat', 'Unknown Threat')}`

                **Severity:** `{recommendation.get('severity', 'UNKNOWN')}`

                **Recommended Action:**  
                {recommendation.get('recommendation', 'Review security configuration.')}

                **Reason:**  
                {recommendation.get('reason', 'Security hardening is recommended.')}

                ---
                """
            )

    else:

        st.success(
            "✅ No remediation recommendations are required."
        )

else:

    st.success(
        "🟢 No active threats detected. "
        "No remediation actions are required."
    )

st.markdown(
    '<div class="section-title">🤖 Autonomous Defense</div>',
    unsafe_allow_html=True
)

if not threats:

    st.success(
        "🟢 No active threat requires autonomous defense."
    )

elif not predictions:

    st.warning(
        "⚠️ Threat detected, but no attack path is available."
    )

elif not twin:

    st.error(
        "❌ Digital Twin is not available."
    )

else:

    attack_path = predictions[0].get(
        "path",
        []
    )

    threat = threats[0]

    if attack_path:

        st.markdown(
            f"**Predicted Attack Path:** "
            f"`{' → '.join(str(x) for x in attack_path)}`"
        )

        st.markdown(
            f"**Threat Level:** "
            f"`{threat.get('severity', 'UNKNOWN')}`"
        )

        st.markdown(
            f"**Risk Score:** "
            f"`{threat.get('risk_score', 0)}/100`"
        )

        st.markdown("---")

        if st.button(
            "🛡️ Run Autonomous Defense",
            width="stretch"
        ):

            with st.spinner(
                "ECHO-X is executing autonomous defense..."
            ):

                try:

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

                    if not cyce_result:

                        st.error(
                            " Autonomous defense cycle failed."
                        )

                    else:

                        selected_defense = (
                            cycle_result[
                                "selected_defense"
                            ]
                        )

                        execution_result = (
                            cycle_result[
                                "execution"
                            ]
                        )

                        verification = (
                            cycle_result[
                                "verification"
                            ]
                        )

                        feedback = (
                            cycle_result[
                                "feedback"
                            ]
                        )

                        updated_learning = (
                            cycle_result[
                                "updated_learning"
                            ]
                        )

                        # -----------------------------------------
                        # SAVE RESULTS
                        # -----------------------------------------

                        st.session_state.defense_result = {

                            "selected":
                                selected_defense,

                            "execution":
                                execution_result,

                            "cycle":
                                cycle_result
                        }

                        st.session_state.verification_result = (
                            verification or {}
                        )

                        st.session_state.feedback_result = (
                            feedback or {}
                        )

                        st.session_state.updated_learning = (
                            updated_learning or {}
                        )

                        st.session_state.defense_cycle_completed = (
                            True
                        )

                        # -----------------------------------------
                        # SUCCESS MESSAGE
                        # -----------------------------------------

                        if verification and verification.get(
                            "neutralized",
                            verification.get(
                                "verified",
                                False
                            )
                        ):

                            st.success(
                                "🛡️ ECHO-X successfully neutralized "
                                "the predicted attack path inside "
                                "the Digital Twin."
                            )

                        else:

                            st.warning(
                                "⚠️ Defense executed, but the "
                                "attack path remains active."
                            )

                        # -----------------------------------------
                        # DEFENSE METRICS
                        # -----------------------------------------

                        d1, d2, d3, d4 = (
                            st.columns(4)
                        )

                        with d1:

                            st.metric(
                                "Selected Defense",
                                selected_defense.get(
                                    "display_name",
                                    "Unknown"
                                )
                            )

                        with d2:

                            st.metric(
                                "Fusion Score",
                                f"{selected_defense.get('fusion_score', 0):.2f}"
                            )

                        with d3:

                            st.metric(
                                "Confidence",
                                f"{selected_defense.get('confidence', 0):.2f}%"
                            )

                        with d4:

                            st.metric(
                                "Effectiveness",
                                f"{selected_defense.get('effectiveness', 0):.2f}%"
                            )

                        # -----------------------------------------
                        # EXECUTION DETAILS
                        # -----------------------------------------

                        st.markdown(
                            "### 🛡️ Defense Execution"
                        )

                        execution_rows = [

                            {
                                "Metric":
                                    "Defense",

                                "Value":
                                    execution_result.get(
                                        "display_name",
                                        "Unknown"
                                    )
                            },

                            {
                                "Metric":
                                    "Source",

                                "Value":
                                    execution_result.get(
                                        "source",
                                        "Unknown"
                                    )
                            },

                            {
                                "Metric":
                                    "Target",

                                "Value":
                                    execution_result.get(
                                        "target",
                                        "Unknown"
                                    )
                            },

                            {
                                "Metric":
                                    "Status",

                                "Value":
                                    execution_result.get(
                                        "status",
                                        "UNKNOWN"
                                    )
                            },

                            {
                                "Metric":
                                    "Attack Blocked",

                                "Value":
                                    (
                                        "YES"
                                        if execution_result.get(
                                            "blocked",
                                            False
                                        )
                                        else "NO"
                                    )
                            }
                        ]

                        execution_df = (
                            make_arrow_safe_dataframe(
                                execution_rows
                            )
                        )

                        st.dataframe(
                            execution_df,
                            width="stretch",
                            hide_index=True
                        )

                        # -----------------------------------------
                        # VERIFICATION
                        # -----------------------------------------

                        st.markdown(
                            "### ✅ Defense Verification"
                        )

                        before_path = (
                            verification.get(
                                "before",
                                attack_path
                            )
                            if verification
                            else attack_path
                        )

                        after_path = (
                            verification.get(
                                "after"
                            )
                            if verification
                            else None
                        )

                        neutralized = (
                            verification.get(
                                "neutralized",
                                verification.get(
                                    "verified",
                                    False
                                )
                            )
                            if verification
                            else False
                        )

                        verification_rows = [

                            {
                                "Metric":
                                    "Before",

                                "Value":
                                    " → ".join(
                                        str(x)
                                        for x in before_path
                                    )
                            },

                            {
                                "Metric":
                                    "After",

                                "Value":
                                    (
                                        "No Attack Path"
                                        if not after_path
                                        else
                                        " → ".join(
                                            str(x)
                                            for x in after_path
                                        )
                                    )
                            },

                            {
                                "Metric":
                                    "Status",

                                "Value":
                                    (
                                        verification.get(
                                            "status",
                                            "UNKNOWN"
                                        )
                                        if verification
                                        else "UNKNOWN"
                                    )
                            },

                            {
                                "Metric":
                                    "Neutralized",

                                "Value":
                                    (
                                        "YES"
                                        if neutralized
                                        else "NO"
                                    )
                            }
                        ]

                        verification_df = (
                            make_arrow_safe_dataframe(
                                verification_rows
                            )
                        )

                        st.dataframe(
                            verification_df,
                            width="stretch",
                            hide_index=True
                        )

                        # -----------------------------------------
                        # FEEDBACK LEARNING
                        # -----------------------------------------

                        st.markdown(
                            "### 🧠 Feedback Learning"
                        )

                        feedback_rows = [

                            {
                                "Metric":
                                    "Simulated Effectiveness",

                                "Value":
                                    (
                                        feedback.get(
                                            "simulated_effectiveness",
                                            selected_defense.get(
                                                "effectiveness",
                                                0
                                            )
                                        )
                                        if feedback
                                        else
                                        selected_defense.get(
                                            "effectiveness",
                                            0
                                        )
                                    )
                            },

                            {
                                "Metric":
                                    "Actual Effectiveness",

                                "Value":
                                    (
                                        feedback.get(
                                            "effectiveness",
                                            0
                                        )
                                        if feedback
                                        else 0
                                    )
                            },

                            {
                                "Metric":
                                    "Attack Blocked",

                                "Value":
                                    (
                                        "YES"
                                        if feedback
                                        and feedback.get(
                                            "blocked",
                                            False
                                        )
                                        else "NO"
                                    )
                            },

                            {
                                "Metric":
                                    "Verification",

                                "Value":
                                    (
                                        "VERIFIED"
                                        if feedback
                                        and feedback.get(
                                            "verified",
                                            False
                                        )
                                        else "NOT VERIFIED"
                                    )
                            },

                            {
                                "Metric":
                                    "Learning Status",

                                "Value":
                                    "UPDATED"
                            }
                        ]

                        feedback_df = (
                            make_arrow_safe_dataframe(
                                feedback_rows
                            )
                        )

                        st.dataframe(
                            feedback_df,
                            width="stretch",
                            hide_index=True
                        )

                        # -----------------------------------------
                        # UPDATED LEARNING
                        # -----------------------------------------

                        st.markdown(
                            "### 🔄 Updated Learning Model"
                        )

                        updated_learning_rows = [

                            {
                                "Metric":
                                    "Defense",

                                "Value":
                                    selected_defense.get(
                                        "display_name",
                                        "Unknown"
                                    )
                            },

                            {
                                "Metric":
                                    "Historical Uses",

                                "Value":
                                    updated_learning.get(
                                        "uses",
                                        0
                                    )
                            },

                            {
                                "Metric":
                                    "Historical Effectiveness",

                                "Value":
                                    updated_learning.get(
                                        "historical_effectiveness",
                                        updated_learning.get(
                                            "average_effectiveness",
                                            0
                                        )
                                    )
                            },

                            {
                                "Metric":
                                    "Historical Block Rate",

                                "Value":
                                    updated_learning.get(
                                        "historical_block_rate",
                                        updated_learning.get(
                                            "block_rate",
                                            0
                                        )
                                    )
                            }
                        ]

                        updated_learning_df = (
                            make_arrow_safe_dataframe(
                                updated_learning_rows
                            )
                        )

                        st.dataframe(
                            updated_learning_df,
                            width="stretch",
                            hide_index=True
                        )

                        st.success(
                            "🧠 ECHO-X learning memory has been updated."
                        )

                except Exception as error:

                    st.error(
                        f"❌ Autonomous defense error: {error}"
                    )

# =========================================================
# LOAD CURRENT DEFENSE RESULTS
# =========================================================

defense_result = get_defense_result()

verification_result = get_verification_result()

feedback_result = get_feedback_result()

selected = defense_result.get(
    "selected",
    {}
)

execution = defense_result.get(
    "execution",
    {}
)

verification = verification_result

defense_available = bool(
    defense_result
)

neutralized = bool(
    verification.get(
        "neutralized",
        verification.get(
            "verified",
            False
        )
    )
)

# =========================================================
# CURRENT DEFENSE SUMMARY
# =========================================================

if defense_result:

    st.markdown(
        '<div class="section-title">🛡️ Current Defense Status</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Defense",
            selected.get(
                "display_name",
                "Unknown"
            )
        )

    with c2:

        st.metric(
            "Fusion Score",
            f"{selected.get('fusion_score', 0):.2f}"
        )

    with c3:

        st.metric(
            "Execution",
            execution.get(
                "status",
                "UNKNOWN"
            )
        )

    with c4:

        st.metric(
            "Verification",
            (
                "VERIFIED"
                if neutralized
                else "NOT VERIFIED"
            )
        )

# =========================================================
# SECURITY INCIDENT TIMELINE
# =========================================================

st.markdown(
    '<div class="section-title">🕒 Security Incident Timeline</div>',
    unsafe_allow_html=True
)

timeline_rows = []

if threats:

    timeline_rows.append(
        {
            "Stage":
                "Threat Detection",

            "Status":
                "COMPLETED",

            "Details":
                f"{len(threats)} threat(s) detected"
        }
    )

if predictions:

    timeline_rows.append(
        {
            "Stage":
                "Attack Path Prediction",

            "Status":
                "COMPLETED",

            "Details":
                f"{len(predictions)} path(s) predicted"
        }
    )

if simulation_results:

    timeline_rows.append(
        {
            "Stage":
                "Attack Simulation",

            "Status":
                "COMPLETED",

            "Details":
                f"{len(simulation_results)} simulation(s) completed"
        }
    )

if defense_result:

    timeline_rows.append(
        {
            "Stage":
                "Autonomous Defense",

            "Status":
                execution.get(
                    "status",
                    "COMPLETED"
                ),

            "Details":
                selected.get(
                    "display_name",
                    "Defense executed"
                )
        }
    )

if verification_result:

    timeline_rows.append(
        {
            "Stage":
                "Defense Verification",

            "Status":
                verification_result.get(
                    "status",
                    "UNKNOWN"
                ),

            "Details":
                (
                    "Attack path neutralized"
                    if verification_result.get(
                        "neutralized",
                        verification_result.get(
                            "verified",
                            False
                        )
                    )
                    else
                    "Attack path still active"
                )
        }
    )

if feedback_result:

    timeline_rows.append(
        {
            "Stage":
                "Feedback Learning",

            "Status":
                "COMPLETED",

            "Details":
                "Learning memory updated"
        }
    )

timeline_df = make_arrow_safe_dataframe(
    timeline_rows
)

if not timeline_df.empty:

    st.dataframe(
        timeline_df,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "Timeline will appear after the security pipeline runs."
    )

# =========================================================
# STEP 39 — EXECUTIVE SECURITY REPORT
# =========================================================

st.markdown(
    '<div class="section-title">📋 Step 39 — Executive Security Report</div>',
    unsafe_allow_html=True
)

st.caption(
    "Executive-level summary of the current ECHO-X security assessment."
)

# ---------------------------------------------------------
# THREAT COUNTS
# ---------------------------------------------------------

critical_count = 0

high_count = 0

medium_count = 0

low_count = 0

for threat in threats:

    severity = str(
        threat.get(
            "severity",
            ""
        )
    ).upper()

    if severity == "CRITICAL":

        critical_count += 1

    elif severity == "HIGH":

        high_count += 1

    elif severity == "MEDIUM":

        medium_count += 1

    elif severity == "LOW":

        low_count += 1

# ---------------------------------------------------------
# EXECUTIVE METRICS
# ---------------------------------------------------------

report_col1, report_col2, report_col3, report_col4 = (
    st.columns(4)
)

with report_col1:

    st.metric(
        "Security Score",
        f"{security_score:.1f}/100"
    )

with report_col2:

    st.metric(
        "Threats Detected",
        threat_count
    )

with report_col3:

    st.metric(
        "Attack Paths",
        path_count
    )

with report_col4:

    if defense_available:

        report_status = (
            "NEUTRALIZED"
            if neutralized
            else "ACTIVE"
        )

    else:

        report_status = "PENDING"

    st.metric(
        "Response Status",
        report_status
    )

# ---------------------------------------------------------
# EXECUTIVE ASSESSMENT
# ---------------------------------------------------------

if neutralized:

    assessment = (
        "ECHO-X detected a security threat, "
        "predicted an attack path, simulated defensive "
        "responses, selected an adaptive defense strategy, "
        "executed the defense inside the Digital Twin, "
        "verified that the predicted attack path was "
        "neutralized, and updated its learning memory."
    )

elif defense_available:

    assessment = (
        "ECHO-X detected a security threat and executed "
        "an autonomous defense strategy. Verification "
        "indicates that the predicted attack path remains "
        "active and requires further defensive adaptation."
    )

elif threats:

    assessment = (
        "ECHO-X detected one or more security threats. "
        "Autonomous defense has not yet been executed."
    )

else:

    assessment = (
        "ECHO-X completed the security assessment with "
        "no active threats requiring autonomous defense."
    )

st.info(
    assessment
)

# ---------------------------------------------------------
# SECURITY ASSESSMENT TABLE
# ---------------------------------------------------------

security_assessment_rows = [

    {
        "Assessment":
            "Network Risk",

        "Value":
            f"{network_risk:.1f}/100",

        "Status":
            posture
    },

    {
        "Assessment":
            "Security Score",

        "Value":
            f"{security_score:.1f}/100",

        "Status":
            posture
    },

    {
        "Assessment":
            "Threats Detected",

        "Value":
            threat_count,

        "Status":
            (
                "ATTENTION REQUIRED"
                if threat_count > 0
                else "CLEAR"
            )
    },

    {
        "Assessment":
            "Predicted Attack Paths",

        "Value":
            path_count,

        "Status":
            (
                "ATTENTION REQUIRED"
                if path_count > 0
                else "CLEAR"
            )
    },

    {
        "Assessment":
            "Autonomous Defense",

        "Value":
            selected.get(
                "display_name",
                "Not Executed"
            ),

        "Status":
            (
                "EXECUTED"
                if defense_available
                else "PENDING"
            )
    },

    {
        "Assessment":
            "Defense Verification",

        "Value":
            verification.get(
                "status",
                "PENDING"
            ),

        "Status":
            (
                "VERIFIED"
                if neutralized
                else
                (
                    "PENDING"
                    if not defense_available
                    else "ATTENTION"
                )
            )
    }
]

security_assessment_df = (
    make_arrow_safe_dataframe(
        security_assessment_rows
    )
)

st.dataframe(
    security_assessment_df,
    width="stretch",
    hide_index=True
)

# ---------------------------------------------------------
# THREAT SUMMARY
# ---------------------------------------------------------

st.markdown(
    "### 🚨 Threat Summary"
)

threat_summary_rows = [

    {
        "Severity":
            "CRITICAL",

        "Count":
            critical_count
    },

    {
        "Severity":
            "HIGH",

        "Count":
            high_count
    },

    {
        "Severity":
            "MEDIUM",

        "Count":
            medium_count
    },

    {
        "Severity":
            "LOW",

        "Count":
            low_count
    }
]

threat_summary_df = (
    make_arrow_safe_dataframe(
        threat_summary_rows
    )
)

st.dataframe(
    threat_summary_df,
    width="stretch",
    hide_index=True
)

# ---------------------------------------------------------
# AUTONOMOUS RESPONSE SUMMARY
# ---------------------------------------------------------

st.markdown(
    "### 🛡️ Autonomous Response Summary"
)

response_rows = [

    {
        "Metric":
            "Selected Defense",

        "Value":
            selected.get(
                "display_name",
                "Not Executed"
            )
    },

    {
        "Metric":
            "Fusion Score",

        "Value":
            selected.get(
                "fusion_score",
                0
            )
    },

    {
        "Metric":
            "Confidence",

        "Value":
            selected.get(
                "confidence",
                0
            )
    },

    {
        "Metric":
            "Simulated Effectiveness",

        "Value":
            selected.get(
                "effectiveness",
                0
            )
    },

    {
        "Metric":
            "Attack Blocked",

        "Value":
            (
                "YES"
                if execution.get(
                    "blocked",
                    False
                )
                else
                "NO"
                if execution
                else
                "NOT EXECUTED"
            )
    },

    {
        "Metric":
            "Verification",

        "Value":
            (
                verification.get(
                    "status",
                    "UNKNOWN"
                )
                if verification
                else
                "PENDING"
            )
    }
]

response_df = (
    make_arrow_safe_dataframe(
        response_rows
    )
)

st.dataframe(
    response_df,
    width="stretch",
    hide_index=True
)

# ---------------------------------------------------------
# EXECUTIVE RECOMMENDATION
# ---------------------------------------------------------

st.markdown(
    "### 💡 Executive Recommendation"
)

if neutralized:

    recommendation = (
        "The detected attack path was successfully "
        "neutralized inside the Digital Twin. "
        "ECHO-X should retain the selected defense "
        "experience in its learning memory and continue "
        "monitoring for recurrence."
    )

elif defense_available:

    recommendation = (
        "The autonomous response was executed, but "
        "verification indicates that the attack path "
        "remains active. ECHO-X should continue the "
        "adaptive defense cycle and evaluate alternative "
        "defensive strategies."
    )

elif threats:

    recommendation = (
        "Security threats were identified and attack "
        "paths were predicted. Execute the autonomous "
        "defense cycle to evaluate and apply the most "
        "appropriate defensive strategy inside the "
        "Digital Twin."
    )

else:

    recommendation = (
        "No active threat requires autonomous defense. "
        "Continue monitoring the network and maintain "
        "current security controls."
    )

st.warning(
    recommendation
)

# =========================================================
# LEARNING INTELLIGENCE
# =========================================================

st.markdown(
    '<div class="section-title">🧠 Learning Intelligence</div>',
    unsafe_allow_html=True
)

memory = LearningMemory()

records = memory.records

# =========================================================
# LEARNING ANALYTICS
# =========================================================

analytics = LearningAnalytics()

analytics_result = None

try:

    analytics_result = (
        analytics.generate_report()
    )

except Exception:

    analytics_result = None

# =========================================================
# LEARNING METRICS
# =========================================================

if records:

    total_events = len(records)

    total_blocked = sum(
        1
        for record in records
        if record.get(
            "blocked",
            False
        )
    )

    average_effectiveness = (

        sum(
            safe_number(
                record.get(
                    "effectiveness",
                    0
                )
            )

            for record in records
        )

        / total_events
    )

    overall_block_rate = (

        total_blocked
        / total_events
        * 100
    )

else:

    total_events = 0

    total_blocked = 0

    average_effectiveness = 0

    overall_block_rate = 0

l1, l2, l3, l4 = (
    st.columns(4)
)

with l1:

    st.metric(
        "Learning Events",
        total_events
    )

with l2:

    st.metric(
        "Blocked",
        total_blocked
    )

with l3:

    st.metric(
        "Avg Effectiveness",
        f"{average_effectiveness:.2f}%"
    )

with l4:

    st.metric(
        "Block Rate",
        f"{overall_block_rate:.2f}%"
    )

# =========================================================
# HISTORICAL DEFENSE PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">📚 Historical Defense Performance</div>',
    unsafe_allow_html=True
)

defense_history = {}

for record in records:

    defense_name = record.get(
        "defense",
        "Unknown"
    )

    if defense_name not in defense_history:

        defense_history[
            defense_name
        ] = {

            "uses":
                0,

            "blocked":
                0,

            "effectiveness_total":
                0
        }

    defense_history[
        defense_name
    ]["uses"] += 1

    defense_history[
        defense_name
    ]["effectiveness_total"] += (

        safe_number(
            record.get(
                "effectiveness",
                0
            )
        )
    )

    if record.get(
        "blocked",
        False
    ):

        defense_history[
            defense_name
        ]["blocked"] += 1

history_rows = []

for defense_name, values in (
    defense_history.items()
):

    uses = values["uses"]

    effectiveness = (

        values["effectiveness_total"]
        / uses
        if uses
        else 0
    )

    block_rate = (

        values["blocked"]
        / uses
        * 100
        if uses
        else 0
    )

    history_rows.append(
        {
            "Defense":
                defense_name,

            "Uses":
                uses,

            "Avg Effectiveness":
                round(
                    effectiveness,
                    2
                ),

            "Blocked":
                values["blocked"],

            "Block Rate":
                round(
                    block_rate,
                    2
                )
        }
    )

history_df = make_arrow_safe_dataframe(
    history_rows
)

if not history_df.empty:

    st.dataframe(
        history_df,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No historical defense data available yet."
    )

# =========================================================
# SECURITY ANALYTICS
# =========================================================

st.markdown(
    '<div class="section-title">📈 Security Analytics</div>',
    unsafe_allow_html=True
)

if records:

    event_numbers = list(
        range(
            1,
            len(records) + 1
        )
    )

    effectiveness_values = [

        safe_number(
            record.get(
                "effectiveness",
                0
            )
        )

        for record in records
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(

            x=event_numbers,

            y=effectiveness_values,

            mode="lines+markers",

            name="Defense Effectiveness"
        )
    )

    fig.update_layout(

        title="Defense Effectiveness Over Time",

        xaxis_title="Learning Event",

        yaxis_title="Effectiveness (%)",

        yaxis=dict(
            range=[
                0,
                100
            ]
        ),

        height=400
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

else:

    st.info(
        "Security analytics will appear after "
        "defense learning events are recorded."
    )

# =========================================================
# LEARNING TREND
# =========================================================

st.markdown(
    '<div class="section-title">📉 Learning Trend</div>',
    unsafe_allow_html=True
)

if len(records) >= 4:

    effectiveness_values = [

        safe_number(
            record.get(
                "effectiveness",
                0
            )
        )

        for record in records
    ]

    midpoint = (
        len(effectiveness_values)
        // 2
    )

    earlier = (
        effectiveness_values[
            :midpoint
        ]
    )

    recent = (
        effectiveness_values[
            midpoint:
        ]
    )

    earlier_avg = (
        sum(earlier)
        / len(earlier)
    )

    recent_avg = (
        sum(recent)
        / len(recent)
    )

    change = (
        recent_avg
        - earlier_avg
    )

    if change > 2:

        trend = "IMPROVING"

    elif change < -2:

        trend = "DECLINING"

    else:

        trend = "STABLE"

    trend_col1, trend_col2, trend_col3 = (
        st.columns(3)
    )

    with trend_col1:

        st.metric(
            "Trend",
            trend
        )

    with trend_col2:

        st.metric(
            "Recent Average",
            f"{recent_avg:.2f}%"
        )

    with trend_col3:

        st.metric(
            "Effectiveness Change",
            f"{change:+.2f}%"
        )

else:

    st.info(
        "More learning events are required to calculate "
        "a reliable learning trend."
    )

# =========================================================
# SECURITY EVENT HISTORY
# =========================================================

st.markdown(
    '<div class="section-title">🗂️ Security Event History</div>',
    unsafe_allow_html=True
)

if records:

    event_rows = []

    for index, record in enumerate(
        reversed(records),
        start=1
    ):

        event_rows.append(
            {
                "Event":
                    index,

                "Timestamp":
                    record.get(
                        "timestamp",
                        "Unknown"
                    ),

                "Threat":
                    record.get(
                        "threat_level",
                        "UNKNOWN"
                    ),

                "Risk":
                    record.get(
                        "risk_score",
                        0
                    ),

                "Defense":
                    record.get(
                        "display_name",
                        record.get(
                            "defense",
                            "Unknown"
                        )
                    ),

                "Effectiveness":
                    record.get(
                        "effectiveness",
                        0
                    ),

                "Blocked":
                    (
                        "YES"
                        if record.get(
                            "blocked",
                            False
                        )
                        else "NO"
                    ),

                "Verified":
                    (
                        "YES"
                        if record.get(
                            "verified",
                            record.get(
                                "neutralized",
                                False
                            )
                        )
                        else "NO"
                    )
            }
        )

    event_df = make_arrow_safe_dataframe(
        event_rows
    )

    st.dataframe(
        event_df,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No security events recorded yet."
    )

# =========================================================
# SYSTEM STATUS
# =========================================================

st.markdown(
    '<div class="section-title">🟢 System Status</div>',
    unsafe_allow_html=True
)

status_rows = [

    {
        "Component":
            "Network Scanner",

        "Status":
            "ONLINE"
    },

    {
        "Component":
            "Risk Analyzer",

        "Status":
            "ONLINE"
    },

    {
        "Component":
            "Threat Detector",

        "Status":
            "ONLINE"
    },

    {
        "Component":
            "Attack Path Predictor",

        "Status":
            "ONLINE"
    },

    {
        "Component":
            "Attack Simulator",

        "Status":
            "ONLINE"
    },

    {
        "Component":
            "Digital Twin",

        "Status":
            (
                "ONLINE"
                if twin
                else "OFFLINE"
            )
    },

    {
        "Component":
            "Autonomous Defense",

        "Status":
            (
                "ACTIVE"
                if defense_result
                else "READY"
            )
    },

    {
        "Component":
            "Learning Memory",

        "Status":
            "ONLINE"
    }
]

status_df = make_arrow_safe_dataframe(
    status_rows
)

st.dataframe(
    status_df,
    width="stretch",
    hide_index=True
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "ECHO-X — Autonomous Adaptive Cyber Defense System | "
    "Defense actions are simulated inside the Digital Twin."
)

if st.session_state.last_scan_time:

    st.caption(
        f"Last scan: "
        f"{st.session_state.last_scan_time}"
    )
