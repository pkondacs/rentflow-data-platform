-- ============================================================================
-- AZURE-001: Teradata source schema - CREDIT_EXPOSURE
--
-- Represents an enterprise data warehouse credit-risk feed on Teradata, a
-- common source for exposure/limit data in financial-services estates.
--
-- NOTE: no live/containerized Teradata instance is provided as part of
-- this repository. This DDL and its seed data are provided for schema
-- and reconciliation design review, and to document the target ADF
-- ingestion pattern. See docs/azure/03_local_dev_setup.md for details
-- and what it would take to run this against a real Teradata instance
-- later.
--
-- CUSTOMER_ID is the cross-source business key (see the Oracle
-- CUSTOMER_MASTER schema). There is no foreign key back to
-- CUSTOMER_MASTER: these are independent source systems, and an
-- orphaned CUSTOMER_ID here is an expected scenario for the later
-- Databricks referential-integrity check to detect.
-- ============================================================================

CREATE TABLE CREDIT_EXPOSURE (
    EXPOSURE_ID           VARCHAR(20)   CHARACTER SET LATIN NOT NULL,
    CUSTOMER_ID            VARCHAR(12)   CHARACTER SET LATIN NOT NULL,  -- business key, no physical FK (cross-source)
    FACILITY_TYPE           VARCHAR(20)   CHARACTER SET LATIN NOT NULL,
    EXPOSURE_AMOUNT         DECIMAL(18,2) NOT NULL,                      -- reconciliation field
    CURRENCY_CODE            CHAR(3)       CHARACTER SET LATIN NOT NULL,
    LIMIT_AMOUNT             DECIMAL(18,2) NOT NULL,
    UTILIZATION_PCT          DECIMAL(7,2)  NOT NULL,
    RISK_GRADE               VARCHAR(10)   CHARACTER SET LATIN,
    AS_OF_DATE                DATE          NOT NULL,
    SOURCE_SYSTEM             VARCHAR(20)   CHARACTER SET LATIN NOT NULL DEFAULT 'CREDIT_EXPOSURE',
    CREATED_TIMESTAMP         TIMESTAMP(0)  NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    UPDATED_TIMESTAMP         TIMESTAMP(0)  NOT NULL DEFAULT CURRENT_TIMESTAMP(0)
)
UNIQUE PRIMARY INDEX (EXPOSURE_ID);

-- Deliberately no CHECK constraint on UTILIZATION_PCT (expected 0-100) or
-- on LIMIT_AMOUNT sign, and no reference check against CUSTOMER_MASTER:
-- those are business-quality rules for a later DQ layer, not physical
-- constraints on this source table.

COMMENT ON TABLE CREDIT_EXPOSURE IS 'Teradata source: credit exposure / facility records, keyed by EXPOSURE_ID, referencing CUSTOMER_ID as a cross-source business key';
COMMENT ON COLUMN CREDIT_EXPOSURE.UPDATED_TIMESTAMP AS 'Watermark column for incremental/delta extraction in ADF';
