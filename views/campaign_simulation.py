import streamlit as st
import components as cmp
import numpy as np
import datetime
import joblib
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

SOCIAL_MEDIA_CATEGORIES = ["Facebook", "Instagram", "Twitter"]

def get_next_month(d: datetime.date) -> datetime.date:
    if d.month == 12:
        return(datetime.date(d.year + 1, 1, 1))
    return(datetime.date(d.year, d.month + 1, 1))

def process_X(**kwargs):
    message = kwargs["message"]
    channel = SOCIAL_MEDIA_CATEGORIES.index(kwargs["channel"])
    duration = kwargs["duration"]
    discount = kwargs["discount"]

    tfidf = joblib.load('model/tfidf_vectorizer.pkl')
    scaler = joblib.load('model/scaler.pkl')

    X_message_new = tfidf.transform([message]).toarray()
    X_numerical_new = scaler.transform([[discount, channel, duration]])
    return np.hstack([X_message_new, X_numerical_new])

def simulate(**kwargs):
    message = kwargs["message"]
    output_container = kwargs["output_container"]

    if message == None or message == "" :
        st.warning("Please fill out all the fields!")
        return
    
    with output_container:
        model = load_model("model/simulator.keras")
        impression, reach, revenue = model.predict(process_X(**kwargs))[0]
        kpis = [
            ("Impression", f"{impression:.2f}"),
            ("Reach", f"{reach:.2f}"),
            ("Revenue", f"{revenue:.2f}")
        ]
        for title, value in kpis:
            cmp.kpi_container(output_container, title, value)

a, b = st.columns(2)

with a:
    st.header("Input")
    with st.form("simulation_form"):
        message = st.text_area(
            label="Message",
            placeholder="Enter the campaign message here ..."
        )
        channel = st.radio(
            label="Channel",
            options=SOCIAL_MEDIA_CATEGORIES
        )
        today = datetime.datetime.now().date()
        next_month = get_next_month(today)

        from_date, to_date = (next_month, get_next_month(next_month))
        from_date, to_date = st.date_input(
            "Select campaign period",
            (next_month, get_next_month(next_month)),
            format="MM/DD/YYYY",
        )

        duration = (to_date - from_date).days
        discount = st.number_input(
            "Discount",
            value=10_000,
            min_value=0,
            step=10_000,
            placeholder="Enter the campaign discount here ..."
        )
        st.form_submit_button(
            "Simulate",
            on_click=simulate,
            kwargs={
                "message": message,
                "channel": channel,
                "duration": duration,
                "discount": discount,
                "output_container": b
            }
        )


with b:
    st.header("Output")
