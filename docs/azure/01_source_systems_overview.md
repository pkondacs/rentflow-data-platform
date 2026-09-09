# Source Systems Overview - AZURE-001

Three source systems feed the ADF ingestion foundation. Each represents a
system type commonly found in an enterprise financial-services data
estate, and each is keyed to the others through the shared business key
`CUSTOMER_ID` (no physical foreign key exists across them - see
[02_target_architecture.md](02_target_architecture.md)).

## Oracle - `CUSTOMER_MASTER`

Represents the customer-master interface an ADF pipeline would encounter
when extracting from an on-prem Oracle database in an enterprise estate.

**This local development environment is a plain Oracle instance
(`gvenzl/oracle-free`, a standard Oracle Database Free container) - it is
NOT Exadata, and this documentation makes no claim otherwise.** It exists
to give ADF something real to connect to (via JDBC/Oracle connector,
self-hosted integration runtime) and to exercise the same SQL/DDL surface
an ADF pipeline would see against Oracle in production.

In a real Exadata-backed estate, the same logical table would sit behind
additional Exadata-specific characteristics that don't apply to this local
container - e.g. Smart Scan / storage-cell offload, Hybrid Columnar
Compression, and InfiniBand-backed storage networking. None of those
affect how ADF connects (it still talks Oracle SQL over a JDBC-style
driver through a self-hosted IR); they matter for source-side performance
tuning, not for the pipeline design covered by AZURE-001.

Table: `CUSTOMER_MASTER` - one row per customer, `CUSTOMER_ID` primary key.

## SQL Server - `TRANSACTIONS`

Represents an on-prem SQL Server OLTP system recording customer
transactions (payments, transfers, fees). Common in FS estates as the
system of record for day-to-day account activity.

Table: `TRANSACTIONS` - one row per transaction, surrogate `TRANSACTION_ID`
primary key, `CUSTOMER_ID` as a business-key reference (no physical FK).

## Teradata - `CREDIT_EXPOSURE`

Represents an enterprise data warehouse credit-risk feed, a common
Teradata use case in banks for aggregated exposure and limit reporting.

**No live or containerized Teradata instance is provided in this
repository.** The DDL and seed data exist to document the schema,
reconciliation fields, and target ADF ingestion pattern; they have not
been run against a live Teradata engine. If a real Teradata
instance (e.g. Vantage Express) is stood up later, this repository does
not currently claim that has happened - see
[03_local_dev_setup.md](03_local_dev_setup.md).

Table: `CREDIT_EXPOSURE` - one row per exposure/facility, `EXPOSURE_ID`
primary index, `CUSTOMER_ID` as a business-key reference (no physical FK).

## Why no physical foreign keys across sources

`CUSTOMER_MASTER`, `TRANSACTIONS`, and `CREDIT_EXPOSURE` are three
independent source systems in the target architecture - exactly as they
would be in a real enterprise estate, where Oracle, SQL Server, and
Teradata do not share a database engine and cannot enforce a cross-engine
foreign key. Rows in `TRANSACTIONS` or `CREDIT_EXPOSURE` that reference a
`CUSTOMER_ID` absent from `CUSTOMER_MASTER` are therefore expected and
present in the seed data by design - they are exactly what a later
Databricks-based referential-integrity check (not part of AZURE-001) is
meant to detect once all three sources land in ADLS Gen2 raw.

## Deliberate data-quality defects

Each source's seed data (`azure/sources/<system>/<table>/02_seed_data.sql`)
includes a small, labeled set of business-quality defects - values that
violate no physical database constraint (no duplicate/NULL primary keys)
but that a real source system does produce and that a later DQ layer is
expected to catch: invalid country/currency codes, future dates, blank
values, out-of-range percentages, and cross-source orphaned
`CUSTOMER_ID` values. Each defect row is marked with a `-- DQ TEST CASE`
comment explaining what it exercises.
