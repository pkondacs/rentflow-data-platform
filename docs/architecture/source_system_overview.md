# Source System Inventory — RentFlowEU
## Source system
RentFlowEU / Loveable application

## Current exported entities
- agencies
- properties
- rental_units
- tenants
- invitations
- tenancies
- email_send_log

## Key relationships
- agencies.id → properties.agency_id
- agencies.id → tenants.agency_id
- agencies.id → invitations.agency_id
- properties.id → rental_units.property_id
- rental_units.id → invitations.rental_unit_id

## Observations
- tenancies is currently empty
- email_send_log is currently empty
- invitations exist before confirmed tenancies
- tenants may contain duplicate emails / repeated invitations

## Architecture questions
- Should tenants be deduplicated by email?
- When does an invitation become a tenancy?
- Should invitation tokens be excluded from analytics for security?
- Should personal data be masked in Silver/Gold layers?

# Current Source Tables

## agencies
Rental agencies

## properties
Physical properties

## rental_units
Individual rentable units

## tenants
Tenant records

## invitations
Tenant onboarding invitations

## tenancies
Active tenancy contracts

## email_send_log
Email audit trail

## Relationships

agencies
    ↓
properties
    ↓
rental_units

agencies
    ↓
tenants

rental_units
    ↓
invitations