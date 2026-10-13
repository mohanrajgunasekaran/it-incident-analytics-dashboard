from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="IT Incident Analytics", page_icon="📊", layout="wide")
DATA = Path(__file__).parent / "data" / "incidents.csv"
ORDER = ["P1", "P2", "P3", "P4"]

@st.cache_data
def load_data(path, modified):
    df = pd.read_csv(path, parse_dates=["created_at", "resolved_at"])
    df["priority"] = pd.Categorical(df["priority"], categories=ORDER, ordered=True)
    df["resolution_hours"] = (df["resolved_at"] - df["created_at"]).dt.total_seconds() / 3600
    df["sla_breached"] = df["status"].eq("Resolved") & df["resolution_hours"].notna() & (df["resolution_hours"] > df["sla_target_hours"])
    df["created_date"] = df["created_at"].dt.date
    return df

st.title("📊 IT Incident Analytics Dashboard")
st.caption("Portfolio project · Synthetic data only · Illustrative SLA targets")
if not DATA.exists():
    st.error("Dataset missing. Run `python generate_data.py` first."); st.stop()
df = load_data(str(DATA), DATA.stat().st_mtime)

with st.sidebar:
    st.header("Filters")
    dmin, dmax = df.created_at.min().date(), df.created_at.max().date()
    dates = st.date_input("Created date range", value=(dmin, dmax), min_value=dmin, max_value=dmax)
    priorities = st.multiselect("Priority", ORDER, default=ORDER)
    services = st.multiselect("Service", sorted(df.service.unique()), default=sorted(df.service.unique()))
    statuses = st.multiselect("Status", sorted(df.status.unique()), default=sorted(df.status.unique()))
    st.caption("Targets are demo assumptions, not a real organisation's SLA policy.")

f = df.copy()
if isinstance(dates, (tuple, list)) and len(dates) == 2: f = f[f.created_date.between(dates[0], dates[1])]
f = f[f.priority.isin(priorities) & f.service.isin(services) & f.status.isin(statuses)]
resolved = f[f.status.eq("Resolved")]
mttr = resolved.resolution_hours.mean() if not resolved.empty else 0
breach = resolved.sla_breached.mean() * 100 if not resolved.empty else 0
a,b,c,d = st.columns(4)
a.metric("Incidents", f"{len(f):,}")
b.metric("P1 / P2 incidents", f"{int(f.priority.isin(['P1','P2']).sum()):,}")
c.metric("SLA breach rate", f"{breach:.1f}%", help="Among resolved incidents in this filtered view.")
d.metric("Mean time to resolve", f"{mttr:.1f} h", help="Resolved incidents only.")
if f.empty:
    st.info("No records match these filters. Widen the date range or select more filter values."); st.stop()

left,right = st.columns([1.4,1])
with left:
    st.subheader("Incident volume over time")
    daily = f.groupby("created_date").size().rename("Incidents").reset_index()
    st.plotly_chart(px.line(daily, x="created_date", y="Incidents", labels={"created_date":"Created date"}), use_container_width=True)
with right:
    st.subheader("Priority distribution")
    counts = f.priority.astype(str).value_counts().reindex(ORDER, fill_value=0).rename_axis("Priority").reset_index(name="Incidents")
    st.plotly_chart(px.pie(counts, names="Priority", values="Incidents", hole=.45), use_container_width=True)

left,right = st.columns(2)
with left:
    st.subheader("Mean time to resolve by priority")
    if resolved.empty: st.info("No resolved records in this selection.")
    else:
        p = resolved.groupby("priority", observed=False).resolution_hours.mean().reset_index()
        p["priority"] = p.priority.astype(str)
        st.plotly_chart(px.bar(p, x="priority", y="resolution_hours", category_orders={"priority":ORDER}, labels={"priority":"Priority","resolution_hours":"Mean resolution time (hours)"}), use_container_width=True)
with right:
    st.subheader("SLA breaches by service")
    if resolved.empty: st.info("No resolved records in this selection.")
    else:
        s = resolved.groupby("service").agg(Resolved=("incident_id","count"), Breaches=("sla_breached","sum")).reset_index()
        s["Breach rate (%)"] = s.Breaches / s.Resolved * 100
        st.plotly_chart(px.bar(s.sort_values("Breach rate (%)", ascending=False), x="service", y="Breach rate (%)", hover_data=["Resolved","Breaches"]), use_container_width=True)

st.subheader("Root-cause categories")
causes = f.root_cause.value_counts().rename_axis("Root cause").reset_index(name="Incidents")
st.plotly_chart(px.bar(causes, x="Incidents", y="Root cause", orientation="h"), use_container_width=True)
st.subheader("Incident records")
cols = ["incident_id","created_at","resolved_at","priority","service","category","root_cause","status","sla_target_hours","resolution_hours","sla_breached","assigned_team"]
table = f[cols].copy()
table["resolution_hours"] = table.resolution_hours.round(2)
st.dataframe(table, use_container_width=True, hide_index=True)
st.download_button("⬇️ Download filtered records (CSV)", table.to_csv(index=False).encode("utf-8"), "filtered_synthetic_incidents.csv", "text/csv")
st.caption("Synthetic records are randomly generated for demonstration and must not be used to infer real operational performance.")
