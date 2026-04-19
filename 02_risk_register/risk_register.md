# Risk Register — Anodot Third-Party Risk Assessment
**Client:** Rockstar Games  
**Vendor:** Anodot  
**Assessment Date:** 4/14/2026  
**Assessed By:** Irvens Eristil  
**Framework:** ISO 27001:2022

---

## Scoring Methodology

**Likelihood:** 1 (Rare) → 5 (Almost Certain)  
**Impact:** 1 (Negligible) → 5 (Catastrophic)  
**Risk Score = Likelihood × Impact**

| Score | Rating |
|-------|--------|
| 1–4 | Low |
| 5–9 | Medium |
| 10–14 | High |
| 15–25 | Critical |

---

## Risk Register

| Risk ID | Risk Description | Likelihood | Impact | Score | Rating | Treatment | Owner |
|---------|-----------------|-----------|--------|-------|--------|-----------|-------|
| R-001 | Long-lived tokens stolen and reused for persistent access | 4 | 5 | 20 | Critical | Enforce short-lived OAuth 2.0 tokens with 24hr expiry | InfoSec |
| R-002 | No breach notification SLA allows silent compromise for days | 4 | 5 | 20 | Critical | Add 24hr notification clause to vendor contract | Legal/GRC |
| R-003 | Over-permissioned warehouse access expands blast radius | 3 | 5 | 15 | Critical | Enforce least-privilege schema-level access only | Cloud Security |
| R-004 | No anomaly detection on Snowflake query behavior | 4 | 4 | 16 | Critical | Deploy behavioral monitoring on query volume and timing | SOC |
| R-005 | Connector downtime not visible to Rockstar | 3 | 3 | 9 | Medium | Implement shared health monitoring dashboard | Engineering |
| R-006 | No token rotation policy enforced contractually | 4 | 4 | 16 | Critical | Require 90-day maximum rotation in contract | GRC |
| R-007 | Vendor sub-processor security not assessed | 3 | 4 | 12 | High | Require annual sub-processor disclosure and assessment | GRC |
| R-008 | No MFA on service accounts used for Snowflake integration | 3 | 5 | 15 | Critical | Require MFA on all service accounts with production access | IAM |

---

## Risk Summary

| Rating | Count |
|--------|-------|
| Critical | 6 |
| High | 1 |
| Medium | 1 |
| Low | 0 |

**Overall Vendor Risk Rating: CRITICAL**

---

## Treatment Definitions

- **Mitigate** — Implement controls to reduce likelihood or impact
- **Accept** — Document and monitor risk within tolerance
- **Transfer** — Shift risk via contract, insurance, or SLA
- **Avoid** — Eliminate the activity that creates the risk