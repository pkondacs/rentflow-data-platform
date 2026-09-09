# AWS CLI

## Purpose

The AWS Command Line Interface (CLI) allows my local computer to interact with AWS services through authenticated API calls.

## Why is it important?

- Automates AWS tasks.
- Used by scripts, CI/CD pipelines and Infrastructure as Code.
- Faster and more repeatable than using the web console.
- Required for many professional workflows.

## Typical commands

```powershell
aws --version
aws configure
aws s3 ls
aws iam list-users
```
## Today's progress

- AWS account created.
- IAM administrator user created.
- Budgets configured.
- AWS CLI installation started.

## Authentication Flow

Laptop
    │
    ▼
AWS CLI
    │
    ▼
IAM Access Key
    │
    ▼
AWS API
    │
    ▼
AWS Services

## Verification Commands

aws --version
aws sts get-caller-identity
aws iam list-users