# Silver Layer Design

## Purpose

The Silver layer contains cleaned, standardized and validated datasets derived from Bronze.

## tenants

Source:

* bronze.tenants_raw

Target:

* silver.tenants_clean

Rules:

* Trim whitespace
* Standardize email casing
* Remove duplicate emails
* Validate mandatory fields

---

## properties

Source:

* bronze.properties_raw

Target:

* silver.properties_clean

Rules:

* Validate property identifiers
* Validate mandatory fields
* Standardize text columns

---

## rental_units

Source:

* bronze.rental_units_raw

Target:

* silver.rental_units_clean

Rules:

* Validate rent > 0
* Validate property references
* Standardize data types

---

## invitations

Source:

* bronze.invitations_raw

Target:

* silver.invitations_clean

Rules:

* Validate status values
* Remove invalid records
* Derive invitation age metrics

---

## tenancies

Source:

* bronze.tenancies_raw

Target:

* silver.tenancies_clean

Rules:

* Validate tenancy dates
* Validate tenant references
* Validate rental unit references

---

## email_send_log

Source:

* bronze.email_send_log_raw

Target:

* silver.email_send_log_clean

Rules:

* Validate timestamps
* Validate recipient fields
* Standardize status values
