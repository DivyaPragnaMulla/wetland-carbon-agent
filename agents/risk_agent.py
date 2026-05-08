
from groq import Groq

class RiskAgent:
    """Specialist subagent for wetland risk assessment"""
    
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
        self.system_prompt = """You are a specialist in wetland carbon flux 
        risk assessment. Use these exact thresholds:
        - CRITICAL: water table < -20cm AND temp anomaly > 2°C
        - HIGH: water table < -10cm OR temp anomaly > 1.5°C OR CO2 flux > 2
        - MODERATE: any single mild stress indicator present
        - LOW: all indicators within normal range
        
        Always reference IPCC thresholds and EU Water Framework Directive."""
    
    def assess(self, water_table_cm, temp_anomaly_c, co2_flux):
        """Rule-based + AI risk assessment"""
        
        # Rule-based classification
        if water_table_cm < -20 and temp_anomaly_c > 2.0:
            risk = "CRITICAL"
            action = "Immediate intervention required"
            frequency = "Daily monitoring"
        elif water_table_cm < -10 or temp_anomaly_c > 1.5 or co2_flux > 2:
            risk = "HIGH"
            action = "Prepare intervention plan urgently"
            frequency = "Weekly monitoring"
        elif water_table_cm < -5 or temp_anomaly_c > 1.0 or co2_flux > 0:
            risk = "MODERATE"
            action = "Flag for seasonal review"
            frequency = "Bi-weekly monitoring"
        else:
            risk = "LOW"
            action = "Continue routine monitoring"
            frequency = "Monthly monitoring"
        
        # AI interpretation
        prompt = f"""Assess this wetland site:
        Water table: {water_table_cm}cm
        Temperature anomaly: {temp_anomaly_c}°C
        CO2 flux: {co2_flux} μmol/m²/s
        Rule-based risk: {risk}
        
        Provide a 2-sentence scientific interpretation."""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {
            "level": risk,
            "action": action,
            "frequency": frequency,
            "interpretation": response.choices[0].message.content,
            "inputs": {
                "water_table_cm": water_table_cm,
                "temp_anomaly_c": temp_anomaly_c,
                "co2_flux": co2_flux
            }
        }
