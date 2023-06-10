# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim
#mcr.microsoft.com/azure-cli
#python:3.11-slim

# On/Off for Python generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=0

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

RUN az login --service-principal -u 115f1e1a-4e9f-443d-869f-a2be6cf0f47c -p KzP8Q~XqEUnOgPYcyjAZpmmjE6f_Ys.5z43~5dpz --tenant 72f988bf-86f1-41af-91ab-2d7cd011db47
RUN az vm list -o table

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "main.py"]