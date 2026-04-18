# 05_python/src/scorer.py

SCORE_LABELS = {
    1: "Not Implemented",
    2: "Partial",
    3: "Implemented",
    4: "Mature",
    5: "Optimized"
}

RISK_THRESHOLDS = {
    "CRITICAL": (1.0, 1.5),
    "HIGH":     (1.5, 2.5),
    "MEDIUM":   (2.5, 3.5),
    "LOW":      (3.5, 5.1)
}

WEIGHT_MULTIPLIERS = {
    "critical": 1.5,
    "high":     1.2,
    "medium":   1.0,
    "low":      0.8
}


def get_score_label(score: int) -> str:
    """Returns human readable label for a numeric score."""
    return SCORE_LABELS.get(score, "Unknown")


def calculate_weighted_average(responses: list, controls: list) -> float:
    """
    Calculates a weighted average score.
    Critical controls carry more weight than low ones.
    """
    weight_map = {c["id"]: c["weight"] for c in controls}

    total_weighted_score = 0
    total_weight = 0

    for response in responses:
        control_id = response["control_id"]
        score = response["score"]
        weight_label = weight_map.get(control_id, "medium")
        multiplier = WEIGHT_MULTIPLIERS.get(weight_label, 1.0)

        total_weighted_score += score * multiplier
        total_weight += multiplier

    if total_weight == 0:
        return 0.0

    return round(total_weighted_score / total_weight, 2)


def get_risk_rating(weighted_avg: float) -> str:
    """Maps a weighted average score to a risk rating."""
    for rating, (low, high) in RISK_THRESHOLDS.items():
        if low <= weighted_avg < high:
            return rating
    return "LOW"


def calculate_vendor_risk(responses: list, controls: list) -> dict:
    """
    Master function. Takes responses and controls.
    Returns full risk summary dictionary.
    """
    scores = [r["score"] for r in responses]
    weighted_avg = calculate_weighted_average(responses, controls)
    risk_rating = get_risk_rating(weighted_avg)

    failed = [r for r in responses if r["score"] <= 2]
    not_implemented = [r for r in responses if r["score"] == 1]

    return {
        "vendor": "Anodot",
        "total_controls_assessed": len(scores),
        "weighted_average_score": weighted_avg,
        "risk_rating": risk_rating,
        "failed_controls": len(failed),
        "not_implemented_count": len(not_implemented),
        "score_breakdown": {
            label: sum(1 for s in scores if s == val)
            for val, label in SCORE_LABELS.items()
        }
    }