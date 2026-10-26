# Schrödinger's Bot 🤖👁️

A Python-based simulation exploring the **Quantum Observer Effect** in software robotics. Schrödinger's Bot is an autonomous agent that patrols in a bipedal robot state; however, the moment a human observer is detected via webcam, the "observer effect" collapses its state into a covert vehicle disguise.

---

## 🛠️ Project Architecture

- **`run_test.py`**: The main test runner that bridges computer vision, state machine logic, and real-time 3D visualization.
- **`vision.py`**: Real-time OpenCV Haar Cascade face-detection module acting as the quantum "observer".
- **`bot.py`**: Core state machine managing autonomous patrol loops, morphing progress, and telemetry logging (`telemetry_log.json`).

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed along with the required dependencies:
```bash
pip install opencv-python ursina numpy
```

### 2. Running the Simulation
Connect your webcam and execute the test runner:
```bash
python run_test.py
```

- **Unobserved State**: The bot actively patrols/roams autonomously.
- **Observed State**: Looking directly at your webcam triggers face detection, instantly collapsing the state into a vehicle disguise.
