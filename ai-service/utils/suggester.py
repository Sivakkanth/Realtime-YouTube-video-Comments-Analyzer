def generate_suggestions(score, comments):
    suggestions = []

    if score < 50:
        suggestions.append("Increase engagement by replying to user comments.")
        suggestions.append("Consider adding more visual explanation.")
    elif score < 75:
        suggestions.append("Improve audio or subtitles for better accessibility.")
    else:
        suggestions.append("Excellent response! Keep up the great work!")

    if any("slow" in c.lower() for c in comments):
        suggestions.append("Consider speeding up the video pace.")

    return suggestions