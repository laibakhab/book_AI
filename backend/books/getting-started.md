---
sidebar_position: 1
---

# Getting Started with ROS 2

The Robot Operating System 2 (ROS 2) is a flexible framework for writing robot software. Despite its name, ROS 2 is not an actual operating system but rather a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

## What is ROS 2?

ROS 2 is the evolution of the original ROS framework, designed to address the needs of commercial robotics applications. Key improvements include:

- **Real-Time Support**: Deterministic behavior for time-critical applications
- **Multi-Robot Systems**: Better support for distributed robotic systems
- **Improved Security**: Proper authentication and encryption
- **Quality of Service**: Reliable communication in challenging environments
- **Cross-Platform Compatibility**: Runs on Linux, Windows, and macOS

## Core Concepts

### Nodes
A node is a process that performs computation. ROS 2 is designed to have many nodes that all work together to form a complete robot application.

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
```

### Topics and Messages
Topics allow nodes to communicate with each other by passing messages. Messages are the data structures that travel along topics.

### Services
Services provide a request/response communication pattern between nodes.

### Actions
Actions are similar to services but designed for long-running tasks that may need to be monitored, canceled, or provide feedback.

## ROS 2 Architecture

ROS 2 uses a DDS (Data Distribution Service) implementation for communication between nodes:

- **Communication Layer**: Implements the publish/subscribe and client/server patterns
- **Middleware Layer**: Manages discovery, delivery, and serialization of messages
- **Application Layer**: Contains the user-defined nodes and their logic

## Installation

For Ubuntu systems, install ROS 2 with:

```bash
# Setup locale
sudo locale-gen en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

# Add ROS 2 apt repository
sudo apt update && sudo apt install curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros key | sudo gpg --dearmor -o /usr/share/keyrings/ros keyring.gpg

# Install ROS 2 packages
sudo apt update
sudo apt install ros-<DISTRO>-desktop
```

Replace `<DISTRO>` with the appropriate ROS distribution (Humble Hawksbill, Iron Irwini, etc.).

:::note
ROS 2 addresses many limitations of the original ROS framework, making it suitable for production robotics applications.
:::

## Learning Objectives

After completing this chapter, you will understand:
- The core concepts and architecture of ROS 2
- How to create basic ROS 2 nodes
- The differences between ROS 1 and ROS 2
- How to install and configure ROS 2
- Communication patterns in ROS 2 (topics, services, actions)