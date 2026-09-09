-- ============================================================================
-- AZURE-001: Oracle source schema - CUSTOMER_MASTER
--
-- Represents the customer-master interface an ADF pipeline would encounter
-- when extracting from an on-prem Oracle database in an enterprise
-- financial-services estate (this local container is a plain Oracle
-- instance for development purposes only - it is NOT Exadata; see
-- docs/azure/01_source_systems_overview.md for the distinction).
--
-- CUSTOMER_ID is the cross-source business key. TRANSACTIONS (SQL Server)
-- and CREDIT_EXPOSURE (Teradata) reference it WITHOUT a physical foreign
-- key, because in the real architecture these are three independent
-- source systems. Referential integrity across them is validated later
-- by a Databricks reconciliation job, not by the database engine.
-- ============================================================================

CREATE TABLE CUSTOMER_MASTER (
    CUSTOMER_ID       VARCHAR2(12)  NOT NULL,
    CUSTOMER_NAME     VARCHAR2(120) NOT NULL,
    CUSTOMER_TYPE     VARCHAR2(20)  NOT NULL,
    TAX_ID            VARCHAR2(30),
    COUNTRY_CODE      VARCHAR2(2)   NOT NULL,
    ONBOARDING_DATE   DATE          NOT NULL,
    RISK_RATING       VARCHAR2(10),
    STATUS            VARCHAR2(10)  NOT NULL,
    SOURCE_SYSTEM     VARCHAR2(20)  DEFAULT 'CUSTOMER_MASTER' NOT NULL,
    CREATED_DATE      DATE          DEFAULT SYSDATE NOT NULL,
    UPDATED_DATE      DATE          DEFAULT SYSDATE NOT NULL,
    CONSTRAINT PK_CUSTOMER_MASTER PRIMARY KEY (CUSTOMER_ID),
    CONSTRAINT CK_CUSTOMER_TYPE CHECK (CUSTOMER_TYPE IN ('RETAIL', 'COMMERCIAL', 'PRIVATE_BANKING')),
    CONSTRAINT CK_CUSTOMER_STATUS CHECK (STATUS IN ('ACTIVE', 'INACTIVE', 'CLOSED'))
);

-- Deliberately no CHECK constraint on COUNTRY_CODE against an ISO-3166 list,
-- and no CHECK constraint on RISK_RATING values: these are business-quality
-- rules, not physical constraints, so they belong in a later Databricks/DQ
-- layer - not in the source DDL. This also lets the seed data below insert
-- realistic business-quality defects without violating the schema.

COMMENT ON TABLE CUSTOMER_MASTER IS 'Oracle source: customer master records, keyed by CUSTOMER_ID (cross-source business key)';
COMMENT ON COLUMN CUSTOMER_MASTER.CUSTOMER_ID IS 'Business key shared across CUSTOMER_MASTER, TRANSACTIONS and CREDIT_EXPOSURE - no physical FK across sources';
COMMENT ON COLUMN CUSTOMER_MASTER.UPDATED_DATE IS 'Watermark column for incremental/delta extraction in ADF';

CREATE INDEX IX_CUSTOMER_MASTER_UPDATED ON CUSTOMER_MASTER (UPDATED_DATE);
