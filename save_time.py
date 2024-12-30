import json
from datetime import datetime

class TimeManager:
    def __init__(self, filename="race_times.json"):
        self.filename = filename
        self.times = self._load_times()
    
    def _load_times(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_time(self, elapsed_time):
        time_entry = {
            "time": round(elapsed_time, 2),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.times.append(time_entry)
        self.times.sort(key=lambda x: x["time"])
        
        with open(self.filename, 'w') as file:
            json.dump(self.times, file, indent=4)
