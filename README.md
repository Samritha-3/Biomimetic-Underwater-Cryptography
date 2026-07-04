# Biomimetic-Underwater-Cryptography
A biomimetic cryptographic key engine for ROVs that converts chaotic marine tracking coordinates and nanosecond timestamps into high-entropy SHA-256 keys.

# Biomimetic Underwater Cryptography: Biological Chaos Entropy Engine

An innovative, zero-hardware-overhead cryptographic pipeline designed for Remotely Operated Vehicles (ROVs) and Autonomous Underwater Vehicles (AUVs). This system repurposes live, on-board computer vision object-tracking streams to harvest the chaotic physical coordinates of marine life, transforming biological behavior into high-entropy, non-deterministic SHA-256 keys for secure subsea acoustic communication networks.

---

## 🌊 The Problem & Solution
* **The Problem:** Underwater acoustic communication channels suffer from extremely limited bandwidth and a total lack of native encryption protocols. At the same time, deep-sea exploration vessels like ROVs and AUVs are constrained by strict power and weight limitations, meaning they cannot support the complexity required by dedicated physical Hardware Security Modules (HSMs). Traditional software-based Pseudo-Random Number Generators (PRNGs) fail to solve this problem; if a malicious actor cracks the core pattern or seeding index, the entire communication network becomes compromised.
* **The Solution:** **Biomimetic Cryptography** harvests the naturally chaotic, non-deterministic spatial movements of marine life directly from an already-running computer vision tracking stream. By extracting absolute pixel centers from moving targets and pairing them with nanosecond-precision timestamps and operating system nonces, it achieves a near-perfect Shannon Entropy score with **zero additional hardware** or extra computational overhead.

---

## 🛠️ System Architecture & Code Pipeline

The system is organized into a modular software architecture consisting of four integrated components:

### 1. Computer Vision Layer (`src/extract.py`)
Converts frames from an on-board monitoring camera into localized tracking metrics. The script converts video frames into the HSV color space to dynamically isolate target bounding boxes (configured to isolate red tracking layers by default). It calculates the precise geometric center coordinates of all moving targets across the frame matrix and appends the raw telemetry data to a localized database file (`outputs/tracking_data.csv`).

### 2. Cryptographic Core Layer (`src/key_generation.py`)
Constructs a secure multi-variable seed utilizing three independent layers of continuous physical and systemic randomness:
* **Biological Chaos:** Pipe-separated pixel coordinate configurations of live marine targets (e.g., `"316,334│750,225│569,254"`).
* **Temporal Chaos:** A 64-bit system clock snapshot accurate to the precise nanosecond, updating constantly.
* **Cryptographic Nonce:** 16 bytes of operating system security token randomness via cryptographically secure bytes (`os.urandom(16)`).

> **🛡️ Hybrid Fallback Security Logic:** If marine density drops to zero or visibility is occluded by kicked-up seafloor sediment, the engine automatically switches to a **Fallback Mode** using an extended 32-byte OS-level random seed combined with the nanosecond timestamp. This guarantees absolute data security and uninterrupted key streaming regardless of changing environmental visibility.

### 3. Academic Validation Layer (`src/shannon_entropy.py`)
Evaluates the mathematical randomness and cryptographic strength of generated keys by computing their uniform character distribution using Shannon Entropy ($H$) calculations.

### 4. Interactive Command Dashboard (`src/dashboard.py`)
An integrated desktop user interface built using Tkinter that overlays active detection diagnostics, active tracking metadata frames, real-time key generation hex sequences, and a scrollable system activity ledger concurrently.

---

## 📊 Performance & Validation Data
Statistical testing across standard operational telemetry yields a **Shannon Entropy score of 3.9995 out of a theoretical maximum of 4.0000** (operating at 99.99% of the mathematical ideal), matching or outperforming many dedicated terrestrial hardware random number generators.

Analysis of the project database `tracking_data.csv` verifies operational robustness across varying target counts:
* **Total Simulation Frames Evaluated:** 172 frames
* **Average Targets per Frame:** ~9.8 fish
* **Maximum Observed Target Density:** 18 fish simultaneously tracked

---

## 🚀 How to Run and Deploy the Project

Follow these precise steps to set up your directory environment, install required modules, simulate the pipeline with existing telemetry, and scale it to process your own raw video assets.

### 📁 1. Project Directory Structure Setup
Before running any scripts, ensure your local directory is organized exactly like this. The python scripts must be placed within a folder named `src`, and a folder named `outputs` must exist to hold the telemetry data:

```text
├── README.md
├── results.mp4                 # <-- Place your source video asset here
├── outputs/
│   └── tracking_data.csv       # <-- Auto-generated or placed database file
└── src/
    ├── extract.py
    ├── key_generation.py
    ├── shannon_entropy.py
    └── dashboard.py
```
---

## 🔒 Copyright & Intellectual Property

© 2026 Samritha S. All rights reserved.

This repository and its contents (including all source code, documentation, datasets, and simulation configurations) are the exclusive intellectual property of the author. 

**No license is granted for this software.** Visitors may view and clone the code for personal educational evaluation only. Unauthorized copying, modification, distribution, redistribution, or commercial use of this material without explicit written permission from the author is strictly prohibited.
