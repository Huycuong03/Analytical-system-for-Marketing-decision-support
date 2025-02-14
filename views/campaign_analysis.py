import streamlit as st
import pandas as pd
import components as cmp
from datetime import datetime

st.title("Campagin analysis")

campaign_df = pd.read_csv("data/campaigns.csv").set_index("id")

a, _ = st.columns([1, 2])
with a:
    selected_campaign_id = st.selectbox(
        "Choose a campaign",
        options=[*range(1, campaign_df.shape[0] + 1)][::-1]
    )

st.markdown("---")
st.header("Info")
selected_campaign = campaign_df.loc[selected_campaign_id]
st.markdown(
f"""
> ### "{selected_campaign["message"]}"
> *from {selected_campaign["from_date"]} to {selected_campaign["to_date"]}* 
""")

SOCIAL_MEDIA_CATEGORIES = ["Facebook", "Instagram", "Twitter"]
info = [
    ("Discount", f"{selected_campaign["discount"]:,.0f} (VND)"),
    ("Channel", SOCIAL_MEDIA_CATEGORIES[selected_campaign["channel"] - 1])
]

for col, (title, value) in zip(st.columns(len(info)), info):
    cmp.kpi_container(col, title, value)

st.markdown("---")
st.header("Analytics")

event_df = pd.read_csv("data/events.csv").query(
    "campaign_id == @selected_campaign_id"
)

sales_df = pd.read_csv("data/orders.csv").query(
    "campaign_id == @selected_campaign_id"
)
sales_df["total"] = (sales_df["subtotal"] - selected_campaign["discount"]).apply(abs)
sales_df["date"] = sales_df["timestamp"].apply(datetime.fromtimestamp).dt.date

impression = event_df.shape[0]
reach = len(event_df["uid"].unique())
ctr = event_df[event_df["action"] == "click"].shape[0] / impression * 100
er = event_df[event_df["action"].isin(["like", "share", "comment"])].shape[0] / impression * 100
br = event_df[event_df["action"].isna()].shape[0] / impression * 100

kpi_r1 = [
    ("Impression", impression),
    ("Reach", reach)
]

for col, (title, value) in zip(st.columns(len(kpi_r1)), kpi_r1):
    cmp.kpi_container(col, title, value)

kpi_r2 = [
    ("Enagement rate", f"{er:.1f} %"),
    ("Click-through rate", f"{ctr:.1f} %"),
    ("Bounce rate", f"{br:.1f} %")
]

a, b = st.columns([2, 1], gap="medium")

with a:
    cmp.line(
        sales_df.groupby("date")["total"].sum().to_frame().reset_index(),
        "date",
        "total",
        "<b>Revenue from campaign</b>"
    )

for title, value in kpi_r2:
        cmp.kpi_container(b, title, value)