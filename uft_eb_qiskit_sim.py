from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
from qiskit.providers.aer.noise import NoiseModel, thermal_relaxation_error
import numpy as np

# Setup basic 6-qubit entangled circuit
qc = QuantumCircuit(6)
for q in range(6):
    qc.h(q)
for q in range(5):
    qc.cx(q, q+1)
qc.measure_all()

# Setup noise model
noise_model = NoiseModel()
for q in range(6):
    t1, t2, time = 50e-6, 30e-6, 0.1e-6
    error = thermal_relaxation_error(t1, t2, time)
    noise_model.add_quantum_error(error, ['id'], [q])

# Simulate
sim = Aer.get_backend('qasm_simulator')
qobj = assemble(transpile(qc, sim))
result = sim.run(qobj, noise_model=noise_model).result()

# Display results
counts = result.get_counts()
print("Simulation Results with Φ-thresholding-like noise:", counts)
