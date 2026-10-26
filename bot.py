import time
import json

class TransformerStateMachine:
    def __init__(self):
        self.state = "ROBOT_PATROL"
        self.morph_progress = 0.0
        self.telemetry_log = []

    def update(self, is_observed):
        start_time = time.time()
        
        if is_observed:
            self.state = "VEHICLE_DISGUISE"
            self.morph_progress = min(1.0, self.morph_progress + 0.1)
        else:
            self.state = "ROBOT_PATROL"
            self.morph_progress = max(0.0, self.morph_progress - 0.1)
            
        latency = (time.time() - start_time) * 1000.0
        
        self.telemetry_log.append({
            "timestamp": time.time(),
            "state": self.state,
            "morph_progress": self.morph_progress,
            "latency_ms": latency
        })
        
        return self.state, self.morph_progress

    def save_telemetry(self, filename="telemetry_log.json"):
        with open(filename, "w") as f:
            json.dump(self.telemetry_log, f, indent=4)
