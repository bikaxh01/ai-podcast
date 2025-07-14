import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const data = {
  metaData: {
    description:
      "A comprehensive guide to Kafka for beginners, covering its core concepts, architecture, and use cases.",
    title: "Understanding Apache Kafka for Beginners",
  },
  scenesData: [
    {
      animationTypes: ["Write", "FadeIn"],
      colorScheme: {
        background: "#1E1E1E",
        highlights: "#FFD700",
        text: "#FFFFFF",
      },
      instruction:
        "Display the title 'Apache Kafka: A Beginner's Guide' prominently in the center of the screen. Fade in the subtitle 'Understanding the Fundamentals'. The background is a dark, professional gray.",
      sceneTitle: "Introduction to Kafka",
      sequence: 1,
      visualElements: [
        "Title: Apache Kafka: A Beginner's Guide",
        "Subtitle: Understanding the Fundamentals",
      ],
    },
    {
      animationTypes: ["Write", "Create", "Arrow"],
      colorScheme: {
        background: "#1E1E1E",
        highlights: "#00CED1",
        text: "#FFFFFF",
      },
      instruction:
        "Introduce the problem Kafka solves: traditional messaging systems being slow and complex. Show a simple diagram with a Producer sending a message to a Consumer, but illustrate it as a slow, direct, point-to-point connection with a bottleneck. Use arrows to show data flow.",
      sceneTitle: "The Problem: Traditional Messaging",
      sequence: 2,
      visualElements: [
        "Text: Traditional Messaging",
        "Diagram: Producer -> Consumer (Point-to-Point)",
        "Arrow: Slow Data Transfer",
        "Text: Bottlenecks & Complexity",
      ],
    },
    {
      animationTypes: ["Write", "Create", "Transform", "FadeIn"],
      colorScheme: {
        background: "#1E1E1E",
        highlights: "#32CD32",
        text: "#FFFFFF",
      },
      instruction:
        "Introduce Kafka as the solution. Show a central Kafka cluster acting as a message broker. Producers send messages to Kafka, and Consumers read from Kafka. Use distinct icons for Producers, Kafka Cluster, and Consumers. Show data flowing from Producers to Kafka, and then from Kafka to Consumers.",
      sceneTitle: "Introducing Kafka: The Solution",
      sequence: 3,
      visualElements: [
        "Text: Apache Kafka",
        "Icon: Producer",
        "Icon: Kafka Cluster",
        "Icon: Consumer",
        "Arrows: Producer -> Kafka, Kafka -> Consumer",
        "Text: High Throughput, Scalable, Fault-Tolerant",
      ],
    },
    {
      animationTypes: ["Write", "Create"],
      colorScheme: {
        background: "#1E1E1E",
        highlights: "#FF4500",
        text: "#FFFFFF",
      },
      instruction:
        "Explain the core concepts: Topics, Producers, Consumers, and Brokers. Show a 'Topic' as a category or feed name. Producers write to Topics. Consumers read from Topics. Brokers are servers that form the Kafka cluster. Use text labels and simple shapes.",
      sceneTitle: "Core Concepts: Topics, Producers, Consumers, Brokers",
      sequence: 4,
      visualElements: [
        "Text: Topic (e.g., 'user_signups')",
        "Label: Producer",
        "Label: Consumer",
        "Label: Broker (Server)",
        "Diagram: Producer -> Topic <- Consumer",
        "Text: Brokers form the cluster",
      ],
    },
    {
      animationTypes: ["Write", "Create", "Transform"],
      colorScheme: {
        background: "#1E1E1E",
        highlights: "#DA70D6",
        text: "#FFFFFF",
      },
      instruction:
        "Explain Partitions. Show a Topic visually divided into ordered, immutable sequences called Partitions. Illustrate messages (like numbered records) within each partition. Emphasize that partitions allow parallel processing and scalability. Show a Topic with multiple partitions (e.g., Partition 0, Partition 1).",
      sceneTitle: "Core Concepts: Partitions",
      sequence: 5,
      visualElements: [
        "Text: Partitions",
        "Diagram: Topic divided into partitions (e.g., 2 partitions)",
        "Visual Representation: Ordered messages within each partition",
        "Text: Scalability & Parallelism",
      ],
    },
    {
      animationTypes: ["Write", "Create", "Transform"],
      colorScheme: {
        background: "#1E1E1E",
        highlights: "#4682B4",
        text: "#FFFFFF",
      },
      instruction:
        "Explain Consumers and Consumer Groups. Show multiple Consumers reading from the same Topic but belonging to different Consumer Groups. Demonstrate how each group gets a full copy of the messages, but within a group, each consumer reads from different partitions to avoid duplicate processing.",
      sceneTitle: "Core Concepts: Consumers & Consumer Groups",
      sequence: 6,
      visualElements: [
        "Text: Consumer Groups",
        "Diagram: Topic with partitions",
        "Icon: Consumer Group A (multiple consumers reading different partitions)",
        "Icon: Consumer Group B (multiple consumers reading different partitions)",
        "Text: Each group gets messages, within a group, partitions are distributed.",
      ],
    },
    {
      animationTypes: ["Write", "Create", "Transform", "Flash"],
      colorScheme: {
        background: "#1E1E1E",
        highlights: "#FFA07A",
        text: "#FFFFFF",
      },
      instruction:
        "Explain the Kafka Architecture: ZooKeeper and Brokers. Show ZooKeeper as the cluster coordinator, managing Broker states. Then show multiple Brokers forming the Kafka cluster, each holding partitions of Topics. Illustrate the data flow and coordination.",
      sceneTitle: "Kafka Architecture: ZooKeeper & Brokers",
      sequence: 7,
      visualElements: [
        "Text: Kafka Architecture",
        "Icon: ZooKeeper (Coordinator)",
        "Multiple Icons: Brokers (Servers)",
        "Diagram: ZooKeeper managing Brokers",
        "Diagram: Topics distributed across Brokers",
        "Arrow: Producers/Consumers interact with Brokers",
      ],
    },
    {
      animationTypes: ["Write", "Create"],
      colorScheme: {
        background: "#1E1E1E",
        highlights: "#9370DB",
        text: "#FFFFFF",
      },
      instruction:
        "Describe Key Use Cases for Kafka. Display common applications like Real-time Analytics, Log Aggregation, Stream Processing, and Event Sourcing. Use icons or simple text representations for each use case.",
      sceneTitle: "Kafka Use Cases",
      sequence: 8,
      visualElements: [
        "Text: Use Cases",
        "Icon/Text: Real-time Analytics",
        "Icon/Text: Log Aggregation",
        "Icon/Text: Stream Processing (e.g., Kafka Streams)",
        "Icon/Text: Event Sourcing",
      ],
    },
    {
      animationTypes: ["Write", "FadeOut"],
      colorScheme: {
        background: "#1E1E1E",
        highlights: "#FFD700",
        text: "#FFFFFF",
      },
      instruction:
        "Conclude the introduction. Display a summary message like 'Kafka: Powerful for building real-time data pipelines.' Fade out all elements, leaving a clean screen.",
      sceneTitle: "Conclusion",
      sequence: 9,
      visualElements: [
        "Text: Kafka: Powerful for real-time data pipelines.",
        "Text: Further learning resources available.",
      ],
    },
  ],
};
