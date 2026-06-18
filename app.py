import streamlit as st
import pandas as pd
from model import predict_event_impact

st.set_page_config(
    page_title="Smart Event Traffic Intelligence System",
    page_icon="🚦",
    layout="wide"
)

# ---------- DATA ----------
file_path = r"C:\Users\shubh\Downloads\Astram event data_anonymized - Astram event data_anonymizedb40ac87.csv"
df = pd.read_csv(file_path)

df["start_datetime"] = pd.to_datetime(df["start_datetime"], errors="coerce")
df["hour"] = df["start_datetime"].dt.hour

total_events = len(df)
unplanned_percent = round((df["event_type"].value_counts().get("unplanned", 0) / total_events) * 100, 1)
top_cause = df["event_cause"].value_counts().idxmax().replace("_", " ").title()
peak_hour = int(df["hour"].value_counts().idxmax())

# ---------- CSS ----------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}
.sub-text {
    font-size: 17px;
    color: #b6b6b6;
    margin-bottom: 25px;
}
.card {
    background-color: #111827;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #263244;
    margin-bottom: 18px;
}
.big-number {
    font-size: 34px;
    font-weight: 700;
}
.small-label {
    color: #9ca3af;
    font-size: 14px;
}
.section-title {
    font-size: 28px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Event Input")

event_cause = st.sidebar.selectbox(
    "Event Cause",
    sorted(df["event_cause"].dropna().unique())
)

priority = st.sidebar.selectbox(
    "Priority",
    sorted(df["priority"].dropna().unique())
)

police_station = st.sidebar.selectbox(
    "Police Station",
    sorted(df["police_station"].dropna().unique())
)

hour = st.sidebar.slider("Event Hour", 0, 23, 21)

requires_road_closure = st.sidebar.selectbox(
    "Requires Road Closure?",
    [False, True]
)

predict_btn = st.sidebar.button("🚀 Predict Impact", use_container_width=True)

# ---------- HERO ----------
st.markdown('<div class="main-title">🚦 Smart Event Traffic Intelligence System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">Predict event-driven traffic congestion and recommend manpower, barricading, and diversion strategy before breakdown occurs.</div>',
    unsafe_allow_html=True
)

st.success(
    "Current systems react after congestion occurs. Our platform predicts traffic risk beforehand and recommends actionable deployment strategies."
)

# ---------- KPI CARDS ----------
st.markdown('<div class="section-title">📌 Key Dataset Insights</div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="card">
        <div class="small-label">Total Events</div>
        <div class="big-number">{total_events}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card">
        <div class="small-label">Unplanned Events</div>
        <div class="big-number">{unplanned_percent}%</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="card">
        <div class="small-label">Top Cause</div>
        <div class="big-number">{top_cause}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="card">
        <div class="small-label">Peak Hour</div>
        <div class="big-number">{peak_hour}:00</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------- PREDICTION ----------
st.markdown('<div class="section-title">🧠 Event Impact Prediction</div>', unsafe_allow_html=True)

if predict_btn:
    result = predict_event_impact(
        event_cause=event_cause,
        priority=priority,
        police_station=police_station,
        hour=hour,
        requires_road_closure=requires_road_closure
    )

    risk_score = result["risk_score"]
    risk_level = result["risk_level"]
    resources = result["resources"]

    p1, p2, p3 = st.columns(3)

    p1.metric("Risk Score", risk_score)
    p2.metric("Risk Level", risk_level)
    p3.metric("Road Closure Chance", f"{result['road_closure_chance']}%")

    st.markdown("### Risk Severity Meter")
    st.progress(risk_score / 100)
    st.caption(f"Current risk severity is {risk_score}% out of 100.")

    if risk_level == "Critical":
        st.error("🔴 Critical Risk: Immediate intervention required.")
    elif risk_level == "High":
        st.warning("🟠 High Risk: Quick response and active monitoring required.")
    elif risk_level == "Medium":
        st.info("🟡 Medium Risk: Monitor closely and keep resources ready.")
    else:
        st.success("🟢 Low Risk: Normal monitoring is sufficient.")

    st.markdown('<div class="section-title">🚔 Resource Recommendation</div>', unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)

    r1.metric("Police Required", resources["police_required"])
    r2.metric("Barricades Required", resources["barricades_required"])
    r3.metric("Diversion", resources["diversion_required"])

    st.info(resources["response"])

    st.subheader("📋 Executive Summary")
    st.success(
        f"""
        Predicted Risk Level: {risk_level}

        Recommended Action:
        • Deploy {resources['police_required']} police personnel  
        • Arrange {resources['barricades_required']} barricades  
        • Diversion Status: {resources['diversion_required']}  
        """
    )

else:
    st.info("Select event details from the sidebar and click Predict Impact.")

st.divider()

# ---------- MAP ----------
st.markdown('<div class="section-title">🗺️ Traffic Event Hotspot Map</div>', unsafe_allow_html=True)

st.write("Historical event locations mapped using latitude and longitude coordinates.")

try:
    st.image(
        r"C:\Users\shubh\Desktop\python\eda.py\hotspot_map.jpeg",
        caption="Traffic Event Hotspot Distribution",
        use_container_width=True
    )
except:
    map_data = df[["latitude", "longitude"]].dropna()
    st.map(map_data)

st.divider()

# ---------- GRAPHS ----------
st.markdown('<div class="section-title">📊 Historical Data Analysis</div>', unsafe_allow_html=True)

g1, g2 = st.columns(2)

with g1:
    st.image("graphs/event_type_pie.png", caption="Planned vs Unplanned Events", use_container_width=True)
    st.image("graphs/event_cause_bar.png", caption="Top Event Causes", use_container_width=True)
    st.image("graphs/top_zones.png", caption="Top Zones by Event Count", use_container_width=True)

with g2:
    st.image("graphs/hour_wise_events.png", caption="Hour-wise Event Distribution", use_container_width=True)
    st.image("graphs/top_police_stations.png", caption="Top Police Stations by Event Count", use_container_width=True)
    st.image("graphs/road_closure_probability.png", caption="Road Closure Probability by Event Cause", use_container_width=True)

st.divider()

# ---------- SYSTEM ----------
st.subheader("🔄 System Workflow")

st.info("""
📂 Historical Traffic Event Data

⬇️

⚙️ Feature Extraction
(Time, Cause, Location, Priority)

⬇️

🧠 Risk Prediction Engine

⬇️

🚔 Resource Recommendation Engine

⬇️

🗺️ Dashboard + Hotspot Map + Insights
""")