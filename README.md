# Schrödinger's Bot

Small vision-triggered state-machine demo. A cube-built robot patrols in a 3D scene (Ursina). When an OpenCV Haar-cascade face detector finds a face in the webcam feed, the robot switches to a flattened vehicle form; when the face leaves, it switches back. Each update is logged to JSON.

## Files

| File | Purpose |
| :--- | :--- |
| `run_test.py` | Ursina scene, webcam loop, robot/vehicle rendering. Press `q` to quit and write the telemetry log. |
| `vision.py` | `ObserverVision`: Haar-cascade frontal-face detection on each frame. |
| `bot.py` | `TransformerStateMachine`: two states (`ROBOT_PATROL`, `VEHICLE_DISGUISE`), morph progress, telemetry. |
| `vision_node.cpp`, `CMakeLists.txt`, `package.xml` | ROS 2 (rclcpp) node scaffold, see below. |

## Telemetry

On quit, `telemetry_log.json` gets one entry per update: timestamp, state, morph progress, and `update_time_ms` (time spent inside `TransformerStateMachine.update()`, not camera-to-decision latency).

## ROS 2 scaffold

`vision_node.cpp` opens the webcam and publishes a constant `geometry_msgs/Twist` (`cmd_vel`, 0.5 m/s forward) on a ~60 Hz timer. It does not use the camera frame yet; ArUco detection and pose estimation are not implemented. It is not connected to the Python demo.

## Run

```bash
pip install -r requirements.txt
python run_test.py
```

Needs a webcam. The ROS 2 node is built separately with colcon in a ROS 2 workspace.
