# CCG Research Index

## Deployment

### 1. Create a memgraph instance on Microsoft Azure.

Once the VM is up and running, SSH into the VM, download and install memgraph

    curl -O https://download.memgraph.com/memgraph/v2.13.0/ubuntu-20.04/memgraph_2.13.0-1_amd64.deb
    dpkg -i /memgraph_2.13.0-1_amd64.deb

### 2. Deploy front-end to Vercel and provision database

