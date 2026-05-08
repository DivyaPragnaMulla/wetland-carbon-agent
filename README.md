# 🌿 Wetland Carbon Monitoring Agent

An AI-powered environmental monitoring agent that analyses wetland 
ecosystem health, carbon sink-to-source transition risk, and generates 
professional monitoring reports using natural language.

## 🔬 Research Background

Built on real research methodology from a postdoctoral contract at the 
**University of Salento, Italy** (2024–2026), working on EU-funded 
**LifeWatch Italy** wetland ecosystem monitoring across 10 sites in 
Castelporziano, Rome. Integrates FluxNet, NASA, and ERA5 open datasets.

## ✨ Features

- 💬 **Ask the Agent** — natural language Q&A on wetland carbon flux
- 📊 **Site Risk Assessment** — interactive sliders → AI monitoring report
- 🔴 **Risk Classification** — LOW / MODERATE / HIGH / CRITICAL
- 📥 **Downloadable Reports** — professional monitoring summaries
- 🌍 **WHO & IPCC Standards** — scientifically grounded thresholds

## 🚀 Live Demo

👉 [Try the live agent](https://wetland-carbon-agent-cqlcrrplcstxzrzklasjr8.streamlit.app/)

## 🛠️ Built With

- [Groq](https://groq.com) — LLM inference (Llama 3.3 70B)
- [Streamlit](https://streamlit.io) — web interface
- [OpenAQ](https://openaq.org) — live air quality data
- Python 3.12

## 📊 Risk Classification Logic

| Risk | Water Table | Temp Anomaly | CO₂ Flux |
|------|------------|--------------|----------|
| 🔴 CRITICAL | < -20cm | > 2°C | > 2 μmol/m²/s |
| 🟠 HIGH | < -10cm | > 1.5°C | > 1 μmol/m²/s |
| 🟡 MODERATE | < -5cm | > 1.0°C | > 0 μmol/m²/s |
| 🟢 LOW | Normal | Normal | Negative |

## 📚 Scientific Basis

- WHO AirQ+ environmental health frameworks
- IPCC climate thresholds (>2°C critical threshold)
- EU Water Framework Directive standards
- FluxNet global carbon flux datasets
- LifeWatch Italy ecological monitoring infrastructure

## 👩‍🔬 Author

**Divya Pragna Mulla**
PhD in Engineering Complex Systems | Environmental Data Analyst

- 🌐 [Portfolio](https://divyapragnamulla.github.io)
- 💼 [LinkedIn](https://www.linkedin.com/in/divya-pragna-mulla-b69879219/)
- 🐙 [GitHub](https://github.com/DivyaPragnaMulla)
- ✅ Global Talent Visa — Right to Work in UK

## 📄 Publications

- Travel Air IQ: A Tool for Air Quality-Aware Tourists — Springer Nature [2024](https://link.springer.com/chapter/10.1007/978-3-031-53555-0_59)
- 5 peer-reviewed publications in Springer Nature and Scientific Reports

## 📜 Certifications

- Anthropic — Introduction to Agent Skills [2026]
- Microsoft Agent Explorer — Founderz x Microsoft [2026]
