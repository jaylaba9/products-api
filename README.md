# AWS Cloud-Native FastAPI Microservice

A FastAPI application deployed on a highly available and secure AWS infrastructure using **Terraform (IaC)**. This project demonstrates modern DevOps practices, including containerization, private networking, and automated secrets management.

## Architecture Overview

The infrastructure is designed with a "Security First" approach, ensuring that sensitive resources like the database are never exposed to the public internet.

* **Networking:** Custom VPC with Public and Private subnets across multiple Availability Zones.
* **Compute:** AWS ECS (Fargate) for serverless container orchestration.
* **Load Balancing:** Application Load Balancer (ALB) acting as the single entry point.
* **Database:** AWS RDS (PostgreSQL 15) isolated in private subnets.
* **Security:** AWS Secrets Manager for credential rotation, Security Groups (ALB -> ECS -> RDS).

---

## Tech Stack

 * **Backend**: Python 3.13, FastAPI 
 * **ORM**: SQLAlchemy
 * **Containerization**: Docker (optimized `python:3.13-slim` image + layer caching) 
 * **Infrastructure**:  Terraform 
 * **Cloud Provider**:  AWS (ECR, ECS, RDS, Secrets Manager, CloudWatch) 

---

## Security Highlights

* **Zero Public Access to DB:** The RDS instance is located in a private subnet with no public IP. Access is only allowed from the ECS service on port 5432.
* **Secrets Management:** No hardcoded credentials. Database passwords are:
    1. Generated via Terraform (`random_password`).
    2. Stored in **AWS Secrets Manager**.
    3. Injected into ECS Tasks as environment variables at runtime.
* **IAM Least Privilege:** The ECS Task Execution Role is strictly limited to pulling images from ECR and reading specific secrets.
* **Observability:** Centralized logging with **AWS CloudWatch Logs**, including `PYTHONUNBUFFERED` logging for real-time debugging.

---

## Features implemented

* **Full CRUD Support:** Endpoints for creating, listing, and deleting products.
* **Auto-Migration:** Database tables are automatically created on application startup (SQLAlchemy `create_all`).
* **Health Monitoring:** Dedicated `/health` endpoint for ALB health checks.
* **Dependency Management:** Clean `requirements.txt` with locked versions for stability.

---

## Infra and API in action

Using API:
<img width="1282" height="679" alt="image" src="https://github.com/user-attachments/assets/48b4e37e-c4f2-4fbf-9546-69a0d53f0a29" />

ECS Cluster:
<img width="1899" height="657" alt="Zrzut ekranu 2026-04-11 083248" src="https://github.com/user-attachments/assets/4f467c77-dd5c-4206-ba33-44d8b2d1805f" />

Logs from startup:
<img width="897" height="587" alt="Zrzut ekranu 2026-04-11 083817" src="https://github.com/user-attachments/assets/add6e9b2-037f-446a-8125-43968a524242" />

Destroying infrastructure:
<img width="421" height="57" alt="Zrzut ekranu 2026-04-11 084928" src="https://github.com/user-attachments/assets/4503633e-a9fb-4677-b48d-9aa1bf2bf05f" />

