# Local Azure source containers

Spins up local Oracle and SQL Server instances for AZURE-001 development.
Teradata is not included - see [docs/azure/03_local_dev_setup.md](../../docs/azure/03_local_dev_setup.md).

## Setup

1. Copy `.env.example` to `.env` at the repo root (if you haven't already) and fill in
   `ORACLE_PASSWORD`, `ORACLE_APP_USER`, `ORACLE_APP_USER_PASSWORD`, `MSSQL_SA_PASSWORD`
   with your own local-only values. Never commit `.env`.
2. From this folder, run:
   ```powershell
   docker compose --env-file ../../.env up -d
   ```
3. Oracle runs `CUSTOMER_MASTER`'s `01_create_schema.sql` / `02_seed_data.sql` automatically
   on first startup (via `gvenzl/oracle-free`'s init-script convention).
4. SQL Server has no built-in init-script mechanism, so a one-shot `sqlserver-init`
   container runs `TRANSACTIONS`'s schema + seed scripts once SQL Server reports healthy.

Check progress with `docker compose logs -f oracle sqlserver-init`.

## Teardown

```powershell
docker compose --env-file ../../.env down
```

Add `-v` to also drop the named volumes (`oracle_data`, `sqlserver_data`) and start clean next time.
