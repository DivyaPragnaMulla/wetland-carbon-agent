
import os
import streamlit as st
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import OrchestratorAgent

# ── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Wetland Carbon Monitoring Agent",
    page_icon="🌿",
    layout="wide"
)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.title("🌿 Wetland Carbon Monitoring Agent")
st.caption("Multi-agent AI system | EU LifeWatch Italy Research | Built by Divya Pragna Mulla PhD")

# ── API KEY INPUT ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("**Get your free API key at [console.groq.com](https://console.groq.com)**")

    api_key = st.text_input(
        "Enter your Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Your key is never stored or shared"
    )

    st.markdown("---")
    st.markdown("**About this agent:**")
    st.markdown("Built on PhD research in wetland ecosystem monitoring at University of Salento, Italy")
    st.markdown("**Subagents:**")
    st.markdown("🔬 Risk Assessment Agent")
    st.markdown("📊 Data Fetching Agent")
    st.markdown("📄 Report Generation Agent")
    st.markdown("🚨 Alert & Intervention Agent")
    st.markdown("---")
    st.markdown("**Built by:** [Divya Pragna Mulla](https://divyapragnamulla.github.io)")
    st.markdown("**Certifications:** Anthropic Agent Skills | Anthropic Subagents | Microsoft AI")

if not api_key:
    st.info("👈 Please enter your Groq API key in the sidebar to get started. Get a free key at console.groq.com")
    st.stop()

# Initialise orchestrator with user API key
try:
    orchestrator = OrchestratorAgent(api_key)
except Exception as e:
    st.error(f"Invalid API key. Please check and try again.")
    st.stop()

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["💬 Ask the Agent", "📊 Site Risk Assessment", "🌍 Live Air Quality"])

# TAB 1 — Chat
with tab1:
    st.subheader("Ask about wetland ecosystem health")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔴 Carbon sink risk"):
            st.session_state.q = "What conditions indicate a wetland is shifting from carbon sink to source?"
    with col2:
        if st.button("📋 Monitoring report"):
            st.session_state.q = "Generate a monitoring summary for a temperate wetland under hydrological stress"
    with col3:
        if st.button("🌡️ Climate stress"):
            st.session_state.q = "How does drought affect CO₂ flux in Mediterranean wetlands?"

    question = st.text_input("Your question:", value=st.session_state.get("q", ""))
    if "q" in st.session_state:
        del st.session_state.q

    if st.button("Ask Agent", type="primary") and question:
        with st.spinner("Agent analysing..."):
            answer = orchestrator.run(question, mode="chat")
            st.markdown(answer)

# TAB 2 — Risk Assessment
with tab2:
    st.subheader("Full Multi-Agent Site Assessment")
    st.markdown("All 4 subagents run in sequence — risk → data → report → alerts")

    col1, col2 = st.columns(2)
    with col1:
        site_name = st.text_input("Site name", placeholder="e.g. Castelporziano Site 1")
        water_table = st.slider("Water Table Depth (cm)", -50, 10, -5)
        temp_anomaly = st.slider("Temperature Anomaly (°C)", 0.0, 4.0, 0.5, 0.1)
        co2_flux = st.slider("CO₂ Flux (μmol/m²/s)", -5.0, 10.0, -1.0, 0.1)
        city = st.text_input("Nearest city for air quality (optional)", placeholder="e.g. Rome")

    with col2:
        icons = {"LOW": "🟢", "MODERATE": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}
        st.metric("Water Table", f"{water_table}cm",
                  delta="⚠️ Critical" if water_table < -20 else "✅ OK")
        st.metric("Temp Anomaly", f"+{temp_anomaly}°C",
                  delta="⚠️ Critical" if temp_anomaly > 2 else "✅ OK")
        st.metric("CO₂ Flux", f"{co2_flux} μmol/m²/s",
                  delta="📈 Source" if co2_flux > 0 else "📉 Sink")

    if st.button("🚀 Run Full Assessment", type="primary"):
        params = {
            "water_table": water_table,
            "temp_anomaly": temp_anomaly,
            "co2_flux": co2_flux,
            "site_name": site_name,
            "city": city
        }

        with st.spinner("Running all subagents..."):
            results = orchestrator.run(params, mode="assess")

        # Risk results
        risk = results["risk"]
        st.markdown(f"## {icons.get(risk['level'], '⚪')} Risk Level: {risk['level']}")
        st.info(f"**Action:** {risk['action']}")
        st.info(f"**Monitoring:** {risk['frequency']}")
        st.markdown("**Scientific interpretation:**")
        st.markdown(risk["interpretation"])

        # Alerts
        st.markdown("### 🚨 Alerts & Recommendations")
        alerts = results["alerts"]
        for alert in alerts["alerts"]:
            st.markdown(alert)
        st.markdown(alerts["recommendations"])

        # Air quality
        if results.get("air_quality") and not results["air_quality"].get("error"):
            aq = results["air_quality"]
            st.markdown("### 🌍 Air Quality")
            st.metric(f"PM2.5 in {aq['city']}",
                     f"{aq['average_pm25']} μg/m³",
                     delta=aq["status"])

        # Full report
        report = results["report"]
        st.markdown("### 📄 Full Monitoring Report")
        st.markdown(report["content"])

        # Download
        st.download_button(
            "📥 Download Full Report",
            data=f"WETLAND MONITORING REPORT\n{'='*50}\nGenerated: {report['generated_at']}\nSite: {report['site']}\n\n{report['content']}",

Generated: {report['generated_at']}
Site: {report['site']}

{report['content']}",
            file_name=f"wetland_report_{site_name.replace(' ','_')}.txt",
            mime="text/plain"
        )

# TAB 3 — Live Air Quality
with tab3:
    st.subheader("Live Air Quality Data")
    city_input = st.text_input("City name", placeholder="e.g. London, Rome, Edinburgh")

    if st.button("🌍 Fetch Live Data") and city_input:
        with st.spinner("Data agent fetching..."):
            data_agent = orchestrator.data_agent
            data = data_agent.fetch_air_quality(city_input)

            if data and not data.get("error"):
                import pandas as pd
                df = pd.DataFrame(data["readings"])
                st.success(f"Found {len(df)} monitoring stations")
                st.dataframe(df, use_container_width=True)
                st.metric("Average PM2.5",
                         f"{data['average_pm25']} μg/m³",
                         delta=data["status"])

                with st.spinner("Report agent interpreting..."):
                    interp = orchestrator.run(
                        f"Interpret PM2.5 of {data['average_pm25']} μg/m³ in {city_input}. WHO limit is 15 μg/m³. Brief health risk in 3 sentences.",
                        mode="chat"
                    )
                    st.markdown("**AI Health Risk:**")
                    st.markdown(interp)
            else:
                st.warning("No data found. Try: London, Rome, Paris, Berlin")

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:grey; font-size:12px;'>
Built by <strong>Divya Pragna Mulla</strong> | PhD Environmental Data Science |
EU LifeWatch Italy Research | 5 peer-reviewed publications<br>
<a href='https://divyapragnamulla.github.io'>Portfolio</a> |
<a href='https://github.com/DivyaPragnaMulla'>GitHub</a> |
<a href='https://www.linkedin.com/in/divya-pragna-mulla-b69879219/'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)
