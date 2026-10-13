# 3-DOF Planar Arm Kinematics and Dynamics Simulator

![Project Status: In Development](https://img.shields.io/badge/STATUS-WIP-blue)
![Version: 0.2.0](https://img.shields.io/badge/VERSION-0.2.0-orange)

> A Python-based GUI simulator built with Tkinter for a 3-DOF planar robotic arm. The application implements forward and inverse kinematics, supports elbow-up and elbow-down IK configurations, and allows users to preview or apply a target end-effector pose `(x, y, φ)`. The project is being developed toward trajectory, dynamics, and joint-torque simulation.

## Features
- 3-DOF planar robotic arm visualization
- Configurable link lengths
- End-effector target position input `(x, y)`
- End-effector orientation input `φ`
- Forward kinematics calculation
- Inverse kinematics calculation
- Elbow-up and elbow-down inverse-kinematics solutions
- Target configuration preview using a ghost robot visualization
- Direct application of the selected IK configuration through the `Move` control
- Simulation State panel displaying:
  - Joint positions
  - End-effector position
  - Joint angles `θ1`, `θ2`, and `θ3`
- Cartesian grid visualization
- Light and dark appearance modes
- Tabbed Tkinter interface for:
  - Simulation
  - Robot configuration
  - Dynamics
  - Settings
- Animated Cartesian `MoveL`-style motion
- Animated end-effector orientation changes with fixed `(x, y)` position
- Real-time Simulation State updates during motion

## Simulation Examples

The simulator can calculate both inverse-kinematics branches for a reachable
target pose. The selected configuration can first be previewed as a lighter
ghost representation before being applied to the robot model.

The following examples use:
- `L1 = 9`
- `L2 = 6`
- `L3 = 3`
- Target pose: `(x = 7, y = 10, φ = 45°)`

<figure>
    <img src="assets/readme_img/elbow_up_preview.jpg" alt="Elbow-up inverse kinematics preview" width="600">
    <figcaption>Elbow-up inverse-kinematics configuration for the target pose (x = 7, y = 10, φ = 45°) with link lengths [9, 6, 3]. The target configuration is displayed as a lighter ghost arm while preserving the robot's current configuration.</figcaption>
</figure>

<figure>
    <img src="assets/readme_img/elbow_down_preview.jpg" alt="Elbow-down inverse kinematics preview" width="600">
    <figcaption>Elbow-down inverse-kinematics configuration for the target pose (x = 7, y = 10, φ = 45°) with link lengths [9, 6, 3]. The target configuration is displayed as a lighter ghost arm while preserving the robot's current configuration.</figcaption>
</figure>

<figure>
    <img src="assets/readme_img/elbow_down_move.jpg" alt="Robot moved to elbow-down configuration" width="600">
    <figcaption>Elbow-down inverse-kinematics configuration for the target pose (x = 7, y = 10, φ = 45°) with link lengths [9, 6, 3]. The selected configuration is applied to the robot, and the simulation state panel displays the resulting joint positions and joint angles.</figcaption>
</figure>

## Interface

The application is organized into four tabs:

- **Simulation:** target pose, elbow configuration, preview, movement controls, and current robot state.
- **Robot:** manipulator geometry and link-length configuration.
- **Dynamics:** interface for mass and payload parameters; calculations are currently under development.
- **Settings:** application appearance and visualization settings.

## Kinematic Model

The simulator implements forward and inverse kinematics for a 3-DOF planar manipulator.

The end-effector pose is defined by:

$$x = L_1\cos\theta_1+L_2\cos(\theta_1+\theta_2)+L_3\cos(\theta_1+\theta_2+\theta_3)$$

$$y = L_1\sin\theta_1+L_2\sin(\theta_1+\theta_2)+L_3\sin(\theta_1+\theta_2+\theta_3)$$

$$\phi = \theta_1+\theta_2+\theta_3$$

Inverse kinematics is used to obtain the joint angles from a desired end-effector pose `(x, y, φ)`.

For the full mathematical derivation, see:

[Full Kinematic Model](docs/Kinematic_Model.pdf)

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Current Development

### Recent updates:

- Added animated robot motion using a basic `MoveL`-style cartesian trajectory.
- The end-effector position is interpolated linearly between the current pose and the target pose.
- Inverse kinematics is calculated for each trajectory point to generate the corresponding joint configurations.
- Added animated end-effector orientation changes when the target position `(x, y)` remains unchanged.
- The Simulation State panel updates joint positions and joint angles during the movement.
- Elbow-up and elbow-down configurations remain available for preview and target selection.

### Currently working on:

- Improving trajectory continuity between elbow configurations.
- Adding joint limits.
- Adding collision detection.
- Implementing configurable velocity and acceleration profiles.
- Preparing the foundation for `MoveJ` and `MoveC`.

## Current Limitations

- Joint limits are not yet implemented.
- Collision detection is not implemented.
- `Move` currently uses a basic linear cartesian trajectory without velocity or acceleration profiles.
- The `Simulate` control is currently a UI placeholder and does not yet perform a dynamic simulation.
- Velocity and acceleration profiles are not yet implemented.
- Robot dynamics and joint torque calculations are not yet implemented.
- The current implementation focuses primarily on position-level kinematics.

> **Note:** Dynamic simulation is under development. The current `Simulate` button is reserved for the future dynamics and trajectory execution workflow.

## Development Roadmap

| Category | Progress | Features | Status |
| :--- | :---: | :--- | :---: |
| **Core Simulation** | `■■■■■■■■□□` 80% | Forward/inverse kinematics, configurable link lengths, elbow-up/down IK solutions, target preview, animated MoveL motion, and live pose updates.<br>**Pending:** joint limits, collision detection, and advanced motion control. | 🔄 In progress |
| **Visualization** | `■■■■■■■■□□` 80% | Tabbed Tkinter GUI, Cartesian grid, light/dark mode, ghost configuration preview, and live joint/end-effector state display.<br>**Pending:** graphical end-effector orientation and additional visualization controls. | 🔄 In progress |
| **Trajectory Planning** | `■■■■□□□□□□` 40% | Basic `MoveL` Cartesian interpolation, animated motion, and orientation-only movement are implemented.<br>**Pending:** MoveJ, MoveC, configurable velocity/acceleration profiles, trajectory validation, and improved continuity handling. | 🔄 Early development |
| **Advanced Kinematics** | `□□□□□□□□□□` 0% | Jacobian calculation and velocity analysis. | ⏳ Planned |
| **Dynamics** | `□□□□□□□□□□` 0% | Dynamic simulation, robot dynamics, and joint torque calculation. | ⏳ Planned |
