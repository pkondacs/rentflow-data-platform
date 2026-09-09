# Local Development Setup - AZURE-001

## Oracle and SQL Server (containerized)

Both run via `azure/docker/docker-compose.yml`. See
[azure/docker/README.md](../../azure/docker/README.md) for the exact
commands. Summary:

- **Oracle** uses `gvenzl/oracle-free` (Oracle Database Free, a standard
  community-maintained container image) - a plain Oracle instance for
  development, explicitly **not** Exadata (see
  [01_source_systems_overview.md](01_source_systems_overview.md)). It
  auto-runs `azure/sources/oracle/customer_master/01_create_schema.sql`
  and `02_seed_data.sql` on first startup.
- **SQL Server** uses the official `mcr.microsoft.com/mssql/server`
  image. Since that image has no built-in "run these .sql files on
  startup" mechanism, a one-shot `sqlserver-init` container runs
  `azure/sources/sqlserver/transactions/01_create_schema.sql` and
  `02_seed_data.sql` via `sqlcmd` once SQL Server reports healthy.

Credentials for both come from environment variables defined in `.env`
(never committed - see `.env.example` at the repo root for the required
placeholder keys).

## Teradata (not containerized)

No live or containerized Teradata instance is provided. Teradata's only
practical local option, Vantage Express, ships as a multi-GB VM appliance
(VMware/VirtualBox), not a lightweight Docker container, which makes it
impractical to include in this repository's local dev setup.

What exists instead:

- `azure/sources/teradata/credit_exposure/01_create_schema.sql` and
  `02_seed_data.sql` - valid Teradata SQL, written and reviewed for
  correctness, but **not executed against a live Teradata engine** as
  part of this repository.
- `docs/azure/01_source_systems_overview.md` and
  `02_target_architecture.md` - document how Teradata fits into the
  ingestion design.

If a real Teradata instance becomes available later (e.g. a Vantage
Express VM, a sandbox, or a licensed enterprise environment), this
document should be updated to state that explicitly, and the scripts
should be validated against it. Until then, no claim is made that a
Teradata runtime has been exercised.

## Running the setup

```powershell
cd azure\docker
copy ..\..\.env.example ..\..\.env   # then fill in real local-only values
docker compose --env-file ..\..\.env up -d
docker compose logs -f oracle sqlserver-init
```

Connect with any Oracle/SQL Server client using the ports and credentials
in your local `.env`. Teradata scripts can be reviewed as SQL text or run
manually against a Teradata instance if one is available.
