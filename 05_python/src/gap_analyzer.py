# 05_python/src/gap_analyzer.py

RECOMMENDATIONS = {
    "A.5.19": "Establish formal supplier security policy with credential handling requirements",
    "A.5.20": "Add 24hr breach notification SLA and token management clauses to contract",
    "A.5.21": "Require annual sub-processor security assessments and disclosure",
    "A.5.22": "Implement shared real time connector health monitoring dashboard",
    "A.5.23": "Define cloud service security requirements formally in all customer agreements",
    "A.8.3":  "Restrict Anodot tokens to least privilege schema access only",
    "A.8.5":  "Rotate to short lived OAuth 2.0 tokens with maximum 24hr expiry",
    "A.8.16": "Deploy anomaly detection on Snowflake query volume and off hours access",
    "A.8.24": "Encrypt all authentication tokens at rest using AES-256 minimum"
}

SEVERITY_MAP = {
    1: "CRITICAL",
    2: "HIGH",
    3: "MEDIUM",
    4: "LOW",
    5: "PASS"
}


def find_gaps(controls: list, responses: list) -> list:
    """
    Compares control requirements against vendor responses.
    Returns list of gaps where score is 2 or below.
    """
    response_map = {r["control_id"]: r for r in responses}
    gaps = []

    for control in controls:
        cid = control["id"]
        response = response_map.get(cid, {})
        score = response.get("score", 0)

        if score <= 2:
            gaps.append({
                "control_id": cid,
                "control_name": control["name"],
                "category": control["category"],
                "score": score,
                "severity": SEVERITY_MAP.get(score, "UNKNOWN"),
                "status": response.get("status", "Not Assessed"),
                "evidence": response.get("evidence", "No evidence provided"),
                "breach_relevance": control.get("breach_relevance", ""),
                "recommendation": RECOMMENDATIONS.get(
                    cid,
                    "Review and implement per ISO 27001:2022"
                )
            })

    gaps.sort(key=lambda x: x["score"])
    return gaps


def summarize_gaps(gaps: list) -> dict:
    """Returns a summary count of gaps by severity."""
    summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0}
    for gap in gaps:
        severity = gap.get("severity", "MEDIUM")
        if severity in summary:
            summary[severity] += 1
    return summary