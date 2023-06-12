## Exploring Azure Quantum
This repository contains sample code that allows you to run quantum programs on Azure Quantum.

### Creating the Environment file (.env)
The following environment variables are required to run the sample, which should be placed in a file named `.env` in the root directory of the sample.

```bash
resource_id="/subscriptions/xxxx-xxx-xx-xx-xxx/resourceGroups/AzureQuantum/providers/Microsoft.Quantum/Workspaces/rcQuantum"
location="East US"
account_url="https://xxxx.blob.core.windows.net"
storage_account_key="xxxx"
file_dir="output"
quantum_target="ionq.simulator"
```

Here is a description of each variable:
- resource_id: The resource id of the Azure Quantum workspace
- location: The location of the Azure Quantum workspace
- account_url: The url of the Azure Storage account
- storage_account_key: A valid key for the Azure Storage account
- file_dir: The container in the Azure Storage account where the output files will be stored
- quantum_target: The target to run the quantum program on
- azure_login_cmd : The command to login to Azure Commercial. This is used to authenticate to Azure Quantum. This is only required ifyou're running the sample in a container. 

### Creating the JSON properties file
There are some issues with passing an env file via Docker's --env-file flag, so we'll use a JSON properties file instead. The following environment variables are required to run the sample, which should be placed in a file named `env.json` in the root directory of the sample.

Use the output of the *Create Service Pricipal* Step below to populate the azure_login_cmd property.

```json
{
    "resource_id": "/subscriptions/xxxx-xxx-xx-xx-xxx/resourceGroups/AzureQuantum/providers/Microsoft.Quantum/Workspaces/rcQuantum",
    "location": "East US",
    "account_url": "https://xxxx.blob.core.windows.net",
    "storage_account_key": "xxxx",
    "file_dir": "output",
    "quantum_target": "ionq.simulator",
     "azure_login_cmd" : "az login --service-principal -u xx -p xx --tenant xx"
}
```

The app reads from this file. A future version will allow you to pass certain properties via env variables as well.



### Create a Service Principal in Azure Commercial, which will be used to authenticate to Azure Quantum
```bash
 az ad sp create-for-rbac --name "rc-az-quantum" --sdk-auth --role contributor --scopes /subscriptions/xxx/resourceGroups/AzureQuantum
```

Your output should look like this:
```bash
{
  "clientId": "xxx",
  "clientSecret": "xxx",
  "subscriptionId": "xxx",
  "tenantId": "xxx",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

Copy the output of the command, as you'll need it when you create the env.json file, specifically, the azure_login_cmd property.

### Running the sample from the command line
```bash
python3 main.py
```

## Build the container to run the sample
```bash
docker build -t quant-sim:1 .
```

If you're running on a Mac with an M1 chip, you'll may need to build the container for the ARM64 architecture if you want to run it on a Linux host:
```bash
docker build --platform linux/amd64 -t quant-sim:1 .
```

### Running the container
```bash
docker run --rm  quant-sim:1
```

The --rm flag will remove the container after it exits.

You should see the following output:
```bash
This workspace's targets:
- ionq.qpu
- ionq.qpu.aria-1
- ionq.simulator
- quantinuum.hqs-lt-s1
- quantinuum.hqs-lt-s1-apival
- quantinuum.hqs-lt-s2
- quantinuum.hqs-lt-s2-apival
- quantinuum.hqs-lt-s1-sim
- quantinuum.hqs-lt-s2-sim
- quantinuum.qpu.h1-1
- quantinuum.sim.h1-1sc
- quantinuum.qpu.h1-2
- quantinuum.sim.h1-2sc
- quantinuum.sim.h1-1e
- quantinuum.sim.h1-2e
Job id: 47cee0ea-073b-11ee-a6b6-56bf2ceda040
Awaiting job results...
Job finished. State probabilities:
0: 0.5
1: 0.5
{'etag': '"0x8DB695F3176E6E3"', 'last_modified': datetime.datetime(2023, 6, 10, 3, 2, 57, tzinfo=datetime.timezone.utc), 'content_md5': bytearray(b',\x80\xba\x1e\x1b)8X\xda\xee\xf5\x1f\x07^\x87H'), 'client_request_id': '4c1f2d58-073b-11ee-a6b6-56bf2ceda040', 'request_id': '859f2ba8-e01e-0014-0948-9be452000000', 'version': '2022-11-02', 'version_id': None, 'date': datetime.datetime(2023, 6, 10, 3, 2, 56, tzinfo=datetime.timezone.utc), 'request_server_encrypted': True, 'encryption_key_sha256': None, 'encryption_scope': None}
Axes(0.125,0.11;0.775x0.77)
```

You'll also notice that a file with the same name as the Job ID was created in the output container in the Azure Storage account. That's the output of the quantum program.
