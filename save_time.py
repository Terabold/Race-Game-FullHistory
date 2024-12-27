# save_times.py

import json
from datetime import datetime

class TimeManager:
    def __init__(self, filename="race_times.json"):
        self.filename = filename
        self.times = self._load_times()
    
    def _load_times(self):
        """Load existing times from file, or create new file if it doesn't exist"""
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
        
        # Sort times from fastest to slowest
        self.times.sort(key=lambda x: x["time"])
        
        # Save to file
        with open(self.filename, 'w') as file:
            json.dump(self.times, file, indent=4)
        
        return len(self.times)  # Return position in leaderboard

    def get_times(self):
        return self.times
    
    def clear_times(self):
        self.times = []
        with open(self.filename, 'w') as file:
            json.dump(self.times, file)