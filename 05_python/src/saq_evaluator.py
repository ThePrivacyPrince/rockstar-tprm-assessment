# 05_python/src/saq_evaluator.py

CRITICAL_QUESTIONS = ["1.1", "1.2", "1.6", "2.2", "3.1", "4.5", "5.1", "5.2"]

ESCALATION_REASON = {
    "1.1": "Token longevity directly enabled attacker persistence after theft",
    "1.2": "Absence of OAuth 2.0 allowed static token reuse across sessions",
    "1.6": "Over-permissioned access caused warehouse-wide exfiltration",
    "2.2": "No notification SLA caused 7-day blind spot for Rockstar",
    "3.1": "Unrestricted schema access maximized the blast radius of the breach",
    "4.5": "No security event logging enabled 10 days of silent undetected exfiltration",
    "5.1": "Absence of IR team caused critical delay in breach notification to Rockstar",
    "5.2": "Untested incident response process broke down under real breach conditions"
}


def evaluate_saq(responses: list) -> dict:
    """
    Evaluates SAQ responses.
    Auto-flags critical findings on key questions.
    Returns full evaluation summary.
    """
    critical_fails = []
    all_fails = []
    pass_count = 0

    for response in responses:
        qid = response["question_id"]
        answer = response["answer"].lower()

        if answer == "yes":
            pass_count += 1
            continue

        finding = {
            "question_id": qid,
            "question": response["question"],
            "answer": answer,
            "breach_relevance": response.get("breach_relevance", "")
        }

        if answer == "no" and qid in CRITICAL_QUESTIONS:
            finding["severity"] = "CRITICAL"
            finding["escalation_reason"] = ESCALATION_REASON.get(qid, "")
            critical_fails.append(finding)

        all_fails.append(finding)

    return {
        "total_questions": len(responses),
        "passed": pass_count,
        "failed": len(all_fails),
        "critical_failures": len(critical_fails),
        "auto_escalate": len(critical_fails) > 0,
        "critical_findings": critical_fails,
        "all_findings": all_fails
    }


def get_critical_summary(saq_results: dict) -> str:
    """
    Returns a plain English summary of critical SAQ failures.
    Used in report generation.
    """
    if not saq_results["auto_escalate"]:
        return "No critical SAQ failures identified."

    lines = [
        f"AUTO-ESCALATE: {saq_results['critical_failures']} "
        f"critical SAQ failure(s) identified.\n"
    ]

    for finding in saq_results["critical_findings"]:
        lines.append(
            f"  [{finding['question_id']}] {finding['question']}\n"
            f"  Reason: {finding['escalation_reason']}\n"
        )

    return "\n".join(lines)