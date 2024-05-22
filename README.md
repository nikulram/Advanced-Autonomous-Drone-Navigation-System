# Advanced Autonomous Drone Navigation System (AADNS) by Nikul Ram

## Overview
The Advanced Autonomous Drone Navigation System (AADNS) is a sophisticated initiative leveraging cutting-edge technologies in AI, machine learning, and simulation to develop highly advanced autonomous drone capabilities. Designed for complex environmental interactions and adaptive flight path management, it aims to push the boundaries of what autonomous drones can achieve in realistic and simulated settings.

## Features
- **Real-Time Obstacle Detection**: Utilizes advanced sensors and AI to dynamically detect and avoid obstacles.
- **Environmental Interaction**: Engages with simulated environments to test response scenarios and improve navigational tactics.
- **Adaptive Flight Path Management**: Algorithms dynamically adjust the drone's flight path based on real-time data.
- **Simulation Integration**: Compatible with AirSim and Gazebo for high-fidelity simulation and testing.
- **Safety and Emergency Protocols**: Robust mechanisms to handle emergency scenarios effectively.


## Planned Enhancements
I am continuously working to improve the system's capabilities. Future enhancements include the integration of advanced pathfinding algorithms such as A* and Dijkstra’s. These enhancements will be integrated into the project's `navigation.py` file and will provide more efficient and optimized pathfinding solutions.

**Note:** For detailed information on future enhancements and the planned implementation of A* and Dijkstra's algorithms, please refer to the `Future_Enhancements.md` file in the `docs` folder. This will give the users an idea on how the, "example usage" can look like.

**Future Enhancements updates will be posted in `Future_Enhancements.md` file in the `docs` folder.** 

## Installation
Ensure you have the following prerequisites installed:
- Python 3.8 or later
- Unreal Engine
- AirSim or Gazebo

Clone the repository:
git clone https://github.com/nikulram/Advanced-Autonomous-Drone-Navigation-System.git

cd Advanced-Autonomous-Drone-Navigation-System
pip install -r requirements.txt

## Usage
To start the simulation environment:
python main.py

Replace main.py with the script configured to launch your simulation environment, tailored to your specific setup in either AirSim or Gazebo.

## Testing
All testing files are located within the same directory as their corresponding modules. To run tests, navigate to the file directory and execute:

python test_module_name.py

Ensure that your testing environment is configured to mimic the operational conditions expected during the simulation.

## Contributing
Interested in contributing? Great! Please follow the next steps:

Fork the repository.
Create your feature branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a Pull Request.

## Documentation
For a detailed explanation of the project's architecture, development phases, and more, see the Advanced Autonomous Drone Navigation System [Documentation](docs/Advanced_Autonomous_Drone_Navigation_System_Documentation_v1.0.pdf) located in the docs folder.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
AirSim and Unreal Engine for simulation capabilities.
Python and its vast ecosystem for backend development.
The contributors and maintainers of all used open-source software.
Special thanks to Hamna Khalid for giving valuable tips and guidance on enhancing the documentation(Advanced_Autonomous_Drone_Navigation_System_Documentation_v1.0) part of this project.   

## References
"Flying Free: A Research Overview of Deep Learning in Drone Navigation," available at MDPI.
"Artificial Intelligence Approaches for UAV Navigation: Recent Advances," available at IEEE Xplore.
"Drone Navigation and Target Interception Using Deep Reinforcement Learning," available at IEEE Xplore.
"Vision-Based Navigation Techniques for Drones," available at MDPI.
"Integration of Weather Data into UAV Decision Making," available at AMETSOC.
"Enhancements in GPS Technology for UAV Navigation and Positioning," available at Springer.
"Simulation of UAV Systems Using Gazebo," available at ScienceDirect.
"AirSim: High-Fidelity Visual and Physical Simulation for Autonomous Vehicles," available at ArXiv.
Mark Rober's "Vortex Cannon vs Drone," available on YouTube.