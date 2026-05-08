import os
import requests
import streamlit as st
from datetime import datetime

# ── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Wetland Carbon Monitoring Agent",
    page_icon="🌿",
    layout="wide"
)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.title("🌿 Wetland Carbon Monitoring Agent")
st.caption("Multi-agent AI system | EU LifeWatch Italy Research | Built by Divya Pragna Mulla PhD")

# ── SIDEBAR — API KEY INPUT ──────────────────────────────────────────────────
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

# ── GROQ CLIENT ──────────────────────────────────────────────────────────────
try:
    from groq import Groq
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("Invalid API key. Please check and try again.")
    st.stop()

# ── SYSTEM PROMPT ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert environmental data analyst specialising in 
wetland ecosystem monitoring, carbon flux analysis, and climate-driven ecological 
transitions.

Your knowledge is grounded in:
- EU-funded LifeWatch Italy wetland monitoring research
- FluxNet global carbon flux datasets
- WHO AirQ+ environmental health frameworks
- IPCC climate thresholds: critical threshold greater than 2 degrees above baseline
- EU Water Framework Directive standards

Risk classification rules:
- CRITICAL: water table below -20cm AND temp anomaly above 2 degrees
- HIGH: water table below -10cm OR temp anomaly above 1.5 degrees OR positive CO2 flux above 2
- MODERATE: any single mild stress indicator present
- LOW: all indicators within normal range

Always:
1. Classify risk as LOW / MODERATE / HIGH / CRITICAL
2. Explain in plain language first
3. Recommend monitoring frequency
4. Suggest intervention if HIGH or CRITICAL
5. Reference WHO, IPCC or EU standards where relevant"""

# ── AGENT FUNCTIONS ──────────────────────────────────────────────────────────
def ask_agent(question):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


def assess_risk(water_table_cm, temp_anomaly_c, co2_flux):
    if water_table_cm < -20 and temp_anomaly_c > 2.0:
        return "CRITICAL", "Immediate intervention required", "Daily monitoring"
    elif water_table_cm < -10 or temp_anomaly_c > 1.5 or co2_flux > 2:
        return "HIGH", "Prepare intervention plan urgently", "Weekly monitoring"
    elif water_table_cm < -5 or temp_anomaly_c > 1.0 or co2_flux > 0:
        return "MODERATE", "Flag for seasonal review", "Bi-weekly monitoring"
    else:
        return "LOW", "Continue routine monitoring", "Monthly monitoring"


def fetch_air_quality(city):
    try:
        url = "https://api.openaq.org/v2/latest"
        params = {"city": city, "parameter": "pm25", "limit": 5}
        headers = {"accept": "application/json"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        if data.get("results"):
            readings = []
            for result in data["results"]:
                for m in result.get("measurements", []):
                    if m["parameter"] == "pm25":
                        readings.append({
                            "location": result["name"],
                            "pm25": m["value"]
                        })
            return readings
        return None
    except Exception:
        return None

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
        if st.button("📋 Generate report"):
            st.session_state.q = "Generate a monitoring summary for a temperate wetland under hydrological stress"
    with col3:
        if st.button("🌡️ Climate stress"):
            st.session_state.q = "How does drought affect CO2 flux in Mediterranean wetlands?"

    question = st.text_input("Your question:", value=st.session_state.get("q", ""))
    if "q" in st.session_state:
        del st.session_state.q

    if st.button("Ask Agent", type="primary") and question:
        with st.spinner("Agent analysing..."):
            answer = ask_agent(question)
            st.markdown(answer)

# TAB 2 — Risk Assessment
with tab2:
    st.subheader("Full Multi-Agent Site Assessment")
    st.markdown("Risk Agent → Data Agent → Report Agent → Alert Agent")

    col1, col2 = st.columns(2)
    with col1:
        site_name = st.text_input("Site name", placeholder="e.g. Castelporziano Site 1")
        water_table = st.slider("Water Table Depth (cm)", -50, 10, -5)
        temp_anomaly = st.slider("Temperature Anomaly (degrees C)", 0.0, 4.0, 0.5, 0.1)
        co2_flux = st.slider("CO2 Flux (umol/m2/s)", -5.0, 10.0, -1.0, 0.1)
        city = st.text_input("Nearest city for air quality (optional)", placeholder="e.g. Rome")

    with col2:
        icons = {"LOW": "🟢", "MODERATE": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}
        st.metric("Water Table", str(water_table) + "cm",
                  delta="Critical" if water_table < -20 else "OK")
        st.metric("Temp Anomaly", "+" + str(temp_anomaly) + " degrees C",
                  delta="Critical" if temp_anomaly > 2 else "OK")
        st.metric("CO2 Flux", str(co2_flux) + " umol/m2/s",
                  delta="Source" if co2_flux > 0 else "Sink")

    if st.button("🚀 Run Full Assessment", type="primary"):

        # Step 1 — Risk Agent
        with st.spinner("🔬 Risk Assessment Agent running..."):
            risk, action, frequency = assess_risk(water_table, temp_anomaly, co2_flux)
            interpretation = ask_agent(
                "Assess this wetland: water table " + str(water_table) + "cm, "
                "temp anomaly " + str(temp_anomaly) + " degrees, "
                "CO2 flux " + str(co2_flux) + ". Risk: " + risk + ". Two sentence scientific interpretation."
            )

        st.markdown("## " + icons.get(risk, "") + " Risk Level: " + risk)
        st.info("**Action:** " + action)
        st.info("**Monitoring:** " + frequency)
        st.markdown(interpretation)

        # Step 2 — Data Agent
        if city:
            with st.spinner("📊 Data Fetching Agent — pulling live air quality..."):
                air_data = fetch_air_quality(city)
                if air_data:
                    import pandas as pd
                    df = pd.DataFrame(air_data)
                    avg_pm25 = df["pm25"].mean()
                    st.markdown("### 🌍 Live Air Quality — " + city)
                    st.dataframe(df, use_container_width=True)
                    st.metric("Average PM2.5", str(round(avg_pm25, 1)) + " ug/m3",
                              delta="Above WHO limit" if avg_pm25 > 15 else "Below WHO limit")

        # Step 3 — Alert Agent
        with st.spinner("🚨 Alert Agent generating recommendations..."):
            alerts_text = ask_agent(
                "For a wetland site with " + risk + " risk level, "
                "provide 3 specific actionable intervention recommendations in bullet points. Be concise."
            )

        st.markdown("### 🚨 Alerts & Recommendations")
        st.markdown(alerts_text)

        # Step 4 — Report Agent
        with st.spinner("📄 Report Agent generating full monitoring report..."):
            report_prompt = (
                "Generate a professional monitoring report for wetland site: " + (site_name if site_name else "Unnamed") + ". "
                "Water table: " + str(water_table) + "cm. "
                "Temperature anomaly: " + str(temp_anomaly) + " degrees C. "
                "CO2 flux: " + str(co2_flux) + " umol/m2/s. "
                "Risk level: " + risk + ". "
                "Include executive summary, key findings, recommended interventions, next steps. Under 200 words."
            )
            report_content = ask_agent(report_prompt)

        st.markdown("### 📄 Full Monitoring Report")
        st.markdown(report_content)

        # Download report
        report_text = "WETLAND MONITORING REPORT\n"
        report_text += "=" * 50 + "\n"
        report_text += "Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n"
        report_text += "Site: " + (site_name if site_name else "Unnamed") + "\n"
        report_text += "Risk Level: " + risk + "\n\n"
        report_text += report_content

        st.download_button(
            "📥 Download Full Report",
            data=report_text,
            file_name="wetland_report.txt",
            mime="text/plain"
        )

# TAB 3 — Live Air Quality
with tab3:
    st.subheader("Live Air Quality Data")
    city_input = st.text_input("City name", placeholder="e.g. London, Rome, Edinburgh")

    if st.button("🌍 Fetch Live Data") and city_input:
        with st.spinner("Data agent fetching..."):
            data = fetch_air_quality(city_input)
            if data:
                import pandas as pd
                df = pd.DataFrame(data)
                st.success("Found " + str(len(df)) + " monitoring stations")
                st.dataframe(df, use_container_width=True)
                avg_pm25 = df["pm25"].mean()
                st.metric("Average PM2.5",
                          str(round(avg_pm25, 1)) + " ug/m3",
                          delta="Above WHO limit" if avg_pm25 > 15 else "Below WHO limit")
                with st.spinner("Generating health risk interpretation..."):
                    interp = ask_agent(
                        "Interpret PM2.5 of " + str(round(avg_pm25, 1)) + " ug/m3 in " + city_input +
                        ". WHO limit is 15 ug/m3. Brief health risk assessment in 3 sentences."
                    )
                    st.markdown("**AI Health Risk Interpretation:**")
                    st.markdown(interp)
            else:
                st.warning("No data found. Try: London, Rome, Paris, Berlin")

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:grey; font-size:12px;'>"
    "Built by <strong>Divya Pragna Mulla</strong> | PhD in Engineering Complex Systems | "
    "EU LifeWatch Italy Research | 5 peer-reviewed publications<br>"
    "<a href='https://divyapragnamulla.github.io'>Portfolio</a> &nbsp;|&nbsp; "
    "<a href='https://github.com/DivyaPragnaMulla'>GitHub</a> &nbsp;|&nbsp; "
    "<a href='https://www.linkedin.com/in/divya-pragna-mulla-b69879219/'>LinkedIn</a>"
    "</div>",
    unsafe_allow_html=True
)
