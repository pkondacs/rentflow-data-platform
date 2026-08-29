## Test Suite

A test suite is the complete collection of automated tests for a project.

**Purpose**:
- Verify existing functionality still works after changes.
- Detect regressions early.
- Increase confidence before committing and deploying.

**Typical workflow:**

1. Modify code.
2. Run `pytest`.
3. Ensure all tests pass.
4. Commit changes.
5. Push to GitHub.
6. CI/CD executes the same test suite automatically.

**SCENARIO**: 
Instead of manually checking every feature after making a change, you let the test framework do it for you. For example, imagine six months from now your project contains:

```
aws/
└── s3/
    └── tests/
        test_validators.py
        test_object_keys.py
        test_s3_service.py

aws/
└── lambda/
    └── tests/
        test_lambda_handler.py

aws/
└── postgres/
    └── tests/
        test_extractor.py

aws/
└── glue/
    └── tests/
        test_glue_job.py
```

When you run:
```
pytest
```

`pytest` (or `pytest -v` ) automatically discovers every file whose name starts with `test_` and executes every test inside them.

You might see:
```
================ test session starts ================

test_validators.py ......           PASSED
test_object_keys.py ....            PASSED
test_s3_service.py .....            PASSED
test_extractor.py ....              PASSED
test_lambda_handler.py ...          PASSED

================ 22 passed in 1.83s =================
```
That gives you confidence that your recent changes haven't accidentally broken existing functionality.
## Real enterprise workflow

A developer makes a code change:

```
Change code
      ↓
Run pytest
      ↓
All tests pass?
      ↓
Yes
      ↓
Commit
      ↓
Push to GitHub
      ↓
CI/CD runs the same tests again
      ↓
Deploy
```

If a test fails, the code is fixed before deployment.

## Testing time-dependent functions

Functions that use the current time can produce different results during every test run.

Instead of calling `datetime.now()` inside the object-key function, pass the timestamp into the function as an argument.

**Benefits**:
- deterministic tests;
- easier debugging;
- no mocking of the system clock;
- clearer separation of responsibilities.

**Production**:
`datetime.now(timezone.utc)`

**Test**:
a fixed datetime such as `2026-07-30 20:15:45 UTC`

# Metadata Testing

## What is metadata?

Metadata is **data that describes other data**.

When uploading a file to Amazon S3, we can attach additional information that is stored separately from the file contents.

Example:

```
agencies.json

Metadata
--------
source-system = rentflow
source-table = agencies
ingestion-time = 2026-07-30T20:15:45Z
validation-status = passed
```

The JSON file itself remains unchanged, but S3 stores this metadata together with the object.

---
## Why use metadata?

Metadata allows downstream systems to understand a file without reading its contents.

Typical uses include:

- identifying the source system
- identifying the source table
- recording ingestion timestamps
- recording validation status
- recording pipeline version
- recording environment (dev/test/prod)
- enabling lineage and auditing

---
## What are we testing?

The goal is **not** to test Amazon S3.
Amazon already tests its own service.
We are testing that **our application sends the correct metadata** to the AWS SDK.

For example:
```
metadata = {
    "source-system": "rentflow",
    "validation-status": "passed",
}
```

The unit test verifies that this dictionary is passed unchanged to boto3.

---
## Why mock boto3?

Uploading to AWS during every test would:

- require internet access
- require AWS credentials
- create unnecessary cloud operations
- slow down the test suite

Instead, we replace boto3 with a mock object.

The mock records:

- whether `upload_file()` was called
- how many times it was called
- which arguments were supplied

No network traffic occurs.

---
## Example
Application code:

```
service.upload_file(
    source_file=Path("agencies.json"),
    bucket_name="rentflow-data-lake",
    object_key="raw/agencies/file.json",
    metadata={
        "source-system": "rentflow",
        "validation-status": "passed",
    },
)
```

Unit test verifies:

```
fake_s3.upload_file.assert_called_once_with(
    Filename="agencies.json",
    Bucket="rentflow-data-lake",
    Key="raw/agencies/file.json",
    ExtraArgs={
        "ContentType": "application/json",
        "Metadata": {
            "source-system": "rentflow",
            "validation-status": "passed",
        },
    },
)
```

---
## Why is this important?

In enterprise data platforms, metadata is often more valuable than the file itself because it enables:

- **Data Lineage** – Where did this data come from?
- **Data Governance** – Which application produced it?
- **Monitoring** – When was it ingested?
- **Data Quality** – Did validation pass or fail?
- **Auditing** – Which pipeline created this object?

Testing metadata ensures that downstream services such as **AWS Glue**, **Athena**, **Lambda**, or data cataloging tools receive consistent and trustworthy context.

---
## Interview Questions

- What is metadata?
- Why attach metadata to S3 objects instead of storing it inside the file?
- Why should metadata be tested?
- Why mock boto3 instead of uploading to AWS during unit tests?
- What types of metadata would you include in a production data pipeline?

---
## One extra insight (this is the "architect" way of thinking)

Notice how your project is evolving:

```
Application Logic
        │
        ▼
Validation
        │
        ▼
Metadata Generation
        │
        ▼
S3 Upload
        │
        ▼
AWS
```

Each layer has a clear responsibility:

- **Validation** determines whether the data is trustworthy.
- **Metadata generation** describes the data.
- **S3Service** stores the data.
- **boto3** communicates with AWS.

This separation makes the system easier to test, maintain, and extend. It's one of the key characteristics of enterprise-grade software architecture.