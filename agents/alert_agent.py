
from groq import Groq

class AlertAgent:
    """Specialist subagent for alerts and intervention recommendations"""
    
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
        self.system_prompt = """You are a specialist in wetland ecosystem 
        intervention and conservation. Provide specific, actionable 
        recommendations based on risk level. Reference EU Water Framework 
        Directive and IPCC guidelines."""
    
    def check(self, risk_result):
        """Generate alerts and interventions based on risk"""
        
        risk_level = risk_result["level"]
        alerts = []
        
        if risk_level == "CRITICAL":
            alerts.append("🔴 CRITICAL ALERT: Immediate intervention required")
            alerts.append("🔴 Water table management must begin within 24 hours")
            alerts.append("🔴 Notify conservation authority immediately")
        elif risk_level == "HIGH":
            alerts.append("🟠 HIGH ALERT: Site requires urgent attention")
            alerts.append("🟠 Prepare intervention plan within 48 hours")
            alerts.append("🟠 Increase monitoring to daily checks")
        elif risk_level == "MODERATE":
            alerts.append("🟡 MODERATE: Site showing stress indicators")
            alerts.append("🟡 Schedule site inspection within 2 weeks")
        else:
            alerts.append("🟢 LOW: Site within normal parameters")
            alerts.append("🟢 Continue routine monitoring schedule")
        
        # AI recommendation
        prompt = f"""For a wetland site with {risk_level} risk level, 
        provide 3 specific, actionable intervention recommendations 
        in bullet points. Be concise and practical."""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {
            "alerts": alerts,
            "recommendations": response.choices[0].message.content,
            "risk_level": risk_level
        }
