import pandas as pd

file_path = "Astram event data_anonymized - Astram event data_anonymizedb40ac87.csv"

df = pd.read_csv(file_path)

df["start_datetime"] = pd.to_datetime(df["start_datetime"], errors="coerce")
df["hour"] = df["start_datetime"].dt.hour
df["day_name"] = df["start_datetime"].dt.day_name()

# Historical frequency scores
police_station_count = df["police_station"].value_counts()
event_cause_count = df["event_cause"].value_counts()
closure_probability = df.groupby("event_cause")["requires_road_closure"].mean() * 100


def calculate_risk_score(event_cause, priority, police_station, hour, requires_road_closure):
    score = 0

    # Priority score
    if priority == "High":
        score += 30
    else:
        score += 10

    # Road closure score
    if requires_road_closure == True:
        score += 25
    else:
        score += 5

    # Event cause score
    high_risk_causes = ["vip_movement", "public_event", "protest", "construction", "accident", "tree_fall"]

    if event_cause in high_risk_causes:
        score += 25
    elif event_cause == "vehicle_breakdown":
        score += 18
    else:
        score += 10

    # Peak hour score
    peak_hours = [5, 6, 20, 21, 22]

    if hour in peak_hours:
        score += 15
    else:
        score += 5

    # Hotspot police station score
    if police_station in police_station_count.head(10).index:
        score += 10
    else:
        score += 3

    return min(score, 100)


def get_risk_level(score):
    if score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"


def get_resource_recommendation(risk_level):
    if risk_level == "Critical":
        return {
            "police_required": "15-25",
            "barricades_required": "25-40",
            "diversion_required": "Mandatory",
            "response": "Immediate action required"
        }

    elif risk_level == "High":
        return {
            "police_required": "10-15",
            "barricades_required": "15-25",
            "diversion_required": "Recommended",
            "response": "Quick response needed"
        }

    elif risk_level == "Medium":
        return {
            "police_required": "5-10",
            "barricades_required": "8-15",
            "diversion_required": "Optional",
            "response": "Monitor closely"
        }

    else:
        return {
            "police_required": "2-5",
            "barricades_required": "0-5",
            "diversion_required": "Not required",
            "response": "Normal monitoring"
        }


def predict_event_impact(event_cause, priority, police_station, hour, requires_road_closure):
    score = calculate_risk_score(
        event_cause,
        priority,
        police_station,
        hour,
        requires_road_closure
    )

    risk_level = get_risk_level(score)
    resources = get_resource_recommendation(risk_level)

    closure_chance = closure_probability.get(event_cause, 0)

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "road_closure_chance": round(closure_chance, 2),
        "resources": resources
    }


# Test example
if __name__ == "__main__":
    result = predict_event_impact(
        event_cause="vip_movement",
        priority="High",
        police_station="Yelahanka",
        hour=21,
        requires_road_closure=True
    )

    print("\n========== EVENT IMPACT PREDICTION ==========")
    print("Risk Score:", result["risk_score"])
    print("Risk Level:", result["risk_level"])
    print("Road Closure Chance:", str(result["road_closure_chance"]) + "%")

    print("\n========== RESOURCE RECOMMENDATION ==========")
    for key, value in result["resources"].items():
        print(key, ":", value)