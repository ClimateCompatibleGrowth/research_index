# CCG Research Index

## Development

To enter development mode of the website, with the memgraph database running in the background, run

    python app/app.py

## Deployment

### 1. Create a memgraph instance on Microsoft Azure.

Once the VM is up and running, SSH into the VM, download and install memgraph

    curl -O https://download.memgraph.com/memgraph/v2.14.1/ubuntu-20.04/memgraph_2.14.1-1_amd64.deb
    sudo dpkg -i /memgraph_2.14.1-1_amd64.deb

### 2. Build Docker container

    docker build

Run the docker container in development mode to test

    docker run -dp 5001:80 -w /app -v "$(pwd):/app" research-index-gunicorn-311 sh -c "python app/app.py"

### 3. Deploy front-end to Azure and provision database

Push container to docker hub

    docker container commit c385 ccg-research-index:v0.1
    docker image tag ccg-research-index:v0.1 willu47docker/ccg-research-index:ccg-research-index
    docker image push willu47docker/ccg-research-index:ccg-research-index
