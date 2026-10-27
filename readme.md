# Schrödinger's Bot 🤖👁️

A hybrid Python/C++ simulation exploring the **Quantum Observer Effect** in distributed robotics. Schrödinger's Bot patrols in a bipedal robot state; when an external observer is detected via an OpenCV Haar-cascade face detector in Python, the state transitions into a covert vehicle disguise.

---

## 🛠️ Project Architecture

- **`vision_node.cpp`**: C++ ROS 2 node publishing velocity commands (`geometry_msgs/Twist`) using standard `get_logger()` syntax, acting as a structural scaffold for future ArUco pose control.
- **`CMakeLists.txt` & `package.xml`**: ROS 2 package configuration managing dependencies (`rclcpp`, `geometry_msgs`, OpenCV).
- **`run_test.py`**: Python test runner synchronizing telemetry and 3D visualization.
- **`vision.py` & `bot.py`**: Core vision module (Face tracking) and state machine managing patrol loops and state-machine update timing metrics (`telemetry_log.json`).

---

## 🚀 Getting Started

### 1. Prerequisites
Install required Python dependencies:
```bash
pip install opencv-python ursina numpy
```

### 2. Running the Simulation
Execute the test runner:
```bash
python run_test.py
```