# Quickstart Guide: Physical AI & Humanoid Robotics

## Prerequisites

- Ubuntu 22.04 LTS
- ROS 2 Humble Hawksbill installed
- Python 3.10+
- Gazebo installed
- NVIDIA Isaac Python packages (if using Isaac Sim)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install ROS 2 dependencies**
   ```bash
   # Source ROS 2 environment
   source /opt/ros/humble/setup.bash
   
   # Install additional ROS packages
   sudo apt update
   sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-gazebo-plugins
   ```

3. **Create a colcon workspace**
   ```bash
   mkdir -p ~/physical_ai_ws/src
   cd ~/physical_ai_ws
   ```

4. **Copy the project files to the workspace**
   ```bash
   cp -r <path-to-project>/src/* ~/physical_ai_ws/src/
   ```

5. **Install Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

6. **Build the workspace**
   ```bash
   cd ~/physical_ai_ws
   source /opt/ros/humble/setup.bash
   colcon build --packages-select brain nervous_system body
   ```

7. **Source the workspace**
   ```bash
   source install/setup.bash
   ```

## Running the Simulation

1. **Launch the simulation environment**
   ```bash
   ros2 launch simulation bringup.launch.py
   ```

2. **In a new terminal, run the command processor**
   ```bash
   cd ~/physical_ai_ws
   source install/setup.bash
   ros2 run brain command_processor
   ```

3. **In another terminal, run the planning system**
   ```bash
   cd ~/physical_ai_ws
   source install/setup.bash
   ros2 run brain planning_system
   ```

## Basic Usage

### Sending a Command
Use the API to send a natural language command:

```bash
curl -X POST http://localhost:8080/api/v1/commands \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Go to the red box and pick it up",
    "type": "text",
    "user_id": "your-user-id"
  }'
```

### Checking Command Status
```bash
curl http://localhost:8080/api/v1/commands/{command_id}
```

### Checking Plan Status
```bash
curl http://localhost:8080/api/v1/plans/{plan_id}
```

## Architecture Overview

The system follows the three-part architecture as mandated by the project constitution:

1. **Brain**: Contains AI models, planning algorithms, and reasoning systems
   - Planning system that converts natural language to action sequences
   - LLM interface for high-level reasoning
   - Decision-making components

2. **Nervous System**: Consists of ROS 2 nodes, topics, and services
   - Communication layer between Brain and Body
   - Message passing infrastructure
   - Service interfaces for synchronous operations

3. **Body**: Includes the robot and simulation environment
   - Robot model with actuators and sensors
   - Physical simulation of the environment
   - Control systems for actuators

## Key Components

- `brain/`: AI and planning components
- `nervous_system/`: ROS 2 nodes and communication
- `body/`: Robot models and simulation
- `simulation/`: World models and simulation launch files
- `common/`: Shared utilities and configuration

## Troubleshooting

- If ROS 2 packages don't build, ensure you've sourced the ROS environment
- If simulation doesn't start, check that Gazebo is properly installed
- If LLM integration fails, confirm API keys are properly configured