
from groq import Groq
from datetime import datetime

class ReportAgent:
    """Specialist subagent for generating monitoring reports"""
    
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
        self.system_prompt = """You are a specialist in writing professional 
        environmental monitoring reports. Write clearly, concisely and 
        scientifically. Always include: executive summary, key findings, 
        recommended interventions, and next steps. Keep under 200 words 
        unless a full report is requested."""
    
    def generate(self, site_name, water_table, temp_anomaly, co2_flux, risk_result, air_data=None):
        """Generate a full monitoring report"""
        
        air_section = ""
        if air_data and not air_data.get("error"):
            air_section = f"""
            Air Quality Data:
            - City: {air_data.get("city")}
            - Average PM2.5: {air_data.get("average_pm25")} μg/m³
            - WHO Status: {air_data.get("status")}"""
        
        prompt = f"""Generate a professional wetland monitoring report:
        
        Site: {site_name}
        Date: {datetime.now().strftime("%Y-%m-%d")}
        
        Ecosystem Parameters:
        - Water table: {water_table}cm
        - Temperature anomaly: {temp_anomaly}°C
        - CO₂ flux: {co2_flux} μmol/m²/s
        - Risk level: {risk_result["level"]}
        - Required action: {risk_result["action"]}
        - Monitoring frequency: {risk_result["frequency"]}
        {air_section}
        
        Write a professional report with executive summary,
        key findings, interventions and next steps."""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {
            "content": response.choices[0].message.content,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "site": site_name
        }
