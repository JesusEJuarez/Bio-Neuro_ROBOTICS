# Bio and Neuro Robotics Projects

This repository contains Python and Matlab projects in the fields of bio and neuro robotics. 

## Bio-Robotics Projects

- [Bio-Robotics Project 1](bio_robotics/project1.py)
- [Bio-Robotics Project 2](bio_robotics/project2.py)
- [Bio-Robotics Project 3](bio_robotics/project3.m)

## Neuro-Robotics Projects
### Path planing
The path planning of a robot is an important aspect because for two given points A and B in space, the robot can reach them through different paths. However, some of these paths may be too complex, time-consuming, or the robot may not be able to traverse certain paths due to its geometry. Hence, it is important to explore methods that allow generating routes as efficiently as possible and ensure that the robot is capable of executing them.
In this section, you will find some path planning algorithms for a 3-degree-of-freedom robot. The workspace for each algorithm could be changed.
- [Random Path Generator](neuro_robotics/RPG.py) :
This Python script implements an Ant Colony Optimization (ACO) algorithm for path planning in a 3-dimensional workspace for a robotic system with three degrees of freedom. The script generates a set of feasible points within the workspace and connects them to form branches, avoiding obstacles defined in the space. The ACO algorithm then optimizes the path between a specified start and end point, considering factors such as pheromone levels and visibility. The optimized path is plotted in a 3D graph and saved to a CSV file for further analysis or execution by the robotic system.  
- [Potential fields](neuro_robotics/projectB.m)
- [Random Walk](neuro_robotics/projectC.py)
