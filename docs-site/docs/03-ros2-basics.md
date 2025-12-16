---
title: ROS 2 — The Robotic Nervous System
---

## Overview
ROS 2 provides communication, synchronization, and control for robotic systems.

## Core Concepts
- Nodes
- Topics
- Services
- Actions

## Python Control with rclpy
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Brain(Node):
    def __init__(self):
        super().__init__('brain')
        self.pub = self.create_publisher(String, 'command', 10)

rclpy.init()
node = Brain()
rclpy.spin(node)

