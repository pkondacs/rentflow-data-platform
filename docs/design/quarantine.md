# Data Quality and Quarantine

## What is Quarantine?

A quarantine table stores records that fail validation.

Purpose:
- Prevent bad data entering Silver
- Preserve failed records
- Allow investigation

---

## Example
Source:

{  
"id": null,  
"property_id": "property_001"  
}

Result:
Record moved to:
quarantine.scenario_3_null_business_key

---
## Why not simply discard records?

Deleting bad records causes:

- Data loss
- Audit issues
- Difficult debugging
    
Quarantine provides traceability.

---
## Typical Production Flow

Source  
↓  
Validation  
↓  
Valid Records → Bronze/Silver  
↓  
Invalid Records → Quarantine

---
## Typical Monitoring

**Metrics**:
- Records received
- Records processed
- Records quarantined
- Failure rate

Alerts:
- Quarantine rate > 5%
- Missing business keys
- Unexpected schema changes

---
## Interview Answer

When records fail validation, I prefer routing them to quarantine tables rather than deleting them.

This preserves traceability, supports root-cause analysis, and allows the main pipeline to continue processing valid records.

