# Data Model: Physical AI & Humanoid Robotics Textbook

## Entity: Learning Path
- **Description**: Structured sequence of chapters that progresses from basic ROS 2 concepts to advanced conversational robotics
- **Attributes**:
  - id: unique identifier for the learning path
  - title: descriptive name of the path
  - duration: estimated time to complete (in weeks)
  - prerequisites: list of required knowledge areas
  - modules: ordered list of modules in the path
- **Validation**: Must have 4 modules as specified, duration must be 13 weeks
- **Relationships**: Contains multiple chapters, associated with target audience

## Entity: Chapter
- **Description**: Individual section of the textbook covering specific topics
- **Attributes**:
  - id: unique identifier for the chapter
  - title: descriptive title of the chapter
  - module: which module the chapter belongs to
  - number: sequential number within the module
  - word_count: actual word count (35,000-55,000 total)
  - readability_score: Flesch-Kincaid grade level (10-14)
  - content_type: MDX format required
  - interactive_elements: count of executable code blocks
- **Validation**: Must maintain readability between grades 10-14, must be in MDX format
- **Relationships**: Belongs to one learning path, contains multiple content sections

## Entity: Humanoid Robot Model
- **Description**: 20+ DoF robot representation in URDF/Xacro format with joint constraints and sensor configurations
- **Attributes**:
  - id: unique identifier for the robot model
  - name: descriptive name of the robot
  - degrees_of_freedom: number of joints (minimum 20)
  - urdf_path: file path to URDF description
  - xacro_path: file path to Xacro description
  - sensors: list of sensor configurations (LiDAR, RealSense, IMU, force/torque)
  - joint_constraints: limits and properties for each joint
- **Validation**: Must have 20+ degrees of freedom as specified
- **Relationships**: Used in simulation environments, referenced in multiple chapters

## Entity: Simulation Environment
- **Description**: Physics-based world with sensor plugins and dynamic objects for testing robot behaviors
- **Attributes**:
  - id: unique identifier for the environment
  - name: descriptive name of the environment
  - physics_engine: Gazebo Harmonic or other simulation platform
  - objects: list of static and dynamic objects in the environment
  - sensor_plugins: configurations for various sensors
  - lighting_conditions: environmental lighting settings
- **Validation**: Must support required sensor plugins as specified
- **Relationships**: Contains humanoid robot models, used for testing robot behaviors

## Entity: AI Pipeline
- **Description**: Integrated system connecting speech recognition, language processing, computer vision, and motion planning components
- **Attributes**:
  - id: unique identifier for the pipeline
  - name: descriptive name of the pipeline
  - speech_recognition: model used (Whisper)
  - language_model: model used (GPT-4o/Llama-3-70B)
  - vision_model: model used (Grounding DINO + SAM)
  - motion_planner: ROS 2 actionlib sequence
  - input_format: accepted input types (voice commands)
  - output_format: generated output types (motion commands)
- **Validation**: Must support end-to-end voice-to-action pipeline
- **Relationships**: Processes user commands, generates robot actions

## Entity: Deployment Configuration
- **Description**: Settings and parameters for both simulated and real hardware execution
- **Attributes**:
  - id: unique identifier for the configuration
  - name: descriptive name of the configuration
  - platform: simulation or real hardware
  - target_hardware: RTX workstation, Jetson Orin, etc.
  - parameters: specific settings for the deployment
  - optimization: TensorRT settings for deployment
  - latency_requirements: performance constraints
- **Validation**: Must support both simulation and real hardware as specified
- **Relationships**: Associated with AI pipeline, humanoid robot model