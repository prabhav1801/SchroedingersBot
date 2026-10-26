import time
import json
import numpy as np
from vision import VisionPoseEstimator

class SchrodingerBotSystem:
    """
    Upgraded autonomous vehicle state machine with decoupled perception,
    asynchronous execution, and telemetry logging.
    """
    def __init__(self):
        self.state = "IDLE"
        self.vision = VisionPoseEstimator()
        self.telemetry_log = []

    def step(self, frame):
        start_time = time.time()
        
        found, tvec, rvec = self.vision.get_pose(frame)
        
        if found:
            self.state = "ACTIVE_TRACKING"
            cmd_velocity = -0.5 * tvec[0:2]
        else:
            self.state = "SEARCHING"
            cmd_velocity = np.zeros(2)
            
        latency_ms = (time.time() - start_time) * 1000.0
        
        log_entry = {
            "timestamp": time.time(),
            "state": self.state,
            "latency_ms": latency_ms,
            "pose": tvec.tolist() if found else None
        }
        self.telemetry_log.append(log_entry)
        
        return self.state, cmd_velocity

    def save_telemetry(self, filename="telemetry_log.json"):
        with open(filename, "w") as f:
            json.dump(self.telemetry_log, f, indent=4)

