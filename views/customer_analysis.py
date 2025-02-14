import streamlit as st
import pandas as pd
import components as cmp

st.title("Customer analysis")

df = pd.read_csv("data/surveys.csv")

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

review_count = selected_df.shape[0]
avg_age = round(selected_df["age"].mean(), 1)
avg_rating = round(selected_df["rating"].mean())

kpis = [
    ("Participant count", review_count),
    ("Average age", avg_age),
    ("Average rating", f"{avg_rating}")
]

for col, (title, value) in zip(st.columns(3), kpis):
    cmp.kpi_container(col, title, value)

st.markdown("---")

a, b = st.columns([2, 1])

with a:
    cmp.hist(
        selected_df["age"], 
        "<b>Age distribution</b>"
    )

with b:
    cmp.donut(
        selected_df["gender"].replace({True: "Male", False: "Female"}).value_counts(normalize=True) * 100,
        "<b>Gender proportion</b>"
    )

a, b = st.columns(2)

INCOME_CATEGORIES = ["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"]
with a:
    cmp.hist(
        selected_df["income_level"].replace(pd.Series(INCOME_CATEGORIES, index=[*range(1, len(INCOME_CATEGORIES) + 1)])).astype("category"),
        "<b>Income distribution</b>",
        desc=True
    )

EDUCATION_CATEGORIES = ["None", "Primary", "Secondary", "Associate", "Bachelor", "Graduate"]
with b:
    cmp.hist(
        selected_df["education_level"].replace(pd.Series(EDUCATION_CATEGORIES, index=[*range(1, len(EDUCATION_CATEGORIES) + 1)])).astype("category"),
        "<b>Education distribution</b>",
        desc=True
    )

a, b = st.columns(2)

VISIT_FREQUENCY_CATEGORIES = ["Daily", "Several times a week", "Once a week", "Several times a month", "Once a month", "Less than once a month", "First time visitor"]
with a:
    cmp.hist(
        selected_df["visit_frequency"].replace(pd.Series(VISIT_FREQUENCY_CATEGORIES, index=[*range(1, len(VISIT_FREQUENCY_CATEGORIES) + 1)])).astype("category"),
        "<b>Visit frequency distribution</b>",
        desc=True
    )

PRODUCT_CATEGORIES = ["Coffee", "Tea", "Soda", "Water", "Juice", "Milk", "Hot Chocolate", "Lemonade", "Beer", "Wine"]
with b:
    cmp.hist(
        selected_df["favorite_product_id"].replace(pd.Series(PRODUCT_CATEGORIES, index=[*range(1, len(PRODUCT_CATEGORIES) + 1)])).astype("category"),
        "<b>Favorite product distribution</b>",
        desc=True
    )

a, b = st.columns([2, 1])

with a:
    cmp.hist(
        selected_df["rating"], 
        "<b>Rating distribution</b>"
    )

with b:
    cmp.donut(
        selected_df["positive_comment"].replace({True: "Positive", False: "Negative"}).value_counts(normalize=True) * 100,
        "<b>Comment's positivity proportion</b>"
    )

SOCIAL_MEDIA_CATEGORIES = ["Facebook", "Instagram", "Twitter"]
cmp.hist(
    selected_df["social_media"].replace(pd.Series(SOCIAL_MEDIA_CATEGORIES, index=[*range(1, len(SOCIAL_MEDIA_CATEGORIES) + 1)])).astype("category"),
    "<b>Social media distribution</b>"
)