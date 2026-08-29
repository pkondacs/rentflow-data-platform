## Prefixes vs Folders

Although the AWS Console displays folders, Amazon S3 is a flat object store.
Objects are identified by keys.

**Example**:
raw/agencies/2026/07/29/agencies.json

The `raw/agencies/2026/07/29/` part is a prefix, not a real directory.
## Purpose 
Object storage used as the foundation of a cloud data lake. 
## Core concepts 
- Buckets
- Objects
- Keys
- Prefixes
- Versioning
## Important 
S3 has object keys and prefixes—not real folders. 
## Today's Learning 
- Created the first data-lake bucket. 
- Enabled versioning. 
- Enabled encryption. 
- Public access blocked.
## Project implementation

Repository:
`rentflow-data-platform`

Branch:
`aws-learning`

Initial structure:
- `aws/s3/scripts`
- `aws/s3/sample_data`
- `aws/s3/tests`
## Authentication

Boto3 can use credentials from the AWS CLI configuration.
Credentials must never be hard-coded or committed to Git.
## What is `boto3`?

**`boto3` is the official AWS SDK (software development kit) for Python.**

Think of it like this:

|Platform|Python library|
|---|---|
|AWS|**boto3**|
|Azure|`azure-storage-blob`, `azure-identity`, `azure-mgmt-*`|
|Databricks|`databricks-sdk`|
|PostgreSQL|`psycopg2` or `sqlalchemy`|
Instead of clicking buttons in the AWS Console, `boto3` lets your Python code call AWS APIs.
For example:
```
import boto3
s3 = boto3.client("s3")
s3.upload_file(...)
```

Behind the scenes, `boto3` makes authenticated HTTPS API calls to AWS.
### How important is it?

For a Data Engineer or Data Architect, I'd rate it:
⭐⭐⭐⭐⭐ (5/5)

You'll use it for:
- S3
- Lambda
- Glue
- Athena
- IAM
- CloudWatch
- STS
- Secrets Manager
- and many other AWS services.

If someone says "automate AWS with Python", they almost always mean **using `boto3`**.
## Raw snapshot naming

Example:

raw/agencies/
ingestion_year=2026/
ingestion_month=07/
ingestion_day=29/
agencies_20260729T215300Z.json

**Reasons**:

- Every execution creates a historical snapshot.
- UTC timestamps avoid timezone ambiguity.
- Date prefixes prepare data for partitioned querying.
- Object metadata records source and ingestion context.

