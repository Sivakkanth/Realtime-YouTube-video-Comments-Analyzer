def calculate_positive_score_percentage(classified_comments):
    positive_total = 0
    negative_total = 0

    for comment in classified_comments:
        if 'status' in comment and 'likes' in comment:
            weight = comment['likes'] + 1
            if comment['status'] == 'p':
                positive_total += weight
            elif comment['status'] == 'n':
                negative_total += weight

    total = positive_total + negative_total

    if total == 0:
        return 0  # Avoid division by zero if no positive or negative comments

    positive_score_percent = (positive_total / total) * 100
    return round(positive_score_percent, 2)