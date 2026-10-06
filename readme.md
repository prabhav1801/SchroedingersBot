# Schrödinger's Bot 🤖🚗

A machine which alters its essential character merely because it is observed.

This is an interactive computer vision simulation developed using Python, OpenCV, and Ursina 3D; it has been inspired by quantum mechanics and the film *Transformers*, and includes an autonomous robot which carries out a routine patrol until a human observer looks into the webcam at which point the robot immediately abandons its cover and deploys a vehicle disguise.

## Concept & Mechanics
- **The Observer Effect:** It tracks the Yaw and Pitch angles in real time by using OpenCV and 3D-to-2D head-pose estimation (solvePnP) with input from a webcam.
- **State Hysteresis:** The system includes directional thresholds and uses multi-frame debounce filters to avoid state-flickering caused by camera noise.
- **Articulated Morphing:** It smoothly interpolates custom 3D primitives on a single rig when changing from a bipedal robot configuration to a vehicle configuration.
- **Asynchronous Pipeline:** This feature enables video capture to take place on a background thread so that camera polling does not block the Ursina 3D render loop.

## Tech Stack
- Python
- OpenCV (`cv2`)
- Ursina Engine
- NumPy