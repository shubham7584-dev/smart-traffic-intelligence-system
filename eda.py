import pandas as pd

file_path = r"C:\Users\shubh\Downloads\Astram event data_anonymized - Astram event data_anonymizedb40ac87.csv"

df = pd.read_csv(file_path)

print("\n========== BASIC INFO ==========")
print("Rows, Columns:", df.shape)

print("\n========== COLUMN NAMES ==========")
for col in df.columns:
    print(col)

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== EVENT TYPE COUNT ==========")
print(df["event_type"].value_counts())

print("\n========== EVENT CAUSE COUNT ==========")
print(df["event_cause"].value_counts().head(10))

print("\n========== PRIORITY COUNT ==========")
print(df["priority"].value_counts())

print("\n========== ROAD CLOSURE COUNT ==========")
print(df["requires_road_closure"].value_counts())

print("\n========== TOP 10 POLICE STATIONS ==========")
print(df["police_station"].value_counts().head(10))

print("\n========== TOP 10 CORRIDORS ==========")
print(df["corridor"].value_counts().head(10))

print("\n========== TOP 10 ZONES ==========")
print(df["zone"].value_counts().head(10))

# Time analysis
df["start_datetime"] = pd.to_datetime(df["start_datetime"], errors="coerce")
df["hour"] = df["start_datetime"].dt.hour
df["day_name"] = df["start_datetime"].dt.day_name()
df["month"] = df["start_datetime"].dt.month

print("\n========== EVENTS BY HOUR ==========")
print(df["hour"].value_counts().sort_index())

print("\n========== EVENTS BY DAY ==========")
print(df["day_name"].value_counts())

print("\n========== EVENTS BY MONTH ==========")
print(df["month"].value_counts().sort_index())

# Duration analysis
df["end_datetime"] = pd.to_datetime(df["end_datetime"], errors="coerce")
df["duration_minutes"] = (df["end_datetime"] - df["start_datetime"]).dt.total_seconds() / 60

print("\n========== DURATION ANALYSIS ==========")
print(df["duration_minutes"].describe())

print("\n========== AVG DURATION BY EVENT CAUSE ==========")
print(df.groupby("event_cause")["duration_minutes"].mean().sort_values(ascending=False).head(10))

print("\n========== ROAD CLOSURE BY EVENT CAUSE ==========")
print(df.groupby("event_cause")["requires_road_closure"].mean().sort_values(ascending=False).head(10))

print("\nDone bhai ✅")