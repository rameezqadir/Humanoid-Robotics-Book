---
title: Vision-Language-Action (VLA)
---

## From Language to Motion

VLA systems convert natural language into robotic actions.

## Pipeline
1. Speech → Whisper
2. Text → LLM planner
3. Plan → ROS actions

## Example
Command:
“Pick up the bottle from the table”

Converted into:
- Navigate
- Detect object
- Manipulate
