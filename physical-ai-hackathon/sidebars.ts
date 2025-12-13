import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar for the textbook
  textbookSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Chapter 1: Physical AI',
      items: [
        'physical-ai/introduction',
      ],
      link: {
        type: 'doc',
        id: 'physical-ai/introduction',
      },
    },
    {
      type: 'category',
      label: 'Chapter 2: Humanoid Robotics',
      items: [
        'humanoid-robotics/overview',
      ],
      link: {
        type: 'doc',
        id: 'humanoid-robotics/overview',
      },
    },
    {
      type: 'category',
      label: 'Chapter 3: ROS 2',
      items: [
        'ros-2/getting-started',
      ],
      link: {
        type: 'doc',
        id: 'ros-2/getting-started',
      },
    },
    {
      type: 'category',
      label: 'Chapter 4: Simulation',
      items: [
        'simulation/gazebo-simulation',
      ],
      link: {
        type: 'doc',
        id: 'simulation/gazebo-simulation',
      },
    },
    {
      type: 'category',
      label: 'Chapter 5: Vision-Language-Action (VLA)',
      items: [
        'vision-language-action/introduction-vla',
      ],
      link: {
        type: 'doc',
        id: 'vision-language-action/introduction-vla',
      },
    },
    {
      type: 'category',
      label: 'Chapter 6: Capstone Project',
      items: [
        'capstone-project/project-overview',
      ],
      link: {
        type: 'doc',
        id: 'capstone-project/project-overview',
      },
    },
  ],
};

export default sidebars;
