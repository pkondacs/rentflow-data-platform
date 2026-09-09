-- ============================================================================
-- AZURE-001: SQL Server source schema - TRANSACTIONS
--
-- Represents an on-prem SQL Server transactional system in an enterprise
-- financial-services estate.
--
-- CUSTOMER_ID is the cross-source business key (see the Oracle
-- CUSTOMER_MASTER schema). There is NO foreign key back to
-- CUSTOMER_MASTER here, because these are two independent source
-- systems in the real architecture - a customer_id in TRANSACTIONS with
-- no matching row in CUSTOMER_MASTER is a legitimate, expected scenario
-- that a later Databricks referential-integrity check is designed to
-- surface, not something the database engine can prevent.
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM sys.databases WHERE name = 'azure_learning')
BEGIN
    CREATE DATABASE azure_learning;
END
GO

USE azure_learning;
GO

IF OBJECT_ID('dbo.TRANSACTIONS', 'U') IS NOT NULL
    DROP TABLE dbo.TRANSACTIONS;
GO

CREATE TABLE dbo.TRANSACTIONS (
    TRANSACTION_ID      BIGINT IDENTITY(1,1) NOT NULL,
    CUSTOMER_ID          VARCHAR(12)   NOT NULL,   -- business key, no physical FK (cross-source)
    ACCOUNT_ID            VARCHAR(20)   NOT NULL,
    TRANSACTION_DATE     DATETIME2(0)  NOT NULL,
    TRANSACTION_TYPE     VARCHAR(20)   NOT NULL,
    AMOUNT                DECIMAL(18,2) NOT NULL,   -- reconciliation field; signed, zero permitted (fees/reversals)
    CURRENCY_CODE         CHAR(3)       NOT NULL,
    CHANNEL               VARCHAR(20)   NOT NULL,
    STATUS                VARCHAR(20)   NOT NULL,
    SOURCE_SYSTEM         VARCHAR(20)   NOT NULL CONSTRAINT DF_TRANSACTIONS_SOURCE DEFAULT ('TRANSACTIONS'),
    CREATED_TIMESTAMP     DATETIME2(0)  NOT NULL CONSTRAINT DF_TRANSACTIONS_CREATED DEFAULT (SYSUTCDATETIME()),
    UPDATED_TIMESTAMP     DATETIME2(0)  NOT NULL CONSTRAINT DF_TRANSACTIONS_UPDATED DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT PK_TRANSACTIONS PRIMARY KEY (TRANSACTION_ID),
    CONSTRAINT CK_TRANSACTION_TYPE CHECK (TRANSACTION_TYPE IN ('DEBIT', 'CREDIT', 'TRANSFER', 'FEE', 'REVERSAL')),
    CONSTRAINT CK_TRANSACTION_CHANNEL CHECK (CHANNEL IN ('BRANCH', 'ONLINE', 'MOBILE', 'ATM', 'CALL_CENTER')),
    CONSTRAINT CK_TRANSACTION_STATUS CHECK (STATUS IN ('POSTED', 'PENDING', 'REVERSED', 'FAILED'))
);
GO

-- Deliberately no CHECK constraint on AMOUNT sign and no CHECK/FK against
-- a currency or customer reference list: those are business-quality rules
-- for the DQ layer, not physical constraints on this source table.

CREATE INDEX IX_TRANSACTIONS_CUSTOMER_ID ON dbo.TRANSACTIONS (CUSTOMER_ID);
CREATE INDEX IX_TRANSACTIONS_UPDATED ON dbo.TRANSACTIONS (UPDATED_TIMESTAMP);
GO
