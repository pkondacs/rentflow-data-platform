# Edge Functions

## Definition

An Edge Function is a serverless backend function that executes on demand,
usually through an HTTP request.
## Responsibilities

- Authentication
- Authorization
- Input validation
- Business logic
- Database access
- Data transformation
- Response generation

## Benefits

- No database credentials exposed to clients
- Centralized business logic
- Easier maintenance
- Better security
- Reusable API endpoints
- Serverless scalability

## Comparison
Supabase Edge Function ≈ AWS Lambda ≈ Azure Function

## RentFlow Example

Python
    ↓
HTTP Request + x-api-key
    ↓
Edge Function
    ↓
Service Role
    ↓
PostgreSQL
    ↓
Sanitized JSON
    ↓
Python

## Interview takeaway

Edge Functions are a secure server-side abstraction layer. Instead of exposing the database directly, applications expose controlled APIs that validate requests, enforce permissions, apply business rules, and return only the data required by the caller

# Enterprise Software

Enterprise software is designed to be:
- Maintainable
- Scalable
- Testable
- Reliable
- Easy for multiple engineers to work on

The goal is not only to make the software work, but to make it easy to extend and support over time.

---
## Characteristics

- Separation of responsibilities
- Modular architecture
- Reusable components
- Configuration instead of hardcoding
- Structured logging
- Robust error handling
- Automated testing
- Version control and CI/CD

---
## Single Responsibility Principle (SRP)

Each module should have one responsibility.

**Examples**:
- validators.py → validation
- s3_service.py → S3 operations
- logger.py → logging
- upload_to_s3.py → orchestration

**Benefits**:
- Easier maintenance
- Better testing
- Reduced coupling
- Easier extension

---
## Beginner vs Enterprise

**Beginner**:
- One large script
- Mixed responsibilities
- Hardcoded values
- Minimal error handling

**Enterprise**:
- Layered architecture
- Services and utilities
- Configuration files
- Logging, testing, monitoring

# Mocking

A mock replaces an external dependency with a fake object during testing.

**Purpose**:
- avoid network calls;
- avoid cloud costs;
- produce deterministic tests;
- make tests fast.

**Typical external dependencies:**
- AWS SDK (boto3)
- PostgreSQL
- REST APIs
- Databricks
- Kafka

A mock does not perform the real action.

Instead, it records:
- whether a method was called;
- how many times;
- with which parameters.

This allows unit tests to verify application logic without relying on external systems.

# Requirements.txt
Stores the Python dependencies required by the project.
## Create
python -m pip freeze > requirements.txt
## Install
python -m pip install -r requirements.txt
## Why use `python -m pip`?
Ensures that pip runs with the currently active Python interpreter or virtual environment.
## Why use `freeze`?
Creates a snapshot of all installed packages and their exact versions, allowing the environment to be reproduced consistently.