# 6-Wheeled Rover Simulation

A complete ROS 2 Humble and Gazebo Classic simulation package for a 6-wheeled skid-steer rover equipped with an Intel RealSense D455 depth camera. Supports manual teleoperation, 3D SLAM via RTAB-Map, autonomous navigation via Nav2, and fully autonomous frontier-based exploration via explore_lite.

---

## ⚠️ Prerequisites

This package requires **Ubuntu 22.04 LTS**. If you are on a different OS, please use a dual-boot setup, virtual machine, or WSL2.

---

## 1. System Setup (For First-Time Users)

If you do not have ROS 2 Humble or Gazebo installed, run the following commands in your terminal to set up your environment.

### Install ROS 2 Humble

```bash
locale  # check for UTF-8
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y

sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu \
  $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt install ros-humble-desktop
sudo apt install ros-dev-tools
```

### Install Gazebo Classic & ROS 2 Integration

```bash
sudo apt install gazebo
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install ros-humble-xacro
```

### Install RTAB-Map (For 3D SLAM)

```bash
sudo apt install ros-humble-rtabmap-ros
```

### Install Nav2 (For Autonomous Navigation)

```bash
sudo apt update
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-pointcloud-to-laserscan
```

### Install explore_lite (For Autonomous Exploration)

> `explore_lite` is not available as an apt package for ROS 2 Humble — it must be built from source.

```bash
cd ~/rover_ws/src
git clone https://github.com/robo-friends/m-explore-ros2.git

cd ~/rover_ws
rosdep install --from-paths src --ignore-src -r -y

# Build the messages package first, then explore_lite
colcon build --symlink-install --packages-select explore_lite_msgs
source install/setup.bash

colcon build --symlink-install --packages-select explore_lite
source install/setup.bash
```

Verify the build succeeded:

```bash
ros2 pkg list | grep explore
# Expected output:
# explore_lite
# explore_lite_msgs
```

---

## 2. Workspace Setup

Once all dependencies are installed, set up your workspace and clone this repository.

```bash
# Source the base ROS 2 installation
source /opt/ros/humble/setup.bash

# Create a workspace
mkdir -p ~/rover_ws/src
cd ~/rover_ws/src

# Clone the repository
git clone https://github.com/spabhut/ProjectVanguard.git rover

# Install missing dependencies automatically
cd ~/rover_ws
rosdep init
rosdep update
rosdep install --from-paths src -y --ignore-src

# Build the workspace
colcon build --symlink-install
```

---

## 3. Running the Simulation

Every time you open a new terminal, source the workspace first:

```bash
cd ~/rover_ws
source install/setup.bash
```

---

### Mode A — Manual Teleoperation (3 terminals)

#### Terminal 1 — Gazebo Simulation

```bash
cd ~/rover_ws && source install/setup.bash
ros2 launch rover rover.launch.py
```

#### Terminal 2 — SLAM (RTAB-Map)

```bash
cd ~/rover_ws && source install/setup.bash
ros2 launch rover slam.launch.py
```

#### Terminal 3 — Keyboard Teleoperation

```bash
cd ~/rover_ws && source install/setup.bash
ros2 run rover teleop_key
```

---

### Mode B — Autonomous Navigation with Nav2 (3 terminals)

#### Terminal 1 — Gazebo Simulation

```bash
cd ~/rover_ws && source install/setup.bash
ros2 launch rover rover.launch.py
```

#### Terminal 2 — SLAM (RTAB-Map)

```bash
cd ~/rover_ws && source install/setup.bash
ros2 launch rover slam.launch.py
```

#### Terminal 3 — Nav2 Navigation Stack

```bash
cd ~/rover_ws && source install/setup.bash
ros2 launch rover nav2.launch.py
```

Use the **2D Goal Pose** tool in RViz to send navigation goals.

---

### Mode C — Autonomous Exploration with explore_lite (4 terminals)

The rover will autonomously explore the entire map using frontier-based exploration. No manual goal-setting needed.

#### Terminal 1 — Gazebo Simulation

```bash
cd ~/rover_ws && source install/setup.bash
ros2 launch rover rover.launch.py
```

#### Terminal 2 — SLAM (RTAB-Map)

```bash
cd ~/rover_ws && source install/setup.bash
ros2 launch rover slam.launch.py
```

#### Terminal 3 — Nav2 Navigation Stack

```bash
cd ~/rover_ws && source install/setup.bash
ros2 launch rover nav2.launch.py
```

#### Terminal 4 — Autonomous Exploration

```bash
cd ~/rover_ws && source install/setup.bash
ros2 launch rover explore.launch.py
```

The rover will now autonomously navigate to frontier boundaries (the edge between known free space and unknown space) until the entire map is explored.

To monitor exploration progress in RViz, add the following displays:
- **MarkerArray** → `/explore/frontiers` — shows active frontier candidates
- **Map** → `/map` — the live RTAB-Map occupancy grid
- **Path** → `/plan` — the current planned path

#### If the rover stops early with "No frontiers found"

This can happen when small unexplored patches are filtered out or lie in the camera's blind spot. Fix it by triggering a spin to expose the rear area:

```bash
# Option 1 — Nav2 spin behaviour (recommended)
ros2 action send_goal /spin nav2_msgs/action/Spin "{target_yaw: 3.14}"

# Option 2 — Direct velocity command
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.8}}"
```

Then relaunch explore_lite in Terminal 4:

```bash
ros2 launch rover explore.launch.py
```

---

## Package Structure

```
rover/
├── CMakeLists.txt
├── package.xml
├── README.md
├── config/
│   ├── nav2_params.yaml      # Nav2 navigation parameters
│   └── explore.yaml          # explore_lite frontier exploration parameters
├── include/
│   └── rover/                # C++ headers (if any)
├── launch/
│   ├── rover.launch.py       # Gazebo simulation launch
│   ├── slam.launch.py        # SLAM (RTAB-Map) launch
│   ├── nav2.launch.py        # Nav2 navigation stack launch
│   └── explore.launch.py     # Autonomous exploration launch
├── rviz/
│   └── rover.rviz            # Pre-configured RViz2 layout
├── scripts/
│   └── teleop_key.py         # Keyboard teleoperation script
├── src/                      # C++ source files (if any)
├── urdf/
│   └── rover.xacro           # Robot description with D455 camera
└── worlds/
    └── rover.world           # Custom Gazebo world
```

---

## Troubleshooting

**Gazebo doesn't open / crashes immediately**
```bash
source /usr/share/gazebo/setup.sh
```

**`colcon build` fails with missing packages**
```bash
rosdep install --from-paths src -y --ignore-src
```

**RViz shows no robot model**
```bash
ros2 topic echo /robot_description
```

**explore_lite fails to build — `explore_lite_msgs` not found**
```bash
# Always build the messages package before explore_lite
colcon build --symlink-install --packages-select explore_lite_msgs
source install/setup.bash
colcon build --symlink-install --packages-select explore_lite
source install/setup.bash
```

**explore_lite stops immediately — "No frontiers found"**

The `min_frontier_size` in `config/explore.yaml` may be too large for the remaining unexplored area.
Lower it and relaunch:
```bash
# In config/explore.yaml, set:
# min_frontier_size: 0.1
ros2 launch rover explore.launch.py
```

**explore_lite cannot see the area behind the rover**

The D455 camera only faces forward. Spin the rover to bring the rear area into view:
```bash
ros2 action send_goal /spin nav2_msgs/action/Spin "{target_yaw: 3.14}"
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.