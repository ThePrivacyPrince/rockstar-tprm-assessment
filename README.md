# Rockstar Games × Anodot — TPRM Postmortem & Risk Assessment Engine

> A real-world third-party risk assessment framework built from the 
> April 2026 ShinyHunters breach of Rockstar Games via their vendor Anodot.
> Built as a portfolio project demonstrating GRC engineering fundamentals.

---

## The Breach — What Happened

On April 14, 2026, hacking group ShinyHunters leaked 78.6 million records from Rockstar Games. The attack did not breach Rockstar directly. Instead, attackers compromised Anodot — a SaaS cloud cost monitoring platform that Rockstar used — extracted long-lived authentication tokens, and used them to silently traverse into Rockstar's connected Snowflake data warehouse.

**The attack chain:**

ShinyHunters → Compromised Anodot → Stole Auth Tokens
→ Impersonated Trusted Service → Accessed Snowflake Warehouse → Exfiltrated 78.6M Records → Rockstar blind for 10 days

**This breach was preventable.** 

Five targeted vendor assessment questions 
would have surfaced the risk before it happened.

## What This Project Demonstrates

- Translating a real security incident into a structured TPRM framework
- Automating vendor risk scoring with Python instead of manual spreadsheets
- Applying ISO 27001:2022 Annex A controls to a real attack vector
- Building a SAQ that identifies critical vendor risks programmatically
- Generating evidence-grade PDF reports from code
- Thinking in policy as code controls defined as data, enforced by logic

## Project Structure

rockstar-tprm-assessment/
├── 01_postmortem/
│   └── incident_timeline.md       # Attack chain + root cause analysis
├── 02_risk_register/
│   └── risk_register.md           # 8 scored risks from this breach
├── 03_saq/
│   └── vendor_saq.md              # 25 questions that surface token risk
├── 04_gap_analysis/
│   └── iso27001_gap_analysis.md   # 9 ISO 27001 controls scored
├── 05_python/
│   ├── main.py                    # Runs the full assessment engine
│   ├── requirements.txt
│   ├── data/
│   │   ├── controls.json          # ISO 27001 control catalog
│   │   ├── vendor_responses.json  # Anodot scored responses
│   │   └── saq_responses.json     # SAQ evaluation data
│   ├── src/
│   │   ├── loader.py              # JSON data loader
│   │   ├── scorer.py              # Risk scoring engine
│   │   ├── gap_analyzer.py        # Control gap identification
│   │   ├── saq_evaluator.py       # SAQ critical flag logic
│   │   └── report_generator.py    # PDF report generator
│   └── tests/
│       └── test_scorer.py         # Unit tests
└── 06_report/
└── anodot_tprm_report.pdf     # Final generated output

## The 5 Questions That Would Have Prevented This Breach

| # | Question | What It Would Have Caught |
|---|----------|--------------------------|
| 1 | Are authentication tokens short-lived under 24 hours? | Token persistence after theft |
| 2 | What is your breach notification SLA? | 10-day blind spot |
| 3 | Is access scoped to least-privilege per schema only? | Warehouse-wide blast radius |
| 4 | Do you have anomaly detection on integration pipelines? | Silent exfiltration |
| 5 | Do you hold a current SOC 2 Type II certification? | All of the above |

## Frameworks Applied

- **ISO 27001:2022** — Annex A controls A.5.19, A.5.20, A.5.21, A.5.22, A.8.3, A.8.5, A.8.16, A.8.24, A.5.23
- **NIST SP 800-161** — Supply chain risk management
- **PCI DSS v4.0** — Requirement 12.8 third-party obligations

## Tech Stack

- **Python 3.11** — Scoring engine, gap analysis, SAQ evaluation
- **ReportLab** — PDF report generation
- **pytest** — Unit testing
- **Rich** — Terminal output formatting

## How to Run

```bash
cd 05_python
pip install -r requirements.txt
python3 main.py
```

Output will be saved to `06_report/anodot_tprm_report.pdf`

## Key Findings

| Control | Area | Score | Status |
|---------|------|-------|--------|
| A.5.19 | Supplier Security Policy | 1/5 | Not Implemented |
| A.5.20 | Supplier Agreements | 1/5 | Not Implemented |
| A.5.21 | ICT Supply Chain | 2/5 | Partial |
| A.5.22 | Supplier Monitoring | 1/5 | Not Implemented |
| A.8.3 | Access Restriction | 1/5 | Not Implemented |
| A.8.5 | Secure Authentication | 1/5 | Not Implemented |
| A.8.16 | Monitoring Activities | 1/5 | Not Implemented |
| A.8.24 | Cryptography | 1/5 | Not Implemented |
| A.5.23 | Cloud Service Security | 1/5 | Not Implemented |

**Overall Vendor Risk Rating: CRITICAL — Average Score: 1.1/5**

## Author

Built by Irvens Erisitl | M.S. Cyber Security | GRC & Security Analyst
Focused on GRC Engineering and Third-Party Risk

*This project is part of an ongoing portfolio demonstrating compliance-as-code and GRC engineering fundamentals.*