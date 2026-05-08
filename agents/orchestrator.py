
from groq import Groq
from agents.risk_agent import RiskAgent
from agents.data_agent import DataAgent
from agents.report_agent import ReportAgent
from agents.alert_agent import AlertAgent

class OrchestratorAgent:
    """Main agent that coordinates all subagents"""
    
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.risk_agent = RiskAgent(api_key)
        self.data_agent = DataAgent()
        self.report_agent = ReportAgent(api_key)
        self.alert_agent = AlertAgent(api_key)
        
        self.system_prompt = """You are the main orchestrator for a wetland 
        carbon monitoring system. You coordinate specialist subagents to analyse
        ecosystem health, assess carbon flux risk, and generate monitoring reports.
        
        Always classify risk as LOW / MODERATE / HIGH / CRITICAL.
        Reference WHO, IPCC and EU Water Framework Directive standards.
        Be scientific but accessible — plain language first, detail on request."""
    
    def run(self, user_input, mode="chat"):
        """Main entry point — routes to appropriate subagents"""
        
        if mode == "assess":
            return self._run_full_assessment(user_input)
        else:
            return self._chat(user_input)
    
    def _chat(self, question):
        """General Q&A about wetland science"""
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    
    def _run_full_assessment(self, params):
        """Full pipeline — calls all subagents in sequence"""
        water_table = params.get("water_table")
        temp_anomaly = params.get("temp_anomaly")
        co2_flux = params.get("co2_flux")
        site_name = params.get("site_name", "Unnamed site")
        city = params.get("city", "")
        
        # Step 1 — Risk subagent
        risk_result = self.risk_agent.assess(water_table, temp_anomaly, co2_flux)
        
        # Step 2 — Data subagent (if city provided)
        air_data = None
        if city:
            air_data = self.data_agent.fetch_air_quality(city)
        
        # Step 3 — Report subagent
        report = self.report_agent.generate(
            site_name, water_table, temp_anomaly, 
            co2_flux, risk_result, air_data
        )
        
        # Step 4 — Alert subagent
        alerts = self.alert_agent.check(risk_result)
        
        return {
            "risk": risk_result,
            "air_quality": air_data,
            "report": report,
            "alerts": alerts
        }
