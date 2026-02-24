import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Quantum-Inspired Reed–Solomon Encoding",
    layout="wide"
)

st.title("Quantum-Inspired Reed–Solomon (RS) Encoding Experiment")
st.markdown("---")

# -----------------------------
# SECTION 1: MDS CODES THEORY
# -----------------------------
st.header("1️⃣ Maximum Distance Separable (MDS) Codes")

st.markdown("""
A **Maximum Distance Separable (MDS) code** satisfies the **Singleton Bound**:

\[
d = n - k + 1
\]

where:
- **n** = codeword length  
- **k** = message length  
- **d** = minimum distance  

**Reed–Solomon codes are optimal MDS codes**, meaning they achieve the maximum possible error-correcting capability.
""")

col1, col2 = st.columns(2)
with col1:
    n = st.number_input("Enter n (codeword length)", min_value=2, value=7)
with col2:
    k = st.number_input("Enter k (message length)", min_value=1, max_value=n-1, value=3)

d = n - k + 1
st.success(f"Minimum Distance (d) = n − k + 1 = **{d}**")

st.markdown("---")

# -----------------------------
# SECTION 2: CLASSICAL RS ENCODING
# -----------------------------
st.header("2️⃣ Classical Reed–Solomon Encoding")

st.markdown("""
Reed–Solomon encoding is done by:
1. Treating the message symbols as coefficients of a polynomial  
2. Evaluating the polynomial at distinct points  

\[
m(x) = a_0 + a_1x + a_2x^2 + \dots
\]
""")

msg = st.text_input(
    "Enter message symbols (comma separated)",
    value="3,5,2"
)

try:
    message = [int(x.strip()) for x in msg.split(",")]
    degree = len(message) - 1

    st.write("**Message Polynomial:**")
    poly_str = " + ".join([f"{message[i]}x^{i}" for i in range(len(message))])
    st.code(f"m(x) = {poly_str}")

    eval_points = list(range(1, len(message) + 3))
    codeword = []

    for x in eval_points:
        val = sum(message[i] * (x ** i) for i in range(len(message)))
        codeword.append(val)

    st.write("**Evaluation Points:**", eval_points)
    st.success(f"Encoded RS Codeword: {codeword}")

except:
    st.error("Please enter valid integers.")

st.markdown("---")

# -----------------------------
# SECTION 3: QUANTUM-INSPIRED ENCODING
# -----------------------------
st.header("3️⃣ Quantum-Inspired RS Encoding")

st.markdown("""
In quantum systems, finite-field arithmetic is not directly available.
So we **simulate RS encoding concepts** using:

- **Quantum superposition** → parallel evaluation  
- **Quantum registers** → message symbols  
- **Measurement** → encoded output  

⚠️ This is a **quantum-inspired simulation**, not a true quantum RS code.
""")

num_qubits = st.slider("Number of Qubits (symbols)", 2, 5, 3)

qc = QuantumCircuit(num_qubits, num_qubits)

# Create superposition
for i in range(num_qubits):
    qc.h(i)

# Toy "encoding" logic
for i in range(num_qubits - 1):
    qc.cx(i, i + 1)

qc.measure(range(num_qubits), range(num_qubits))

st.subheader("Quantum Circuit")
st.pyplot(qc.draw(output="mpl"))

backend = AerSimulator()
job = backend.run(qc, shots=1024)
result = job.result()
counts = result.get_counts()

st.subheader("Measurement Output (Quantum-Inspired Codeword)")
st.pyplot(plot_histogram(counts))

st.markdown("---")

# -----------------------------
# SECTION 4: INTERPRETATION
# -----------------------------
st.header("4️⃣ Interpretation")

st.markdown("""
- Classical RS codes use **finite-field polynomial evaluation**
- Quantum circuits use **superposition & entanglement**
- This experiment shows how **classical ECC ideas map to quantum computation**
- Forms a conceptual bridge toward **Quantum Error Correction**
""")

st.info("""
✔ Correct academic name:
**“Quantum-Inspired Simulation of Reed–Solomon Encoding”**

✖ Avoid:
“Quantum Reed–Solomon Code” (advanced research topic)
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Virtual Lab Experiment | Quantum Computing & Error Control Codes")