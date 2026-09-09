# Target ADF Architecture - AZURE-001

## Scope

AZURE-001 covers ingestion only: three source systems landing raw,
as-extracted data into ADLS Gen2. It explicitly does **not** cover
Bronze/Silver/Gold modeling, data-quality rule execution, or
cross-source referential-integrity checks - those are later phases,
implemented in Databricks/PySpark, and are out of scope here.

```
Oracle CUSTOMER_MASTER   ─┐
SQL Server TRANSACTIONS  ─┼─► Azure Data Factory ─► ADLS Gen2 (raw zone)
Teradata CREDIT_EXPOSURE ─┘
```

## ADF components (built later, via ADF Studio + Git integration)

The `adf/` folder at the repo root is reserved as the Git integration root
for the actual Data Factory instance. Nothing in it is hand-written -
see [adf/README.md](../../adf/README.md). This section documents the
design those artifacts are expected to implement:

- **Linked services** - one per source (Oracle, SQL Server, Teradata) plus
  one for the ADLS Gen2 raw zone. On-prem/containerized sources require a
  **self-hosted integration runtime** (SHIR) rather than the Azure IR,
  since ADF cannot reach a local Docker container or an on-prem database
  directly - this mirrors how an enterprise would connect to real
  on-prem Oracle/SQL Server/Teradata systems.
- **Datasets** - one per source table (`CUSTOMER_MASTER`, `TRANSACTIONS`,
  `CREDIT_EXPOSURE`), plus a parameterized sink dataset for the raw zone.
- **Pipelines** - one Copy Activity pipeline per source, parameterized by
  table name and load date so the same pattern extends to additional
  tables without duplicating pipelines.
- **Triggers** - schedule or tumbling-window triggers per pipeline once a
  cadence is defined; not required to demonstrate the ingestion pattern
  itself.

## Raw zone landing convention

```
raw/
  oracle/customer_master/ingest_date=YYYY-MM-DD/*.parquet
  sqlserver/transactions/ingest_date=YYYY-MM-DD/*.parquet
  teradata/credit_exposure/ingest_date=YYYY-MM-DD/*.parquet
```

- Partitioned by source system, table, and ingestion date so each run is
  independently addressable and replayable.
- Written as extracted, without transformation - schema and business-rule
  validation happen downstream in Bronze/Silver (future phase).

## Incremental loading / watermarks

Every source table carries an `UPDATED_DATE` / `UPDATED_TIMESTAMP` column
(added specifically for this purpose) so a later pipeline iteration can
demonstrate watermark-based incremental extraction instead of a full
reload per run. AZURE-001 does not implement the watermark lookup itself -
it only ensures the column exists and is populated realistically in the
seed data.

## Reconciliation-ready fields

To support later source-to-target reconciliation (also a future phase,
not implemented in AZURE-001), each source carries fields a reconciliation
job would compare between source and raw zone:

- **Amounts**: `TRANSACTIONS.AMOUNT`, `CREDIT_EXPOSURE.EXPOSURE_AMOUNT` /
  `LIMIT_AMOUNT` - summable fields for source-vs-landed total checks.
- **Record counts**: implicit - a reconciliation job counts rows per
  source/table/ingest_date and compares source count to landed count.
- **Timestamps/watermarks**: `UPDATED_DATE` / `UPDATED_TIMESTAMP` on every
  table, usable both for incremental extraction and for verifying that
  landed data reflects the expected as-of point in time.

## Explicitly out of scope for AZURE-001

- Bronze/Silver/Gold Databricks processing
- Data-quality rule execution against the seeded defects
- Cross-source referential-integrity checks (Oracle/SQL Server/Teradata
  via shared `CUSTOMER_ID`)
- Any real ADF pipeline/dataset/linkedService JSON (populated later by
  ADF Git integration, not hand-crafted)
