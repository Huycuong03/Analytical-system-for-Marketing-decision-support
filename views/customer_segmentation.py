import streamlit as st
import pandas as pd
import components as cmp
from sklearn.cluster import KMeans

st.title("Customer segmentation")

st.header("Segmentation")

df = pd.read_csv("data/surveys.csv")

cols = ["age", "gender", "income_level", "education_level", "visit_frequency", "favorite_product_id"]
inertia = []
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df[cols])
    inertia.append(kmeans.inertia_)

cmp.line(
    pd.DataFrame({"Number of clusters": k_range, "Inertia": inertia}),
    "Number of clusters",
    "Inertia",
    "<b>Number of clusters and Inertia</b>"
)

N_CLUSTERS = 5
kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42)
kmeans.fit(df[cols])
df["cluster"] = kmeans.predict(df[cols])

cmp.hist(
    ("Cluster " + (df["cluster"] + 1).astype(str)).astype("category"),
    "<b>Customer clusters by size</b>",
    desc=True
)

st.markdown("---")
st.header("Segment analysis")

a, _ = st.columns([1, 2])
with a:
    selected_cluster = st.selectbox(
        "Choose a customer cluster",
        options=[*range(1, N_CLUSTERS + 1)]
    ) - 1

segment_df = df.query(
    "cluster == @selected_cluster"
)

INCOME_CATEGORIES = ["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"]
EDUCATION_CATEGORIES = ["None", "Primary", "Secondary", "Associate", "Bachelor", "Graduate"]
VISIT_FREQUENCY_CATEGORIES = ["Daily", "Several times a week", "Once a week", "Several times a month", "Once a month", "Less than once a month", "First time visitor"]

segment_size = segment_df.shape[0]
segment_proportion = segment_df.shape[0] / df.shape[0] * 100
avg_income_level = INCOME_CATEGORIES[int(segment_df["income_level"].median() - 1)]
avg_edu_level = EDUCATION_CATEGORIES[int(segment_df["education_level"].median() - 1)]
avg_rating = segment_df["rating"].mean()
avg_visit_freq = VISIT_FREQUENCY_CATEGORIES[int(segment_df["visit_frequency"].median() - 1)]

kpis_r1 = [
    ("Segment size", f"{segment_size} ({segment_proportion:.1f}%)"),
    ("Average income level", avg_income_level),
    ("Average education level", avg_edu_level)
]

kpi_r2 = [
    ("Average visit frequency", avg_visit_freq),
    ("Average rating", f"{avg_rating:.1f}")
]

for col, (title, value) in zip(st.columns(len(kpis_r1)), kpis_r1):
    cmp.kpi_container(col, title, value)

for col, (title, value) in zip(st.columns(len(kpi_r2)), kpi_r2):
    cmp.kpi_container(col, title, value)

st.markdown("---")

segment_growth = segment_df.groupby(["year", "quarter"]).agg("size").reset_index()
segment_growth = segment_growth.rename(columns={0: "Size"})
segment_growth["Year-Quarter"] = segment_growth['year'].astype(str) + '-Q' + segment_growth['quarter'].astype(str)
cmp.line(
    segment_growth,
    "Year-Quarter",
    "Size",
    "<b>Expected growth</b>"
)

PRODUCT_CATEGORIES = ["Coffee", "Tea", "Soda", "Water", "Juice", "Milk", "Hot Chocolate", "Lemonade", "Beer", "Wine"]
cmp.hist(
    segment_df["favorite_product_id"].replace(pd.Series(PRODUCT_CATEGORIES, index=[*range(1, len(PRODUCT_CATEGORIES) + 1)])).astype("category"),
    "<b>Favorite product distribution</b>",
    desc=True
)