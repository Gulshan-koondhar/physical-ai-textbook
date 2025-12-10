// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro/introduction-to-physical-ai'],
    },
    {
      type: 'category',
      label: 'Module 1 - ROS 2 Fundamentals',
      items: [
        'module-1-ros/ros2-from-zero',
        'module-1-ros/urdf-xacro-mastery',
        'module-1-ros/nodes-topics-services',
        'module-1-ros/rviz-configuration',
        'module-1-ros/ros2-bag-foxglove',
        'module-1-ros/interactive-examples'
      ],
    },
    {
      type: 'category',
      label: 'Module 2 - Simulation',
      items: [
        'module-2-simulation/gazebo-harmonic-setup',
        'module-2-simulation/simulating-humanoid',
        'module-2-simulation/unity-rendering',
        'module-2-simulation/sensor-plugin-configuration',
        'module-2-simulation/sensor-configurations',
        'module-2-simulation/ros-tcp-connector'
      ],
    },
    {
      type: 'category',
      label: 'Module 3 - AI Brain',
      items: [
        'module-3-ai-brain/isaac-sim-installation',
        'module-3-ai-brain/isaac-ros-gems',
        'module-3-ai-brain/nav2-moveit2',
        'module-3-ai-brain/synthetic-data'
      ],
    },
    {
      type: 'category',
      label: 'Module 4 - VLA Integration',
      items: [
        'module-4-vla/whisper-gpt-ros-planner',
        'module-4-vla/open-vocabulary-detection',
        'module-4-vla/end-to-end-pipeline',
        'module-4-vla/jetson-deployment',
        'module-4-vla/ai-integration-examples',
        'module-4-vla/tensorrt-optimization'
      ],
    },
    {
      type: 'category',
      label: 'Capstone Project',
      items: ['capstone/red-cup-project'],
    },
    {
      type: 'category',
      label: 'Hardware Guide',
      items: ['hardware/hardware-guide'],
    },
    {
      type: 'category',
      label: 'Appendices',
      items: [
        'appendix/troubleshooting',
        'appendix/urdf-repository'
      ],
    }
  ],
};

module.exports = sidebars;