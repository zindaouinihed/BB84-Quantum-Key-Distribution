
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# BB84 QUANTUM KEY DISTRIBUTION (QKD) SIMULATOR
# This program simulates the BB84 protocol and evaluates the
# effect of an intercept-resend eavesdropping attack.
# ============================================================


class BB84Simulator:
    """
    Simulates the BB84 Quantum Key Distribution protocol.

    Parameters:
        number_of_qubits (int): Number of qubits transmitted.
        eve_probability (float): Probability that Eve intercepts
                                 a transmitted qubit.
    """

    def __init__(self, number_of_qubits=1000, eve_probability=1.0):

        self.N = number_of_qubits
        self.eve_probability = eve_probability

        # Initialize protocol variables
        self.alice_bits = None
        self.alice_bases = None
        self.bob_bits = None
        self.bob_bases = None
        self.eve_bits = None
        self.eve_bases = None

        # Initialize the sifted keys and error rate
        self.alice_key = None
        self.bob_key = None
        self.qber = 0

    # --------------------------------------------------------
    # STEP 1: ALICE - RANDOM BIT AND BASIS GENERATION
    # --------------------------------------------------------

    def alice_prepare(self):
        """
        Alice generates random classical bits and encoding bases.
        Basis 0 represents the rectilinear basis (+).
        Basis 1 represents the diagonal basis (x).
        """

        self.alice_bits = np.random.randint(0, 2, self.N)
        self.alice_bases = np.random.randint(0, 2, self.N)

        print("\n[STEP 1] ALICE PREPARATION")
        print("Alice generated", self.N, "random bits.")
        print("Random bases generated successfully.")

    # --------------------------------------------------------
    # STEP 2: BOB - RANDOM MEASUREMENT BASIS SELECTION
    # --------------------------------------------------------

    def bob_choose_bases(self):
        """
        Bob independently selects a random measurement basis
        for each received qubit.
        """

        self.bob_bases = np.random.randint(0, 2, self.N)

        print("\n[STEP 2] BOB BASIS SELECTION")
        print("Bob selected random measurement bases.")

    # --------------------------------------------------------
    # STEP 3: EVE - INTERCEPT-RESEND ATTACK
    # --------------------------------------------------------

    def eve_attack(self):
        """
        Eve intercepts qubits according to the specified probability.

        She randomly chooses measurement bases, measures the
        intercepted qubits, and prepares replacement states.
        """

        intercepted = (
            np.random.random(self.N) < self.eve_probability
        )

        self.eve_bases = np.random.randint(0, 2, self.N)

        # Eve obtains the correct bit when her basis matches
        # Alice's encoding basis; otherwise, the result is random.

        self.eve_bits = np.where(
            self.eve_bases == self.alice_bases,
            self.alice_bits,
            np.random.randint(0, 2, self.N)
        )

        print("\n[STEP 3] EVE ATTACK")
        print("Intercept probability:", self.eve_probability * 100, "%")
        print("Intercepted qubits:", np.sum(intercepted))

        return intercepted

    # --------------------------------------------------------
    # STEP 4: BOB - QUANTUM MEASUREMENT SIMULATION
    # --------------------------------------------------------

    def bob_measure(self, intercepted=None):
        """
        Simulates Bob's measurement outcomes.

        Bob measures either Alice's original states or the
        replacement states prepared by Eve.
        """

        if intercepted is None:
            intercepted = np.zeros(self.N, dtype=bool)

        # Measurement without interception:
        # Matching bases reproduce Alice's bit, while different
        # bases produce a random measurement outcome.

        direct_results = np.where(
            self.bob_bases == self.alice_bases,
            self.alice_bits,
            np.random.randint(0, 2, self.N)
        )

        # Measurement after Eve's interception and resend:
        # Bob measures the states prepared by Eve.

        eve_results = np.where(
            self.bob_bases == self.eve_bases,
            self.eve_bits,
            np.random.randint(0, 2, self.N)
        )

        # Select the appropriate measurement result
        self.bob_bits = np.where(
            intercepted,
            eve_results,
            direct_results
        )

        print("\n[STEP 4] BOB MEASUREMENT")
        print("Bob completed quantum measurements.")

    # --------------------------------------------------------
    # STEP 5: SIFTING - BASIS COMPARISON
    # --------------------------------------------------------

    def sifting(self):
        """
        Alice and Bob publicly compare their measurement bases.

        They retain only positions where their bases match
        and discard all positions with different bases.
        """

        matching = self.alice_bases == self.bob_bases

        self.alice_key = self.alice_bits[matching]
        self.bob_key = self.bob_bits[matching]

        print("\n[STEP 5] SIFTING")
        print("Total qubits:", self.N)
        print("Matching bases:", len(self.alice_key))
        print("Discarded qubits:", self.N - len(self.alice_key))

    # --------------------------------------------------------
    # STEP 6: SECURITY ANALYSIS - QBER CALCULATION
    # --------------------------------------------------------

    def calculate_qber(self):
        """
        Calculates the Quantum Bit Error Rate (QBER).

        QBER is the ratio of mismatched bits between Alice's
        and Bob's sifted keys.
        """

        if len(self.alice_key) == 0:
            self.qber = 0
            return

        errors = np.sum(self.alice_key != self.bob_key)

        self.qber = errors / len(self.alice_key)

        print("\n[STEP 6] SECURITY ANALYSIS")
        print("Number of errors:", errors)
        print("QBER:", round(self.qber * 100, 2), "%")

    # --------------------------------------------------------
    # STEP 7: PARAMETER ESTIMATION
    # --------------------------------------------------------

    def parameter_estimation(self, sample_ratio=0.2):
        """
        Estimates the QBER using a randomly selected sample
        of the sifted key.

        The sample is used to evaluate the observed error rate.
        """

        key_length = len(self.alice_key)

        sample_size = int(key_length * sample_ratio)

        if sample_size == 0:
            print("Not enough bits for parameter estimation.")
            return

        # Randomly select positions for error-rate estimation
        indices = np.random.choice(
            key_length,
            sample_size,
            replace=False
        )

        sample_errors = np.sum(
            self.alice_key[indices] != self.bob_key[indices]
        )

        sample_qber = sample_errors / sample_size

        print("\n[STEP 7] PARAMETER ESTIMATION")
        print("Sample size:", sample_size)
        print("Sample errors:", sample_errors)
        print("Estimated QBER:", round(sample_qber * 100, 2), "%")

        # Illustrative rejection threshold
        if sample_qber > 0.11:
            print("WARNING: High error rate. Reject the key.")
        else:
            print("Error rate is below the illustrative threshold.")

    # --------------------------------------------------------
    # STEP 8: DISPLAY FINAL SIMULATION RESULTS
    # --------------------------------------------------------

    def display_results(self):
        """
        Displays the final sifted keys and simulation statistics.
        """

        print("\n========== FINAL BB84 RESULTS ==========")

        print("Total qubits:", self.N)
        print("Sifted key length:", len(self.alice_key))
        print("QBER:", round(self.qber * 100, 2), "%")

        print("\nAlice's sifted key:")
        print(self.alice_key)

        print("\nBob's sifted key:")
        print(self.bob_key)

        print("\n========================================")


# ============================================================
# EXPERIMENT 1: COMPARISON WITH AND WITHOUT EAVESDROPPING
# ============================================================

def compare_scenarios():
    """
    Runs two BB84 simulations:
    1. Ideal communication without Eve.
    2. Communication under a full intercept-resend attack.
    """

    scenarios = {
        "Without Eve": 0.0,
        "With Eve": 1.0
    }

    results = {}

    for name, probability in scenarios.items():

        print("\n\n################################")
        print("SCENARIO:", name)
        print("################################")

        simulator = BB84Simulator(
            number_of_qubits=1000,
            eve_probability=probability
        )

        # Execute the BB84 protocol
        simulator.alice_prepare()
        simulator.bob_choose_bases()

        intercepted = simulator.eve_attack()

        simulator.bob_measure(intercepted)

        # Extract and evaluate the sifted key
        simulator.sifting()
        simulator.calculate_qber()
        simulator.parameter_estimation()
        simulator.display_results()

        results[name] = simulator.qber * 100

    return results


# ============================================================
# EXPERIMENT 2: EFFECT OF EVE'S INTERCEPTION PROBABILITY
# ============================================================

def analyze_eve_probability():
    """
    Evaluates how different interception probabilities
    influence the QBER.

    The experiment uses 11 probability values between
    0% and 100%.
    """

    probabilities = np.linspace(0, 1, 11)

    qber_values = []

    for probability in probabilities:

        simulator = BB84Simulator(
            number_of_qubits=5000,
            eve_probability=probability
        )

        simulator.alice_prepare()
        simulator.bob_choose_bases()

        intercepted = simulator.eve_attack()
        simulator.bob_measure(intercepted)

        simulator.sifting()
        simulator.calculate_qber()

        qber_values.append(simulator.qber * 100)

    return probabilities * 100, qber_values


# ============================================================
# EXPERIMENT 3: GRAPHICAL VISUALIZATION AND ANALYSIS
# ============================================================

def plot_results(comparison, probabilities, qber_values):
    """
    Creates two plots:
    1. QBER comparison with and without Eve.
    2. QBER variation as Eve's interception probability increases.
    """

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Plot 1: Compare the two communication scenarios
    names = list(comparison.keys())
    values = list(comparison.values())

    axes[0].bar(names, values, color=["green", "red"])

    axes[0].set_title("BB84: With Eve vs Without Eve")
    axes[0].set_ylabel("QBER (%)")
    axes[0].set_ylim(0, 35)

    for i, value in enumerate(values):
        axes[0].text(i, value + 1, f"{value:.2f}%", ha="center")

    # Plot 2: Relationship between interception probability and QBER
    axes[1].plot(
        probabilities,
        qber_values,
        marker="o",
        label="Simulated QBER"
    )

    # Theoretical QBER for an ideal intercept-resend attack
    axes[1].plot(
        probabilities,
        probabilities * 0.25,
        linestyle="--",
        label="Theoretical QBER"
    )

    axes[1].set_title("Effect of Eve on QBER")
    axes[1].set_xlabel("Eve Interception Probability (%)")
    axes[1].set_ylabel("QBER (%)")
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()
    plt.show()


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":

    # Run the comparison experiment
    comparison = compare_scenarios()

    # Study the effect of different Eve probabilities
    probabilities, qber_values = analyze_eve_probability()

    # Generate the final visualization
    plot_results(
        comparison,
        probabilities,
        qber_values
    )
