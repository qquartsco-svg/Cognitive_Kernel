# Cognitive Kernel

> **Give your AI agent persistent memory. 3 lines of code.**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/cognitive-kernel)](https://pypi.org/project/cognitive-kernel/)

**Cognitive Kernel** is a modular cognitive framework that simulates brain-like memory, decision-making, and cognitive dynamics for AI agents.

## 🚀 Quick Start

```python
from cognitive_kernel import CognitiveKernel

# Create kernel
kernel = CognitiveKernel()

# Remember
kernel.remember("I like coffee", importance=0.9)

# Decide
decision = kernel.decide(["rest", "work", "exercise"])
print(decision["action"])  # "work"
```

## 🧠 Core Features

### 7 Core Engines
- **Panorama Memory**: Temporal event storage
- **MemoryRank**: Personalized PageRank for memory importance
- **Prefrontal Cortex (PFC)**: Softmax utility-based decision-making
- **Basal Ganglia**: Q-Learning for habit formation
- **Thalamus**: Input filtering/gating
- **Amygdala**: Emotion processing
- **Hypothalamus**: Energy management

### Cognitive Dynamics
- **Entropy-based Dynamics**: Automatic rotational torque generation
- **Core Strength**: Memory gravity (convergence force)
- **Precession**: Slow rotation of preference axis in state space
- **Maxwell Structure**: ADHD(+) ↔ ASD(-) poles create magnetic field
- **Core Decay**: Dementia/Alzheimer's modeling

### Cognitive Modes
- `NORMAL`, `ADHD`, `ASD`, `PTSD`
- `PANIC`, `EPILEPSY`, `OCD`, `IED`
- `DEPRESSION`, `BIPOLAR`
- `DEMENTIA`, `ALZHEIMER` ⭐

## 📚 Documentation

### Core Concepts
- [Maxwell Structure in State Space](docs/MAXWELL_STRUCTURE.md) - ADHD/ASD poles and magnetic field
- [Physical Dynamics](docs/PHYSICAL_DYNAMICS.md) - Precession and rotational dynamics
- [Stability Core](docs/STABILITY_CORE.md) - Mental resilience model

### Advanced Features
- [Dementia & Alzheimer's Dynamics](docs/DEMENTIA_ALZHEIMER_IMPLEMENTATION.md) - Memory loss modeling
- [Dynamics Engine](docs/DYNAMICS_ENGINE_FUNCTIONS.md) - Entropy, core strength, torque
- [Disorder Spectrum](docs/DISORDER_SPECTRUM_ANALYSIS.md) - Cognitive disorder mapping

### Technical
- [API Reference](docs/API_REFERENCE.md)
- [Version History](docs/version_history/VERSION_HISTORY.md)
- [PHAM Blockchain](docs/version_history/PHAM_BLOCKCHAIN_LOG.md)

## 🔬 Cognitive Dynamics Explained

### Entropy & Core Strength

**Entropy** measures choice uncertainty:
```
E = -Σ P(k) ln P(k)
```

**Core Strength** is memory gravity that reconverges entropy:
```
C(t) = C(0) * exp(-λ * Δt)
```

### Precession & Rotational Torque

The system generates **automatic rotational torque** based on entropy:
```
T(k) = γ * E_norm * cos(φ - ψ_k)
```

This creates a **precession** (slow rotation) of the preference axis in state space.

### Maxwell Structure

ADHD(+) and ASD(-) poles create an **effective magnetic field** in cognitive state space:
- **ADHD**: High entropy → Strong rotation → Exploration
- **ASD**: Low entropy → Weak rotation → Exploitation

See [Maxwell Structure](docs/MAXWELL_STRUCTURE.md) for details.

### Dementia & Alzheimer's

**Dementia**: Gradual core strength decay
- Old memories decay faster (`old_memory_decay_rate`)
- New memories remain intact

**Alzheimer's**: Rapid core strength collapse
- New memories decay immediately (`new_memory_decay_rate`)
- Core decay rate is high
- Memory update failure

See [Dementia & Alzheimer's Implementation](docs/DEMENTIA_ALZHEIMER_IMPLEMENTATION.md) for details.

## 📦 Installation

```bash
pip install cognitive-kernel
```

## 🎯 Usage Examples

### Basic Memory & Decision

```python
from cognitive_kernel import CognitiveKernel

kernel = CognitiveKernel()

# Remember events
kernel.remember("I prefer morning coffee", importance=0.9)
kernel.remember("I exercise at 6pm", importance=0.8)

# Decide
decision = kernel.decide(["rest", "work", "exercise"])
print(decision["action"])  # "exercise"
```

### Cognitive Modes

```python
# ADHD mode (high entropy, strong rotation)
kernel.set_mode("ADHD")

# ASD mode (low entropy, weak rotation)
kernel.set_mode("ASD")

# Dementia mode (core decay)
kernel.set_mode("DEMENTIA")

# Alzheimer's mode (rapid core collapse)
kernel.set_mode("ALZHEIMER")
```

### Long-term Memory

```python
# Save session
kernel.save_session("my_session.json")

# Load session
kernel.load_session("my_session.json")
```

## 🏗️ Architecture

```
Cognitive Kernel
├── Panorama Memory (Event Storage)
├── MemoryRank (Importance Ranking)
├── Prefrontal Cortex (Decision-making)
├── Basal Ganglia (Habit Formation)
├── Thalamus (Input Filtering)
├── Amygdala (Emotion Processing)
├── Hypothalamus (Energy Management)
└── Dynamics Engine (Entropy, Core, Torque)
```

## 🔗 Related Projects

- [Dynamics Engine](https://github.com/gnjz/dynamics-engine) - Standalone dynamics module
- [MemoryRank Engine](https://github.com/gnjz/memoryrank-engine) - Memory ranking

## 📄 License

MIT License

## 👤 Author

**GNJz (Qquarts)**

---

**Version**: 2.0.2  
**Last Updated**: 2026-01-31
