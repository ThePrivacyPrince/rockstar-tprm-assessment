# Vendor Security Assessment Questionnaire
**Vendor:** Anodot  
**Client:** Rockstar Games  
**Assessment Date:** 4/14/2026  
**Assessed By:** Irvens Eristil  
**Framework:** ISO 27001:2022 | NIST SP 800-161

---

## How to Use This SAQ

Send this questionnaire to the vendor before onboarding or during 
annual reassessment. For each question the vendor should provide:

- **Answer:** Yes / Partial / No / N/A
- **Evidence:** Documentation, screenshots, or policy references
- **Notes:** Any context or planned remediation

A "No" answer on any Critical question triggers an automatic finding 
in the risk register and requires escalation before access is granted.

## Critical Questions
*A "No" on any of these is an automatic Critical finding — escalate immediately*

| ID | Question | Breach Relevance |
|----|----------|-----------------|
| 1.1 | Are authentication tokens short-lived under 24 hours? | Root cause of attacker persistence after theft |
| 1.2 | Is OAuth 2.0 or equivalent used for all service-to-service auth? | Static tokens enabled silent lateral movement |
| 1.6 | Are tokens scoped to least-privilege access only? | Warehouse-wide access caused mass exfiltration |
| 2.2 | What is your breach notification SLA? | No SLA caused 7-day blind spot for Rockstar |
| 3.1 | Is warehouse access scoped to minimum schemas only? | Unrestricted access maximized blast radius |
| 4.5 | Do you log all security events? | No logging enabled 10 days of silent exfiltration |
| 5.1 | Do you have an incident response team? | No IR team caused critical notification delay |
| 5.2 | Have you tested your incident response process? | Untested IR broke down under real conditions |

## Section 1 — Authentication and Token Management

| ID | Question | Answer | Evidence | Notes |
|----|----------|--------|----------|-------|
| 1.1 | Are authentication tokens short-lived under 24 hours? | | | |
| 1.2 | Is OAuth 2.0 or equivalent used for all service-to-service authentication? | | | |
| 1.3 | Are service account tokens rotated on a schedule of 90 days or less? | | | |
| 1.4 | Are authentication tokens stored in a secrets manager? | | | |
| 1.5 | Is MFA enforced on all service accounts with production data access? | | | |
| 1.6 | Are tokens scoped to least-privilege access only? | | | |
| 1.7 | Is there automated alerting when tokens are used outside normal patterns? | | | |

## Section 2 — Incident Detection and Notification

| ID | Question | Answer | Evidence | Notes |
|----|----------|--------|----------|-------|
| 2.1 | Do you have a documented IR plan for third-party integration breaches? | | | |
| 2.2 | What is your contractual SLA for notifying customers of a security incident? | | | |
| 2.3 | Do you have SIEM or anomaly detection covering your integration pipeline? | | | |
| 2.4 | How do you detect unauthorized use of authentication tokens? | | | |
| 2.5 | Are customers notified when connector services go offline unexpectedly? | | | |

## Section 3 — Access Control and Least Privilege

| ID | Question | Answer | Evidence | Notes |
|----|----------|--------|----------|-------|
| 3.1 | Is access to customer data warehouses scoped to minimum schemas only? | | | |
| 3.2 | Are privileged access reviews conducted quarterly? | | | |
| 3.3 | Is network access for integrations restricted by IP allowlist? | | | |
| 3.4 | Are read and write permissions separated for analytics vs operational access? | | | |
| 3.5 | Do you log all queries made to connected customer data environments? | | | |

## Section 4 — Supply Chain and Sub-Processors

| ID | Question | Answer | Evidence | Notes |
|----|----------|--------|----------|-------|
| 4.1 | Do you maintain an inventory of sub-processors with access to customer data? | | | |
| 4.2 | Are sub-processors subject to the same security requirements as your platform? | | | |
| 4.3 | Do you conduct annual security assessments of sub-processors? | | | |
| 4.4 | Do you hold a current SOC 2 Type II or ISO 27001 certification? | | | |
| 4.5 | Do you log security events across your infrastructure? | | | |
| 4.15 | Do you employ a third party to test your infrastructure security? | | | |

## Section 5 — Incident Response and Business Continuity

| ID | Question | Answer | Evidence | Notes |
|----|----------|--------|----------|-------|
| 5.1 | Do you have an incident response team? | | | |
| 5.2 | Have you tested your incident response process? | | | |
| 5.3 | Do you have a business continuity plan? | | | |
| 5.5 | Do you have a process to remediate new risks? | | | |

## SAQ Scoring Summary

| Section | Total Questions | Critical Questions |
|---------|----------------|-------------------|
| 1 — Authentication | 7 | 3 |
| 2 — Detection and Notification | 5 | 2 |
| 3 — Access Control | 5 | 1 |
| 4 — Supply Chain | 6 | 1 |
| 5 — Incident Response | 4 | 2 |
| **Total** | **27** | **9** |

## Assessor Notes

This SAQ was developed specifically around the attack vector used in 
the April 2026 Rockstar Games / Anodot breach. The critical questions 
in this document are the exact questions that would have identified 
Anodot's risk posture before the breach occurred. Any vendor holding 
privileged access to production data infrastructure should complete 
this questionnaire at onboarding and annually thereafter.