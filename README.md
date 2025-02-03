# CCG Research Index

## Development

Create a `.env` file in the project root with the following environment variables:
```sh
MG_HOST=          # Memgraph host address
MG_PORT=          # Default Memgraph port
MG_PORT_ALT=      # Alternative port
MG_USER=          # Memgraph user
MG_PASS=          # Memgraph user password
```

To enter development mode of the website, with the memgraph database running in the background, run

    fastapi dev app/main.py

## Deployment

### 1. Create a memgraph instance on Microsoft Azure.

Once the VM is up and running, SSH into the VM, download and install memgraph

    curl -O https://download.memgraph.com/memgraph/v2.14.1/ubuntu-20.04/memgraph_2.14.1-1_amd64.deb
    sudo dpkg -i /memgraph_2.14.1-1_amd64.deb
Set up the Memgraph user to match the credentials specified in the `.env` file.

### 2. Build Docker container

    docker build -t research_index_web_app:development .

Run the docker container in development mode to test

    docker run -dp 8000:8000 research_index_web_app:development

    docker run -dp 5001:80 -w /app -v "$(pwd):/app" research-index-gunicorn-311 sh -c "python app/app.py"

### 3. Deploy front-end to Azure and provision database

Push container to docker hub

    docker container commit c385 ccg-research-index:v0.1
    docker image tag ccg-research-index:v0.1 willu47docker/ccg-research-index:ccg-research-index
    docker image push willu47docker/ccg-research-index:ccg-research-index
