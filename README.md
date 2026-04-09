# Project Progress Summary

Application: FastAPI-based microservice with a structured app/ layout and full dependency management (requirements.txt).

Version Control: Git repository initialized.

Containerization:

- Dockerized using python:3.13-slim for a lightweight footprint.

- Optimized build process with Layer Caching and .dockerignore.

Cloud Registry:

- Private AWS ECR repository created via AWS CLI.

- Secure authentication using AWS SSO (Identity Center) profiles.

- Docker image built, tagged, and pushed to ECR (v1).

Infrastructure as Code (IaC):

- Initialized Terraform with the AWS provider using a dedicated SSO profile. All below resources were created using Terraform.

Networking & Security:

- Deployed VPC using a verified community module, featuring public and private subnets across multiple Availability Zones.

- Implemented a NAT Gateway to allow secure outbound connectivity for private resources.

- Implemented Security Groups with fine-grained rules.

Container Orchestration (ECS):

- Configured an ECS Cluster and defined IAM Roles for task execution and ECR access.

- Created an ECS Task Definition for the FastAPI application with optimized Fargate resource allocation (0.25 vCPU / 0.5 GB RAM).

- Deployed an ECS Service managing the container lifecycle in private subnets.

Load Balancing:

- Application Load Balancer (ALB): Deployed a public-facing ALB to distribute traffic across ECS tasks in private subnets.

- Target Groups & Health Checks: Configured HTTP health checks on /health to ensure traffic is only routed to healthy containers.

- Security Layering: Implemented a dual-layer SG architecture: ALB accepts public traffic on port 80 and forwards it to ECS tasks on port 8000 via a private internal "relay".

Monitoring & Observability:

- CloudWatch Logs: Configured centralized logging using awslogs driver.

- Log Groups: Created dedicated CloudWatch Log Groups with defined retention policies for real-time application monitoring and debugging.

Database & Secrets Management:

- AWS RDS (PostgreSQL): Deployed a managed PostgreSQL 15 instance within private subnets to ensure data isolation.

- DB Subnet Groups: Isolated database traffic within a dedicated subnet group across multiple Availability Zones.

- AWS Secrets Manager: Implemented secure credential management. Database passwords are automatically generated via random_password and injected into ECS tasks at runtime.

- IAM Access: Configured ECS Task Execution Role with specific GetSecretValue permissions to retrieve credentials without hardcoding them in the environment.
