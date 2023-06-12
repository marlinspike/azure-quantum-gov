from azure.quantum.cirq import AzureQuantumService
from dotenv import load_dotenv
import os,  subprocess
from matplotlib import pyplot
load_dotenv()
import utils
from appsettings import AppSettings
CONFIG_FILE = 'env.json'

app_settings = AppSettings(CONFIG_FILE)

process = subprocess.run([app_settings.settings["azure_login_cmd"]], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True,shell=True)
print(process.stdout)

quantum_target = app_settings.settings["quantum_target"]
print(f"Resource ID: {app_settings.settings['resource_id']}") #print(f"Resource ID: {os.getenv('resource_id')}")
service = AzureQuantumService(
    resource_id = app_settings.settings["resource_id"],
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
# Using the IonQ simulator target. Using 10 repetitions (simulated runs).
job = service.targets(f"{quantum_target}").submit(circuit, name="hello world-cirq-ionq", repetitions=10)

# Print the job ID.
print("Job id:", job.job_id())

# Await job results.
print("Awaiting job results...")
result = job.results()

#Upload results to blob storage
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

