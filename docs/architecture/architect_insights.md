# Architect Insight

The most important architecture decision is not the transport mechanism.

The important architecture is:

Source
    ↓
Landing
    ↓
Bronze
    ↓
Silver
    ↓
Gold

The ingestion layer can evolve over time:

Version 1:
API → JSON Landing → Databricks

Version 2:
API → Databricks

Version 3:
CDC → Streaming → Databricks

The lakehouse architecture remains stable.


## Topic
Unity Catalog Governance
## Problem
How to separate domain ownership in Databricks while keeping centralized governance.
## What I learned
- One metastore can support multiple workspaces
- Catalogs are strong domain boundaries
- Bronze ownership should remain platform-controlled
## Architecture insight
Governance is more important than pure performance in banking environments.
## Real-world application
In my rental platform:
- separate finance data from operational data
- restrict raw access
- expose curated Gold datasets
## Open questions
- How to implement row-level security efficiently?
- Best Terraform setup for Unity Catalog permissions?



## Milestone
Completed first end-to-end Bronze ingestion pipeline for RentFlowEU.
## Architecture

RentFlowEU (Lovable Cloud)
    ↓
Export API
    ↓
Local Python Extraction
    ↓
JSON Landing Files
    ↓
Databricks Volume
    ↓
Bronze Delta Tables

## Bronze Tables Created

- bronze.agencies_raw
- bronze.properties_raw
- bronze.rental_units_raw
- bronze.tenants_raw
- bronze.invitations_raw
- bronze.tenancies_raw
- bronze.email_send_log_raw

## Key Learning

Operational systems should remain isolated from analytical workloads.
Bronze tables should preserve source fidelity and remain as close as possible to the source data.

## Future Improvements

- Incremental ingestion
- Audit logging
- Data quality checks
- CI/CD deployment

---

# Topic
Schema Enforcement and Schema Evolution
## Goal

Understand how Databricks handles invalid source data and source schema changes.
## Notebook

05_schema_evolution_merge_schema.py
## Scenarios Implemented

### Scenario 1: Missing Mandatory Column

Source record missing:
property_id

Result:
- Validation failure
- Record quarantined

Lesson:  
Business keys should be validated during ingestion.

---
### Scenario 2: Wrong Data Type

Source:
monthly_rent = "seven hundred"

Result:
- try_cast() converts invalid value to NULL
- Validation detects NULL
- Record quarantined

Lesson:  
Schema enforcement prevents malformed data entering downstream layers.

---
### Scenario 3: Null Business Key

Source:
id = NULL

Result:
- Validation failure
- Record quarantined

Lesson:  
Schema validity and business validity are different concepts.

---
### Scenario 4: New Column Appears

Source:
currency

New column added.
Result:
- Standard write fails
- mergeSchema=true succeeds

Lesson:  
Schema evolution allows controlled introduction of new attributes.

---
## Key Insight

Schema Enforcement  ≠ Schema Evolution
Schema Enforcement protects quality.
Schema Evolution manages source changes.


# Bronze Layer Design

## Purpose

Store source data with minimal transformation.

## Rules

- Preserve source structure
- Keep source identifiers
- Add ingestion metadata
- Do not apply business logic
- Do not remove duplicates

## Metadata Added

- _source_system
- _source_table
- _ingested_at

## Source

RentFlowEU API exports

## Benefits

- Traceability
- Reproducibility
- Auditing
- Easier troubleshooting