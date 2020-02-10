# luigi_with_kubernetes_summary
Shows how luigi can be used with kubernetes

## ToDo:
0. Current Tasks
   1. Add kubernetes parameter to setup
   2. Welche Parameter benötigt Luigi von Kubernetes?
   3. Use Case und Dataset beschreiben?
   4. Kubernetes zum Laufen bringen (Mini-Cube Example)
   5. Edge detection Beispiel in Luigi Tasks bringen: Task 1
   6. Edge detection Beispiel in Luigi Tasks bringen: Task 2
   7. Kubernetes und Luigi verbinden
       1. Wie?
       2. Kubernetes und Luigi verbinden – Umsetzung
       3. Vorteile (wenn über mehrere Nodes)  dann Luigi-Worker in versch. Nodes
       4. Kubernetes: Abläufe der Tasks - Visualisierung
   8. Abschlusspräsentation
   9. Readme:
       1. Prior knowledge

1. Setup 
    1. Kubernetes
    2. Virtual environment and dependencies
    3. Luigi
    4. Dataset

2. Luigi Basics
    1. Basic Concepts
    2. Basic Example (What is Luigi and how does it work)
  
3. Luigi and Kubernetes
    1. Functionality (Concept + Pipeline)
    2. Result: How does Luigi interact with Kubernetes (components; e.g.: Tasks to pods.)
    3. How to get data to the tasks (pods)
    4. Scaling

4. Use Cases
    1. Batch-Processing Pipeline - Implementation (+ Image of a pipeline)
    2. Stream-Processing Pipeline - Implementation (+ Image of a pipeline)

## Guidelines
- Codestyle --> Pep: https://www.python.org/dev/peps/
- Docstrings and Type Hinting 
- Documentation in Readme  
