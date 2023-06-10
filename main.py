from azure.quantum.cirq import AzureQuantumService
from dotenv import load_dotenv
import os
import subprocess
from matplotlib import pyplot
load_dotenv()
import utils

azure_login_cmd = os.getenv("azure_login_cmd").strip('"')

process = subprocess.run(['az login --service-principal -u xx -p xx --tenant xx'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True,shell=True)
print(process.stdout)

quantum_target = os.getenv("quantum_target")
print(f"Resource ID: {os.getenv('resource_id')}")
service = AzureQuantumService(
    resource_id = os.getenv("resource_id"),
    location = "East US" #os.getenv("location"),
)

def print_service_targets():
    print("This workspace's targets:")
    for target in service.targets():
        print("-", target.name)


print_service_targets()

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
job = service.targets(f"{quantum_target}").submit(circuit, name="hello world-cirq-ionq", repetitions=100)

# Print the job ID.
print("Job id:", job.job_id())

# Await job results.
print("Awaiting job results...")
result = job.results()
blob_props = utils.create_output_file(str(result), job.job_id())


# To view the probabilities computed for each Qubit state, you can print the result.
print("Job finished. State probabilities:")
print(result)
if(blob_props != None):
    print(blob_props)


from cirq.vis import plot_state_histogram

# Convert the result to a cirq result by "measuring" the returned
# qubits a number of times equal to the specified number of repetitions.
measurement = result.to_cirq_result()

# We can now use Cirq to plot the results of the "measurement."
result = plot_state_histogram(measurement)
print(result)

