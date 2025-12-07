# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Prerequisites

Before starting with this textbook, ensure you have:

### Hardware Requirements
- **RTX Workstation**: NVIDIA RTX graphics card (RTX 3080 or better recommended) for AI model training and simulation
- **Jetson Kit**: Jetson Orin for real hardware deployment
- **Internet Access**: For downloading dependencies and AI models

### Software Requirements
- **Operating System**: Ubuntu 22.04 LTS
- **Docker**: For containerized environments (optional but recommended)
- **Git**: For version control and repository management
- **Python 3.10+**: For ROS 2 and AI components

### Account Requirements
- GitHub account for accessing the textbook repository
- NVIDIA Developer account (for Isaac Sim access)

## Setup Process

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/physical-ai-textbook.git
cd physical-ai-textbook
```

### 2. Install Dependencies
```bash
# Install system dependencies
sudo apt update
sudo apt install python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### 3. Install ROS 2 Humble
Follow the official ROS 2 Humble installation guide:
```bash
# Add ROS 2 repository
sudo apt update && sudo apt install -y curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 packages
sudo apt update
sudo apt install ros-humble-desktop ros-humble-ros-base
sudo apt install ros-dev-tools
```

### 4. Install Docusaurus
```bash
npm install
```

## Running the Textbook Locally

### 1. Start the Docusaurus Development Server
```bash
npm start
```
This will start a local server at `http://localhost:3000` where you can view the textbook.

### 2. Navigate to Your First Chapter
Open your browser and go to:
```
http://localhost:3000/docs/intro/01-introduction-to-physical-ai
```

## First Exercise: Basic ROS 2 Node

Try the first interactive example in Chapter 1.2:

1. Create a new ROS 2 workspace:
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

2. Run the example code provided in the textbook (the interactive code block will execute directly in your environment if properly configured).

## Next Steps

1. Complete the setup verification exercises in Chapter 1
2. Proceed to Chapter 1.2 to begin with ROS 2 fundamentals
3. Follow the sequential path through all four modules
4. Complete the capstone project in Chapter 15

## Troubleshooting

### Common Issues

- **"command not found" errors**: Ensure you've sourced the ROS 2 setup file (`source /opt/ros/humble/setup.bash`)
- **Python package errors**: Make sure you're using Python 3.10+ and have activated your virtual environment
- **GPU/CUDA issues**: Verify your NVIDIA drivers are properly installed and compatible with Isaac Sim

### Getting Help

- Check the Troubleshooting Appendix in the textbook
- Review common errors in Appendix A
- Visit the GitHub repository issues for community support