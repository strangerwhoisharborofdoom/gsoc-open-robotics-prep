<div align="center">

![GSoC 2026](https://img.shields.io/badge/GSoC-2026-ff69b4?style=for-the-badge&logo=google&logoColor=white)
![Open Robotics](https://img.shields.io/badge/Open%20Robotics-ROS%202-blue?style=for-the-badge&logo=ros&logoColor=white)
![Gazebo](https://img.shields.io/badge/Gazebo-Simulation-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![CI](https://github.com/strangerwhoisharborofdoom/gsoc-2026-proposal/actions/workflows/ci.yml/badge.svg)

</div>

# Automated Benchmarking for ROS2 Systems

> **GSoC 2026 Proposal** | Open Robotics Mentorship  
> Building standardized, automated performance benchmarking tools for distributed ROS2 systems

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![ROS2](https://img.shields.io/badge/ROS2-Humble%2FJazzy%2FRolling-blue)](https://docs.ros.org/)
[![Language](https://img.shields.io/badge/Languages-C%2B%2B%20%7C%20Python%20%7C%20YAML-orange)]()

---

## What This Project Solves

ROS2 developers lack a **standardized, automated, and reproducible** benchmarking framework for evaluating distributed node performance. While several tools exist, none provide a unified solution that combines:

- **Automated test execution** across multiple ROS2 distributions
- **Cross-RMW comparison** (CycloneDDS, FastDDS, Connext)
- **Real-time monitoring** with minimal instrumentation overhead
- **Actionable performance reports** with bottleneck identification
- **CI/CD integration** for regression detection

This project builds on [REP 2014](https://ros.org/reps/rep-2014.html) guidelines to deliver a production-ready benchmarking suite for the ROS2 ecosystem.

## The Unsolved Problem in ROS2 Benchmarking

Despite significant progress, ROS2 still lacks a **unified benchmarking standard**. Here is what existing tools miss:

| Gap | Why It Matters |
|-----|---------------|
| **Fragmented tooling** | `ros2_tracing` traces but does not benchmark; `performance_test` simulates synthetic graphs but requires code modification; `ros2_benchmark` (NVIDIA) is tied to Isaac ROS workflows |
| **No cross-RMW benchmarks** | Developers cannot easily compare CycloneDDS vs FastDDS vs Connext on the same workload |
| **Manual baseline comparison** | No tool automatically flags performance regressions across ROS2 versions or configuration changes |
| **Missing distributed benchmarks** | Existing tools focus on single-machine performance, not multi-node, multi-host scenarios |
| **No standardized workload suite** | Every project defines its own benchmarks, making cross-project comparison impossible |
| **Limited real-time analysis** | Tracing data requires offline post-processing; no real-time dashboard for live ROS2 systems |
| **Poor CI/CD integration** | Benchmark results are not easily consumable in GitHub Actions or similar pipelines |

This project directly addresses these gaps by building a **unified, extensible benchmarking framework** that integrates tracing, synthetic workloads, and real-time monitoring into a single toolchain.

## Existing Tools Comparison

### Tool Landscape Overview

| Tool | Maintainer | Primary Focus | Strengths | Limitations |
|------|------------|---------------|-----------|-------------|
| **[ros2_tracing](https://github.com/ros2/ros2_tracing)** | Open Robotics | Tracing & profiling | Low-overhead LTTng-based tracing; probes in ROS2 core; cross-platform | Trace-only, no benchmarking logic; requires offline analysis; no standardized metrics |
| **[performance_test](https://github.com/irobot-ros/ros2-performance)** | iRobot / Apex.AI | Synthetic workload simulation | JSON-defined topologies; measures latency, reliability, CPU, memory | Requires code modification; C++ only; limited to synthetic graphs; not actively maintained |
| **[ros2_benchmark](https://github.com/NVIDIA-ISAAC-ROS/ros2_benchmark)** | NVIDIA | Isaac ROS graph benchmarking | Non-intrusive; measures throughput, latency, compute; CI/CD ready | Tied to NVIDIA/Isaac ecosystem; requires rosbag inputs; limited to specific message types |
| **[performance_test_fixture](https://github.com/ros2/performance_test_fixture)** | Open Robotics | Unit-level benchmarking | Google Benchmark integration; memory allocation stats; CMake automation | Only for micro-benchmarks of ROS2 APIs; not for full system evaluation |
| **[ros2_framework_perf](https://discourse.openrobotics.org/t/ros-2-performance-benchmarking/44382)** | Open Robotics (internal) | Core framework profiling | Uses `perf` for profiling; identifies memory and executor bottlenecks | Internal tool; not publicly available; requires `perf` expertise |
| **This Project** | Open Robotics (proposed) | **Unified benchmarking suite** | Combines tracing + synthetic workloads + real-time monitoring + cross-RMW + CI/CD | New project; requires adoption by community |

### How This Project Complements Existing Tools

- **`ros2_tracing`**: Uses it as the **underlying tracing backend** for low-overhead data collection
- **`performance_test`**: Learns from its JSON topology approach but makes it **non-intrusive** (no code changes)
- **`ros2_benchmark`**: Adopts its **playback + monitor architecture** but makes it **distribution-agnostic** (not NVIDIA-specific)
- **`performance_test_fixture`**: Integrates its **memory measurement tools** for fine-grained allocation tracking

## System Architecture

```
+------------------------------------------------------------------+
|                      ROS2 BENCHMARK SUITE                        |
+------------------------------------------------------------------+
|                                                                  |
|  +------------------+    +------------------+    +------------+  |
|  |  Benchmark CLI   |    |  Web Dashboard   |    | CI/CD CLI  |  |
|  |  (Python)        |    |  (Flask + JS)    |    | (Python)   |  |
|  +--------+---------+    +--------+---------+    +-----+------+  |
|           |                       |                      |       |
|           +-----------+-----------+----------------------+       |
|                       |                                          |
|           +-----------v-----------+                              |
|           |   Benchmark Controller  (Python)                     |
|           |   - Orchestrates test execution                      |
|           |   - Manages Docker containers                        |
|           |   - Aggregates results                               |
|           +-----------+-----------+                              |
|                       |                                          |
|         +-------------+-------------+                            |
|         |                           |                            |
|  +------v------+             +------v------+                     |
|  |  Workload   |             |  Workload   |                     |
|  |  Generator  |             |  Generator  |                     |
|  |  (C++)      |             |  (Python)   |                     |
|  |  - Latency  |             |  - Throughput|                    |
|  |  - Jitter   |             |  - Load test |                    |
|  |  - Scalability           |  - QoS test  |                     |
|  +------+------+             +------+------+                     |
|         |                           |                            |
|         +-------------+-------------+                            |
|                       |                                          |
|           +-----------v-----------+                              |
|           |   ROS2 Test Graph      (Nodes in Docker)            |
|           |   - Configurable topology (YAML)                     |
|           |   - Multi-RMW support                                |
|           |   - Multi-host capable                               |
|           +-----------+-----------+                              |
|                       |                                          |
|           +-----------v-----------+                              |
|           |   ros2_tracing       (LTTng backend)                |
|           |   - Low-overhead tracing                             |
|           |   - Kernel + user-space events                       |
|           +-----------+-----------+                              |
|                       |                                          |
|           +-----------v-----------+                              |
|           |   Metrics Aggregator  (Python)                       |
|           |   - Real-time statistics                             |
|           |   - Bottleneck detection                             |
|           |   - Report generation (JSON, HTML, Markdown)         |
|           +----------------------+                               |
|                                                                  |
+------------------------------------------------------------------+
```

### Component Details

| Component | Language | Technology | Responsibility |
|-----------|----------|------------|----------------|
| **CLI** | Python | Click, Rich | User-facing commands for running benchmarks |
| **Benchmark Controller** | Python | Asyncio, Docker SDK | Orchestrates test execution and container lifecycle |
| **Workload Generator (C++)** | C++17 | rclcpp, std::chrono | High-precision latency and jitter measurement |
| **Workload Generator (Python)** | Python | rclpy, asyncio | Throughput and scalability testing |
| **Web Dashboard** | Python + JS | Flask, Chart.js, WebSocket | Real-time visualization of benchmark results |
| **Metrics Aggregator** | Python | Pandas, NumPy | Statistical analysis and bottleneck detection |
| **CI/CD CLI** | Python | GitHub Actions API | Regression detection and trend analysis |
| **Configuration** | YAML | pyyaml | Test topology, workload parameters, thresholds |

## How This Helps ROS2 Developers

| Developer Need | How This Project Helps |
|----------------|------------------------|
| **Choosing an RMW** | Run the same benchmark against CycloneDDS, FastDDS, and Connext to pick the best for your use case |
| **Optimizing a graph** | Identify which node or topic is the bottleneck before rewriting code |
| **Validating hardware** | Benchmark on Jetson, Raspberry Pi, x86 to ensure your hardware meets requirements |
| **Regression testing** | Integrate benchmarks in CI/CD to catch performance degradation on every commit |
| **Comparing ROS2 versions** | Run identical benchmarks on Humble, Iron, Jazzy, and Rolling to evaluate upgrades |
| **QoS tuning** | Test different QoS policies (reliability, durability, history) for optimal performance |
| **Real-time validation** | Verify that your system meets timing requirements with statistical confidence |
| **Documentation for stakeholders** | Generate professional HTML/Markdown reports to show performance characteristics to management |

## Planned Contributions to the Open Robotics Ecosystem

This project is designed to contribute back to the broader ROS2 community:

### 1. Upstream Contributions

| Contribution | Target Repository | Description |
|--------------|------------------|-------------|
| **Standard benchmark workload definitions** | `ros2/demos` | Common benchmark topologies (chain, star, ring) usable by all ROS2 developers |
| **Cross-RMW benchmark scripts** | `ros2/rmw` | Automated comparison scripts for DDS implementations |
| **CI/CD benchmark action** | `ros2/ros2` | GitHub Action for running performance benchmarks on PRs |
| **Documentation improvements** | `ros2/docs.ros.org` | Benchmarking best practices guide based on REP 2014 |

### 2. New Open-Source Packages

| Package | Description | License |
|---------|-------------|--------|
| **ros2_benchmark_suite** | Core benchmarking framework with CLI | Apache 2.0 |
| **ros2_benchmark_workloads** | Pre-defined workload definitions (YAML) | Apache 2.0 |
| **ros2_benchmark_dashboard** | Web-based real-time monitoring dashboard | Apache 2.0 |
| **ros2_benchmark_ci** | GitHub Actions integration for regression detection | Apache 2.0 |

### 3. Community Engagement

- Present findings at **ROSCon 2026**
- Publish **benchmark comparison results** across ROS2 distributions
- Create a **public benchmark leaderboard** for ROS2 middleware performance
- Mentor **future contributors** to continue the project post-GSoC

## 12-Week Implementation Plan

### Phase 1: Foundation (Weeks 1-3)

| Week | Tasks | Deliverables |
|------|-------|-------------|
| **1** | Environment setup; study `ros2_tracing` internals; design YAML schema | Dev environment, design doc |
| **2** | Implement basic C++ workload generator (publisher/subscriber) | `benchmark_core` prototype |
| **3** | Implement Python workload generator; integrate with `ros2_tracing` | Working prototype with tracing |

### Phase 2: Core Features (Weeks 4-7)

| Week | Tasks | Deliverables |
|------|-------|-------------|
| **4** | Build Benchmark Controller with Docker orchestration | `benchmark_controller` module |
| **5** | Implement metrics aggregator with latency, throughput, jitter stats | Statistics engine |
| **6** | Add cross-RMW benchmark support (CycloneDDS, FastDDS) | Multi-RMW test runner |
| **7** | Build CLI interface with Click; add YAML configuration parser | Functional CLI tool |

### Phase 3: Visualization & Reporting (Weeks 8-10)

| Week | Tasks | Deliverables |
|------|-------|-------------|
| **8** | Develop Flask-based web dashboard with real-time charts | Web dashboard MVP |
| **9** | Implement report generators (JSON, HTML, Markdown) | Report generation module |
| **10** | Add bottleneck detection algorithms; integrate with CI/CD | Smart analysis features |

### Phase 4: Polish & Integration (Weeks 11-12)

| Week | Tasks | Deliverables |
|------|-------|-------------|
| **11** | Integration testing across ROS2 distributions; bug fixes | Stable release candidate |
| **12** | Documentation, GitHub Actions integration, final polish | Production-ready release |

## Quick Start (Planned)

```bash
# Clone the repository
git clone https://github.com/strangerwhoisharborofdoom/ros2_benchmark_suite.git
cd ros2_benchmark_suite

# Install dependencies
pip install -r requirements.txt

# Run a basic latency benchmark
ros2-benchmark run \
  --workload latency_chain \
  --nodes 5 \
  --duration 60 \
  --rmw cyclonedds \
  --output report.html

# Compare RMWs
ros2-benchmark compare \
  --workload throughput_star \
  --rmws cyclonedds,fastrtps,connext \
  --output comparison.md
```

## Getting Involved

This is a **GSoC 2026 proposal repository**. The actual implementation will be hosted under the Open Robotics organization upon selection.

- **Author**: Pavan C N
- **University**: Garden City University, Bangalore
- **Program**: Google Summer of Code 2026
- **Mentorship**: Open Robotics
- **Contact**: p0073100@gmail.com

### Before GSoC (Current Phase)

This repository contains:
- Project proposal and design documentation
- Initial research and tool comparison analysis
- Prototype development and experimentation

### After GSoC Selection

The production code will be migrated to:
- **`open-robotics/ros2_benchmark_suite`** (main repository)
- **`open-robotics/ros2_benchmark_workloads`** (workload definitions)
- **`open-robotics/ros2_benchmark_dashboard`** (visualization)

## References

- [REP 2014: Benchmarking performance in ROS 2](https://ros.org/reps/rep-2014.html)
- [ros2_tracing Documentation](https://github.com/ros2/ros2_tracing)
- [performance_test (iRobot)](https://github.com/irobot-ros/ros2-performance)
- [ros2_benchmark (NVIDIA ISAAC ROS)](https://github.com/NVIDIA-ISAAC-ROS/ros2_benchmark)
- [performance_test_fixture](https://github.com/ros2/performance_test_fixture)
- [ROS 2 Performance Benchmarking Discussion](https://discourse.openrobotics.org/t/ros-2-performance-benchmarking/44382)
- [REP 2004: Quality of Service](https://www.ros.org/reps/rep-2004.html)
