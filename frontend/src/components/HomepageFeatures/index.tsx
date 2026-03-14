import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Comprehensive Coverage',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Six in-depth chapters covering Physical AI, Humanoid Robotics, ROS 2,
        Simulation, Vision-Language-Action systems, and a Capstone Project.
      </>
    ),
  },
  {
    title: 'AI-Powered Assistance',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Get instant answers to your questions with our RAG-powered AI assistant
        trained on the entire textbook content.
      </>
    ),
  },
  {
    title: 'Practical Learning',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Each chapter includes theoretical foundations, practical examples,
        and hands-on exercises to reinforce your learning.
      </>
    ),
  },
  {
    title: 'Cutting-Edge Topics',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Explore the latest advancements in robotics and embodied AI with
        real-world applications and research insights.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--3')}>
      <div className={clsx('card', styles.featureCard)}>
        <div className="card__header">
          <div className={clsx('text--center', styles.iconContainer)}>
            <Svg className={styles.featureSvg} role="img" />
          </div>
          <Heading as="h3" className={styles.cardTitle}>{title}</Heading>
        </div>
        <div className="card__body">
          <p className={styles.cardDescription}>{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={clsx(styles.features, 'fade-in-up')}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
