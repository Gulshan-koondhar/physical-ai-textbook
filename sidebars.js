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
        'module-1-ros/ros2-from-zero'
        // Additional chapters will be added as they are created
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