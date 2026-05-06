
import requests

class DataAgent:
    """Specialist subagent for fetching live environmental data"""
    
    def __init__(self):
        self.openaq_base = "https://api.openaq.org/v2"
    
    def fetch_air_quality(self, city):
        """Fetch live PM2.5 data from OpenAQ"""
        try:
            url = f"{self.openaq_base}/latest"
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
                                "pm25": m["value"],
                                "last_updated": m["lastUpdated"]
                            })
                
                if readings:
                    avg = sum(r["pm25"] for r in readings) / len(readings)
                    who_limit = 15
                    return {
                        "city": city,
                        "readings": readings,
                        "average_pm25": round(avg, 2),
                        "who_limit": who_limit,
                        "exceeds_who": avg > who_limit,
                        "status": "Above WHO limit" if avg > who_limit else "Below WHO limit"
                    }
            return None
        except Exception as e:
            return {"error": str(e)}
    
    def fetch_fluxnet_info(self, site_id=None):
        """Returns FluxNet dataset information"""
        return {
            "source": "FluxNet",
            "url": "https://fluxnet.org",
            "description": "Global carbon flux measurements",
            "note": "Download data directly from fluxnet.org for site-specific analysis"
        }
