# Incident Postmortem — Rockstar Games / Anodot Breach
**Date of Incident:** April 14, 2026  
**Threat Actor:** ShinyHunters  
**Attack Vector:** Third-party SaaS vendor (Anodot) → Snowflake  
**Records Leaked:** 78.6 million  
**Assessed By:** Irvens Eristil 
**Framework:** ISO 27001:2022

---

## What Happened

Rockstar Games was not hacked directly. A vendor was.

Anodot is a cloud cost monitoring and analytics SaaS platform which held 
privileged authentication tokens that connected directly to Rockstar's 
Snowflake data warehouse. ShinyHunters compromised Anodot's systems, 
extracted those tokens, and used them to impersonate a legitimate 
internal service. Once inside Snowflake, they operated silently for 
10 days using normal database operations that looked like authorized 
activity. No Snowflake vulnerability was exploited. The tokens were 
enough.

---

## Attack Chain
ShinyHunters
↓
Compromised Anodot infrastructure
↓
Extracted long-lived authentication tokens
↓
Impersonated Anodot as trusted internal service
↓
Accessed Rockstar's Snowflake data warehouse
↓
Exfiltrated 78.6M records using normal query operations
↓
Operated undetected for 10 days
↓
Posted ransom demand on dark web — April 11, 2026
↓
Rockstar declined to pay
↓
Data published — April 14, 2026

---

## Incident Timeline

| Date | Event | TPRM Failure |
|------|-------|-------------|
| Pre-breach | Anodot onboarded with warehouse-wide Snowflake access | No vendor tiering or access scoping performed |
| Pre-breach | Long-lived static tokens provisioned for Anodot | No token rotation policy or expiry enforced |
| Pre-breach | No breach notification SLA in Anodot contract | Contractual gap left Rockstar blind to vendor incidents |
| April 4 | Anodot connectors go offline across regions | Rockstar not notified — no monitoring SLA existed |
| April 4–11 | Silent compromise underway | No anomaly detection on Snowflake query behavior |
| April 11 | ShinyHunters posts dark web ransom demand | Rockstar learns of breach from attackers not from Anodot |
| April 14 | Ransom deadline passes. 78.6M records published | No IR playbook for third-party integration breach |


## Root Cause Analysis

### Root Cause 1 — Token Hygiene Failure
Anodot held long-lived static authentication tokens with no expiry 
and no rotation policy. When those tokens were stolen, attackers had 
persistent trusted access with no time limit. Short-lived OAuth 2.0 
tokens rotating every 24 hours would have made the stolen credentials 
worthless within one day.

**ISO 27001 Control Failed:** A.8.5 — Secure Authentication


### Root Cause 2 — Over-Permissioned Access
Anodot required access to specific cost-monitoring schemas. Instead 
it was granted warehouse wide access. When the tokens were stolen, 
attackers had access to everything — not just what Anodot needed to 
do its job. Least privilege scoping limits blast radius when a vendor 
is compromised.

**ISO 27001 Control Failed:** A.8.3 — Information Access Restriction


### Root Cause 3 — No Breach Notification SLA
Anodot's connectors went offline April 4. Rockstar found out April 11 
from a dark web post. That is a 7-day blind spot created entirely by 
the absence of a contractual notification requirement. A 24 hour 
notification SLA in the vendor agreement closes this gap.

**ISO 27001 Control Failed:** A.5.20 — Addressing Security Within 
Supplier Agreements


### Root Cause 4 — No Continuous Monitoring
Rockstar had no visibility into Anodot's health or Snowflake query 
behavior in real time. Monitoring for anomalous query patterns — 
off-hours access, volume spikes, unusual schema queries — would have 
flagged this on Day 1.

**ISO 27001 Control Failed:** A.8.16 — Monitoring Activities


### Root Cause 5 — No Vendor Security Assessment
Anodot was never formally assessed as a third-party vendor despite 
holding critical privileged access to production data infrastructure. 
A TPRM assessment using the SAQ in this project would have identified 
all four root causes above before a single token was stolen.

**ISO 27001 Control Failed:** A.5.19 — Information Security in 
Supplier Relationships


## What Would Have Prevented This

| Control | Action | Outcome |
|---------|--------|---------|
| Token rotation | Short-lived OAuth 2.0 tokens — 24hr expiry | Stolen tokens worthless within one day |
| Least privilege | Schema-level access only | Blast radius limited to cost data only |
| Notification SLA | 24hr contractual breach notification | Rockstar alerted April 4 not April 11 |
| Anomaly detection | Snowflake query monitoring | Silent exfiltration flagged Day 1 |
| Vendor assessment | SAQ completed at onboarding | All risks identified before breach |


## Lessons for TPRM Programs

1. **Your attack surface includes every vendor with privileged access.**
   The question is not just "are our systems secure" but "are the 
   systems of everyone connected to us secure."

2. **Token hygiene is not optional for SaaS integrations.**
   Any vendor holding long lived credentials to your production 
   environment is a liability. Treat it like one.

3. **Silence from a vendor is not the same as safety.**
   Without a notification SLA you will find out about a vendor breach 
   the same way Rockstar did, from the attacker.

4. **Monitoring your own systems is not enough.**
   You need visibility into what your vendors are doing inside your 
   environment. Anomaly detection on third-party query behavior is 
   not optional.

5. **Onboarding is the best time to assess.**
   Every vendor with privileged access should complete a security 
   assessment before they receive credentials. Not after an incident.