# BB84-Quantum-Key-Distribution
A Python simulation of the BB84 Quantum Key Distribution protocol and Intercept-Resend attack. 

## Project Overview

This project presents a Python-based simulation of the **BB84 Quantum Key Distribution (QKD) protocol**, introduced by Charles Bennett and Gilles Brassard in 1984.

The simulation demonstrates how two parties, Alice and Bob, can establish a shared secret key using quantum principles, and how an eavesdropper (Eve) can compromise the communication through an Intercept-Resend attack.

## Objectives

- Understand the fundamental principles of the BB84 protocol.
- Simulate quantum key distribution between Alice and Bob.
- Demonstrate the impact of an Intercept-Resend attack.
- Analyze the Quantum Bit Error Rate (QBER).
- Compare the protocol's behavior with and without an eavesdropper.

## Protocol Workflow

1. **State Preparation:** Alice randomly generates bits and encoding bases.
2. **Quantum Transmission:** Alice sends the encoded quantum states to Bob.
3. **Measurement:** Bob randomly chooses measurement bases.
4. **Sifting:** Alice and Bob compare their bases and keep only matching positions.
5. **Eavesdropping Detection:** They estimate the QBER to detect possible interference.

## Eve's Intercept-Resend Attack

Eve intercepts the transmitted quantum states, measures them using randomly selected bases, and resends new states to Bob.

This attack introduces errors that can be detected through QBER analysis.

## Technologies Used

- Python
- NumPy
- Matplotlib

## Installation

Clone the repository:

```bash
git clone https://github.com/zindaouinihed/BB84-Quantum-Key-Distribution.git
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Running the Simulation

```bash
python bb84.py
```

## Results and Analysis

The simulation compares QBER values with and without Eve's intervention and studies how the error rate changes with the interception probability.

In an ideal BB84 simulation, a full Intercept-Resend attack introduces an expected QBER of approximately **25%** in the sifted key.

### QBER Analysis
![QBER Analysis](images/qber_analysis.png)

## Important Note

This project is an educational classical simulation of the BB84 protocol. It illustrates the protocol's logic and security principles but does not implement actual quantum hardware or a complete practical QKD system.

## Author

**Nihed Zindaoui**

[GitHub Profile](https://github.com/zindaouinihed)
