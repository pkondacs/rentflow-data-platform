# Schema Evolution

## Safe Changes

Examples:
- New nullable column
- Additional nested field
    

Example:

Before
    id  
    monthly_rent

After
    id  
    monthly_rent  
    currency

Supported by:

mergeSchema=true
---

## Breaking Changes

Examples:

- Column rename
- Column removal
- Data type change

Before
    monthly_rent

After
    rent_amount

These changes usually require migration logic.

---

## Delta Lake

Without mergeSchema:
Write fails.

With mergeSchema:
New columns automatically added to Delta table.

---

## Architect View

Not every source change should be accepted automatically.
Production systems often require:

Dev Review  
↓  
Testing  
↓  
Approval  
↓  
Promotion to Production