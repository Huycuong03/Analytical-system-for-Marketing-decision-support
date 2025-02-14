import streamlit as st
import pandas as pd
import components as cmp
from datetime import datetime

def load_data() -> pd.DataFrame:
    QUATERS = [-1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    order_df = pd.read_csv("data/orders.csv")
    campaign_df = pd.read_csv("data/campaigns.csv")
    sales_df = order_df.merge(
        campaign_df[["id", "discount"]],
        how="left",
        left_on="campaign_id",
        right_on="id"
    )
    sales_df = sales_df.drop(["campaign_id", "id_y"], axis=1).rename(columns={"id_x": "id"}).set_index("id").fillna(0)
    sales_df["total"] = (sales_df["subtotal"] - sales_df["discount"]).map(lambda value: value if value >=0 else 0)
    tmp = sales_df["timestamp"].map(datetime.fromtimestamp)
    sales_df["year"] = tmp.map(lambda dt: dt.year)
    sales_df["quarter"] = tmp.map(lambda dt: QUATERS[dt.month])
    return sales_df

df = load_data()

st.title("Sales analysis")

year_selectbox, quarter_selectbox = st.columns(2, gap="small", vertical_alignment="center")

with year_selectbox:
    year = st.selectbox(
        "Year",
        options=sorted(df["year"].unique(), reverse=True)
    )

with quarter_selectbox:
    quarter = st.selectbox(
        "Quarter",
        options=[1, 2, 3, 4],
    )

selected_df = df.query(
    "year == @year & quarter == @quarter"
)

items_df = pd.read_csv("data/order_items.csv").merge(
    selected_df.reset_index(),
    how="inner",
    left_on="order_id",
    right_on="id"
)[["order_id", "product_id", "quantity"]]

PRODUCT_CATEGORIES = ["Coffee", "Tea", "Soda", "Water", "Juice", "Milk", "Hot Chocolate", "Lemonade", "Beer", "Wine"]
items_df["product_name"] = items_df["product_id"].replace(pd.Series(PRODUCT_CATEGORIES, index=[*range(1, len(PRODUCT_CATEGORIES) + 1)]))

revenue = selected_df["total"].sum()
order_count = selected_df.shape[0]
aov = selected_df["total"].mean()

kpis = [
    ("Revenue", f"{revenue:,.0f} (VND)"),
    ("Order count", order_count),
    ("Average order value (AOV)", f"{aov:,.2f} (VND)")
]

for col, (title, value) in zip(st.columns(3), kpis):
    cmp.kpi_container(col, title, value)

st.markdown("---")

a, b = st.columns(2)

with a:
    data = df.groupby(["year", "quarter"])["total"].sum().to_frame().reset_index()
    data["year_quarter"] = data["year"].astype(str) + "-Q" + data["quarter"].astype(str)
    cmp.line(
        data,
        x="year_quarter",
        y="total",
        title="<b>Revenue by quarter</b>"
    )

with b:
    cmp.bar(
        df.groupby("base")["total"].sum(),
        "<b>Revenue by location</b>"
    )

a, b = st.columns(2)

with a:
    cmp.hist(
        items_df.groupby("order_id")["quantity"].sum(),
        "<b>Number of products per purchase distribution</b>"
    )

with b:
    cmp.bar(
        items_df.groupby("product_name")["quantity"].sum().sort_values(ascending=False),
        "<b>Number of purchases per product distribution</b>"
    )