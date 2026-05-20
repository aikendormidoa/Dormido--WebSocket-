"""
Part C: Plant Health Classification Model
Classifies sensor readings as: Healthy / Warning / Critical
This simulates a simple rule-based AI model inference.
"""


def classify_plant_health(temperature: float, humidity: float, crop_health_index: float) -> dict:
    """
    Part C Step 1: Receives temperature, humidity, crop_health_index as input.
    Returns classification label, color, alert message, and recommendation.

    Thresholds (based on common agricultural standards):
      Temperature: optimal 20–30°C
      Humidity:    optimal 50–80%
      Crop Index:  0–100 (100 = perfect health)
    """

    issues = []

    # Temperature check
    if temperature < 10 or temperature > 40:
        issues.append("critical_temp")
    elif temperature < 15 or temperature > 35:
        issues.append("warning_temp")

    # Humidity check
    if humidity < 20 or humidity > 95:
        issues.append("critical_humidity")
    elif humidity < 40 or humidity > 85:
        issues.append("warning_humidity")

    # Crop health index check
    if crop_health_index < 30:
        issues.append("critical_crop")
    elif crop_health_index < 60:
        issues.append("warning_crop")

    # Determine overall status
    if any("critical" in i for i in issues):
        label = "Critical"
        color = "#ff4757"
        alert = build_alert(issues, temperature, humidity, crop_health_index)
        recommendation = get_recommendation("Critical", issues)

    elif any("warning" in i for i in issues):
        label = "Warning"
        color = "#ffa502"
        alert = build_alert(issues, temperature, humidity, crop_health_index)
        recommendation = get_recommendation("Warning", issues)

    else:
        label = "Healthy"
        color = "#2ed573"
        alert = None
        recommendation = "All parameters are within optimal range. No action needed."

    return {
        "label": label,
        "color": color,
        "alert": alert,
        "recommendation": recommendation,
    }


def build_alert(issues, temp, humidity, crop_index):
    parts = []
    if any("temp" in i for i in issues):
        parts.append(f"Temperature {temp}°C is out of range")
    if any("humidity" in i for i in issues):
        parts.append(f"Humidity {humidity}% is out of range")
    if any("crop" in i for i in issues):
        parts.append(f"Crop health index {crop_index} is low")
    return " | ".join(parts)


def get_recommendation(status, issues):
    recs = []
    if status == "Critical":
        if any("temp" in i for i in issues):
            recs.append("Immediately adjust greenhouse temperature or provide shade/heating.")
        if any("humidity" in i for i in issues):
            recs.append("Activate irrigation system or improve drainage urgently.")
        if any("crop" in i for i in issues):
            recs.append("Inspect crops immediately for disease, pests, or nutrient deficiency.")
    elif status == "Warning":
        if any("temp" in i for i in issues):
            recs.append("Monitor temperature closely and prepare cooling/heating systems.")
        if any("humidity" in i for i in issues):
            recs.append("Adjust irrigation schedule slightly.")
        if any("crop" in i for i in issues):
            recs.append("Schedule a crop health inspection within 24 hours.")
    return " ".join(recs) if recs else "Monitor the situation closely."
