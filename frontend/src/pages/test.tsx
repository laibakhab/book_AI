import React from 'react';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import Link from '@docusaurus/Link';

export default function TestPage(): JSX.Element {
  return (
    <Layout title="UI Test Page" description="Testing the futuristic UI components">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6">
            <div className="card">
              <div className="card__header">
                <h3>Test Card</h3>
              </div>
              <div className="card__body">
                <p>This is a test card to validate the styling and responsiveness.</p>
              </div>
              <div className="card__footer">
                <Link className="button button--secondary" to="/">Go Home</Link>
              </div>
            </div>
          </div>
          <div className="col col--6">
            <div className={clsx('card', 'hover-lift', 'hover-glow')}>
              <div className="card__header">
                <h3>Hover Effects Test</h3>
              </div>
              <div className="card__body">
                <p>Try hovering over this card to see the lift and glow effects.</p>
              </div>
            </div>
          </div>
        </div>

        <div className="margin-vert--lg">
          <h2>Typography Tests</h2>
          <h1>Heading 1</h1>
          <h2>Heading 2</h2>
          <h3>Heading 3</h3>
          <h4>Heading 4</h4>
          <h5>Heading 5</h5>
          <h6>Heading 6</h6>
          <p>This is a paragraph with <code>inline code</code> to test typography styling.</p>
        </div>

        <div className="margin-vert--lg">
          <h2>Button Tests</h2>
          <div className="button-group button-group--block">
            <Link className="button button--primary" to="/">Primary Button</Link>
            <Link className="button button--secondary" to="/">Secondary Button</Link>
            <Link className="button button--primary futuristic-glow" to="/">Glow Button</Link>
          </div>
        </div>

        <div className="margin-vert--lg">
          <h2>Animation Tests</h2>
          <div className="row">
            <div className="col col--3">
              <div className={clsx('card', 'float-element')}>
                <div className="card__body text--center">
                  <p>Float Animation</p>
                </div>
              </div>
            </div>
            <div className="col col--3">
              <div className={clsx('card', 'pulse-element')}>
                <div className="card__body text--center">
                  <p>Pulse Animation</p>
                </div>
              </div>
            </div>
            <div className="col col--3">
              <div className={clsx('card', 'slide-in-left')}>
                <div className="card__body text--center">
                  <p>Slide In Left</p>
                </div>
              </div>
            </div>
            <div className="col col--3">
              <div className={clsx('card', 'slide-in-right')}>
                <div className="card__body text--center">
                  <p>Slide In Right</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="margin-vert--lg">
          <h2>Code Block Test</h2>
          <pre><code>{`import numpy as np

def humanoid_control_loop():
    """Main control loop for humanoid robot."""
    while True:
        # Get sensor data
        imu_data = get_imu_data()
        joint_angles = get_joint_angles()

        # Calculate control commands
        commands = calculate_control_commands(imu_data, joint_angles)

        # Send commands to actuators
        send_commands(commands)

        # Wait for next cycle
        time.sleep(0.01)`}</code></pre>
        </div>

        <div className="margin-vert--lg">
          <h2>Admonition Tests</h2>
          <div className="alert alert--info">
            <p>This is an info alert.</p>
          </div>
          <div className="alert alert--note">
            <p>This is a note alert.</p>
          </div>
          <div className="alert alert--tip">
            <p>This is a tip alert.</p>
          </div>
          <div className="alert alert--caution">
            <p>This is a caution alert.</p>
          </div>
          <div className="alert alert--danger">
            <p>This is a danger alert.</p>
          </div>
        </div>

        <div className="margin-vert--lg">
          <h2>Table Test</h2>
          <table>
            <thead>
              <tr>
                <th>Component</th>
                <th>Status</th>
                <th>Version</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>ROS 2</td>
                <td>Active</td>
                <td>Galactic</td>
              </tr>
              <tr>
                <td>Gazebo</td>
                <td>Active</td>
                <td>11.5.0</td>
              </tr>
              <tr>
                <td>MoveIt</td>
                <td>Inactive</td>
                <td>2.3.2</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  );
}