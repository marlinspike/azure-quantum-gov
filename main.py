from azure.quantum.cirq import AzureQuantumService
from dotenv import load_dotenv
import os
from matplotlib import pyplot
load_dotenv()
service = AzureQuantumService(
    resource_id = os.getenv("resource_id"),
    location = os.getenv("location"),
)

print("This workspace's targets:")
for target in service.targets():
    print("-", target.name)

# Build the quantum program
import cirq

q0 = cirq.LineQubit(0)
circuit = cirq.Circuit(
    cirq.H(q0),               # Apply an H-gate to q0
    cirq.measure(q0)          # Measure q0
)
circuit

#Submit the quantum program to Azure Quantum
# Using the IonQ simulator target, call "run" to submit the job. We'll
# use 100 repetitions (simulated runs).
job = service.targets("ionq.simulator").submit(circuit, name="hello world-cirq-ionq", repetitions=100)

# Print the job ID.
print("Job id:", job.job_id())

# Await job results.
print("Awaiting job results...")
result = job.results()

# To view the probabilities computed for each Qubit state, you can print the result.
print("Job finished. State probabilities:")
print(result)


from cirq.vis import plot_state_histogram

# Convert the result to a cirq result by "measuring" the returned
# qubits a number of times equal to the specified number of repetitions.
measurement = result.to_cirq_result()

# We can now use Cirq to plot the results of the "measurement."
result = plot_state_histogram(measurement)
print(result)

