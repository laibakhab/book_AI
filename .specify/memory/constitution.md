



<!--
Sync Impact Report:
Version change: none (new file) → 1.0.0
Modified principles: none (new principles added)
Added sections: All sections (new constitution with 6 principles and additional sections)
Removed sections: none
Templates requiring updates: [] (✅ no updates needed - existing templates compatible)
Follow-up TODOs: none
-->
# Physical AI & Humanoid Robotics Constitution

## Core Principles

### Physical AI First
AI systems must operate in the real or simulated physical world. Embodied intelligence is mandatory for all projects.

### Clear System Separation
The architecture follows a clear separation: Brain (AI models, planning, reasoning), Nervous System (ROS 2 nodes, topics, services), and Body (Robot or simulator environments like Gazebo/Isaac).

### Simulation-First Approach
All designs must be validated in simulation before real hardware deployment. Prefer Isaac Sim and Gazebo for development and testing.

### Practical Over Theoretical
Focus on deployable systems. Avoid abstract ML theory unless directly needed for robot functionality. Emphasize working implementations over theoretical concepts.

### Modularity
Every component must be replaceable and modular. Systems must be designed for teaching purposes and hackathon demonstrations.

### Tooling Constraints
Use ROS 2 (Python), NVIDIA Isaac ecosystem, Jetson Orin for edge computing deployments, and LLMs only for planning and language understanding tasks.

## Technology Stack Requirements

Projects must utilize the following technology stack:
- ROS 2 (Python) for robotics middleware
- NVIDIA Isaac ecosystem (Isaac Sim, Isaac ROS packages)
- Jetson Orin for edge computing deployments
- LLMs restricted to planning and language understanding tasks
- Gazebo simulation environment when not using Isaac Sim

## Development Workflow

The project follows a systematic development workflow:
- All implementations start in simulation
- Components are developed modularly with clear interfaces
- Emphasis on step-by-step breakdowns for educational purposes
- Documentation must include clear architecture diagrams
- Content suitable for technical textbook inclusion

## Governance

This constitution governs all development activities within the Physical AI & Humanoid Robotics project. All team members must follow these principles. Amendments require documentation and approval by the project leads. All PRs and reviews must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-14 | **Last Amended**: 2025-12-14
