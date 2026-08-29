## Initial approach
The first extraction uses the Supabase Python API rather than a direct
PostgreSQL connection.

**Flow**:
Supabase API
→ Python extractor
→ local JSON snapshot
→ validation
→ Amazon S3
## Security
- Secrets are stored in `.env`.
- `.env` is excluded from Git.
- Extracted operational data is also excluded from Git.
- Extraction should use read-only permissions.
- Highly privileged keys should not be used unless explicitly required.
## Important limitation

Supabase API queries return a limited number of rows by default.
Larger tables require pagination using range-based queries.

## RentFlow export architecture

The AWS pipeline does not authenticate through a personal Google or Supabase user account. 

**Flow:** 
Python / AWS Lambda 
→ `x-api-key`
→ Supabase `data-export` Edge Function 
→ service-role database access
→ sanitized JSON response 
→ S3 raw zone 

**Benefits:** 
- No interactive login. 
- Suitable for scheduled pipelines. 
- Row-Level Security is not weakened. 
- The service-role key stays server-side. 
- Exported tables and columns are explicitly allow-listed. 
- Sensitive fields can be removed or masked before leaving Supabase. 

The export API supports incremental loading: 
`?updated_after=<ISO-8601 timestamp>&limit=1000`