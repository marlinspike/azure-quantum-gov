from dotenv import load_dotenv
import os
import uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from typing import Any, Dict
load_dotenv()

storage_account_key = os.getenv("storage_account_key")
account_url = os.getenv("account_url")
#default_credential = DefaultAzureCredential()
#create blob service client
print(f"Storage account key: {storage_account_key}")
print(f"Account url: {account_url}")
client = BlobServiceClient(account_url, credential=storage_account_key) #Use credential=default_credential for integrated auth

def create_output_file(data:str, filename:str="") -> Dict[str, Any]:
    """
    Create a file in the data directory and upload to Azure Blob Storage
    :param data: The data to write to the file
    :param filename: The name of the file to create
    :returns: Blob properties
    """
    blob_props = None
    # Create a file in local data directory to upload and download
    if(filename == ""):
        filename = f"{uuid.uuid4()}.txt"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    local_path = "output"
    upload_file_path = os.path.join(dir_path,local_path, filename)

    # Write text to the file
    with open(upload_file_path, "w") as file:
        file.write(data)

    #print("\nUploading to Azure Storage as blob:\n\t" + upload_file_path)
    blob_client = client.get_blob_client(container="output", blob=filename)

    # Upload the created file
    with open(upload_file_path, "rb") as data:
        blob_props = blob_client.upload_blob(data)

    return blob_props


#data = create_output_file("Hello World")
#print(data)