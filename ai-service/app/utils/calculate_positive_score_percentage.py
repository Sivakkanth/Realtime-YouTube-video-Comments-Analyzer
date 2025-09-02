from typing import List, Dict

def calculate_positive_score_percentage(classified_comments: List[Dict]) -> float:
    positive_total = sum((c.get("likes", 0) + 1) for c in classified_comments if c.get("status") == "p")
    negative_total = sum((c.get("likes", 0) + 1) for c in classified_comments if c.get("status") == "n")

    total = positive_total + negative_total
    if total == 0:
        return 0.0

    return round((positive_total / total) * 100, 2)