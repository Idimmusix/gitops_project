# Full Stack Automation Project Documentation

## Table of content

- [Overview](#overview)
- [Objectives](#objectives)
- [Technologies](#technologies)
- [Project Architecture](#project-architecture)
- [Project Structure](#project-structure)
- [Pipeline Configuration Files](#pipeline-configuration-files)
- [Infrastructure Pipelines](#infrastructure-pipelines)
- [Application Pipelines](#application-pipelines)



## Overview

This project uses GitOps principles to streamline infrastructure and application deployment. It leverages Github Actions CI/CD with tools like Terraform, Ansible, and Docker, to ensure efficient and automated provisioning and monitoring.

## Objectives

- **Cloud cost optimization** with cost estimation tools like InfraCost.  
- **GitOps workflows** for seamless automation.  
- **Terraform + Ansible integration** for infrastructure management and monitoring stack setup.  
- **Git branching strategies** for streamlined CI/CD pipelines.  

## Technologies
- **Terraform**: Infrastructure as Code tool to provision cloud resources.
- **Ansible**: Configuration management tool used for provisioning and configuring servers.
- **Docker**: Containerization platform used to package the application and monitoring stacks.
- **Traefik**: Reverse proxy for routing traffic between containers.
- **Grafana**: Used to monitor and visualize container-level metrics and logs.  
- **Prometheus**: collection of metrics
- **cAdvisor**: exposes container-level metrics
- **Loki**: log aggregation
- **Promtail**: log collection


## Project Architecture
<img src=".assets/gitops.png" alt="Architecture Image" />


## Project Structure
```
📦 Project Root
│
├── .github/
│   └── workflows/              # GitHub Actions CI/CD workflows
│       ├── ansible-monitoring.yml      # Workflow to trigger Ansible for monitoring stack
│       ├── cd-backend.yml              # Continuous Deployment workflow for backend
│       ├── cd-frontend.yml             # Continuous Deployment workflow for frontend
│       ├── ci-backend.yml              # Continuous Integration workflow for backend
│       ├── ci-frontend.yml             # Continuous Integration workflow for frontend
│       ├── terraform-apply.yml         # Workflow to apply Terraform configurations
│       ├── terraform-plan.yml          # Workflow to run 'terraform plan' and output cost estimations
│       └── terraform-validate.yml      # Workflow to validate Terraform configurations
│
├── ansible/
│   ├── roles/                  # Directory for Ansible roles (future role definitions)
│   ├── compose.monitoring.yml  # Docker Compose configuration for monitoring services
│   └── playbook.yml            # Main playbook for configuring the monitoring stack
│
├── backend/                    # Backend code and resources
│   └── ...                     # (Add backend-related files and folders here)
│
├── frontend/                   # Frontend code and resources
│   └── ...                     # (Add frontend-related files and folders here)
│
├── monitoring/
│   ├── dashboards/             # Directory for custom Grafana dashboards
│   ├── dashboard-providers.yml # Grafana dashboard provider configuration
│   ├── loki-config.yml         # Loki log aggregation configuration
│   ├── loki-datasource.yml     # Grafana datasource configuration for Loki
│   ├── prometheus-datasource.yml # Prometheus datasource configuration for Grafana
│   ├── prometheus.yml          # Prometheus main configuration file
│   └── promtail-config.yml     # Promtail configuration for log scraping
│
├── terraform/
│   ├── ansible.tf              # Terraform resource for triggering Ansible
│   ├── backend.tf              # Backend configuration for Terraform state management
│   ├── dns.tf                  # DNS configurations
│   ├── ec2.tf                  # EC2 resource definitions
│   ├── main.tf                 # Main Terraform entry point
│   ├── output.tf               # Outputs from Terraform resources
│   ├── variables.tf            # Input variables for Terraform configurations
│   └── vpc.tf                  # VPC configuration for network setup
│
|
├── compose.yml                 # Docker Compose configuration file for full-stack services
└── README.md                   # Documentation and project overview
```

## Pipeline Configuration Files
The CI/CD pipelines are divided into modular `.yml`files for better organization and maintainability:

- Infrastructure Pipelines:
  - `terraform-validate.yml`: Validates Terraform configurations.
  - `terraform-plan.yml`: Runs terraform plan and includes cost estimation in PR comments.
  - `terraform-apply.yml`: Applies the Terraform configuration with auto-approval.
  - `ansible-monitoring.yml`: Deploys the monitoring stack using Ansible.
  

- Application Pipelines:
  - `ci-frontend.yml`: Builds, test, packages and pushes the frontend Docker images, then updates compose.yml.
  - `cd-frontend.yml`: Deploys the frontend container in the cloud.
  - `ci-backend.yml`: Builds, test, packages and pushes the backend Docker images, then updates compose.yml.
  - `cd-backend.yml`: Deploys the backend, posgresql, and adminer containers in the cloud.

  


## Infrastructure Pipelines
These pipelines automates infrastructure provisioning and monitoring stack setup using Terraform and Ansible. Additionally, it utilizes an incredible tool such as InfraCost for cost breakdown, estimation and optimization.

### Branching Strategy
---
- `infra_features`: For writing and testing Terraform configurations.
- `main`: The main branch for infrastructure management and provisioning.

### Pipeline Workflow
---
- Workflow Steps:
  - Push to `infra_features`: Triggers `terraform-validate.yml` to ensure configuration correctness.
  - Pull Request to `main` with changes in the `ansible`, `monitoring`, `terraform` directories, `.github/workflows/{ansible-monitoring.yml, terraform-apply.yml, terraform-plan.yml, terraform-validate.yml}` files: Triggers `terraform-plan.yml` which returns infrastructure plan and cost analysis as a PR comment.
  - Merge to `main` with changes to the `ansible`, `monitoring` or `terraform` directories, `.github/workflows/{ansible-monitoring.yml, terraform-apply.yml, terraform-plan.yml, terraform-validate.yml}` files: Triggers `terraform-apply.yml`terraform apply to provision infrastructure resources. `terraform-apply.yml` on successful completion, then trigger `ansible-monitoring.yml` to configure the server and deploy the monitoring stack (Prometheus, Grafana, Loki, Promtail & Cadvisor).
  
## Application Pipelines
The application pipeline build, test, packages and deploy the three-tier application stack.
### Branching Strategy
---
- `integration`: For managing the continuous integration of the applications
- `main` with changes to the `frontend` or `backend` directories, `.github/workflows/{cd*.yml,ci*.yml}` files: For managing the continuous deployment of the containerized applications.

### Pipeline Workflow
---
- Workflow Steps:
  - Pull request from `integration` to `main`: Build Docker images for the application.
    - `ci-frontend.yml`: This pipeline is triggered when changes are made to the `frontend/` folder or the `ci-frontend.yml` file. Build, test and push the frontend image to dockerhub. Then it updates compose.yml with the recent frontend image tag.
    - `ci-backend.yml`: This pipeline is triggered when changes are made to the `backend/` folder or the `ci-backend.yml` file. Build, test and push the backend image to dockerhub. Then it updates compose.yml with the recent backend image tag.

  - Merge from `integration` to `main`: Deploys the application stack to the provisioned cloud infrastructure.
    - `cd-frontend.yml`: This pipeline is triggered when changes are made to the `frontend/` folder or the `cd-frontend.yml` file. It pulls the updated docker image and deploys it.
    - `cd-backend.yml`: This pipeline is triggered when changes are made to the `backend/` folder or the `cd-backend.yml` file. It pulls the updated docker image and deploys it.