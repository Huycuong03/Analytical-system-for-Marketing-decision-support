import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(layout="wide")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)
    
if st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')
else:
    st.logo("assets/logo.png", size="large")

    authenticator.logout(location="sidebar")

    customer_analysis_page = st.Page(
        page="views/customer_analysis.py",
        title="Customer analysis",
        icon=":material/account_circle:",
        default=True
    )

    customer_segmentation_page = st.Page(
        page="views/customer_segmentation.py",
        title="Customer Segmentation",
        icon=":material/scatter_plot:"
    )

    sales_analysis_page = st.Page(
        page="views/sales_analysis.py",
        title="Sales analysis",
        icon=":material/bar_chart:"
    )

    campaign_analysis_page = st.Page(
        page="views/campaign_analysis.py",
        title="Campaign analysis",
        icon=":material/campaign:"
    )

    campaign_simulation_page = st.Page(
        page="views/campaign_simulation.py",
        title="Campaign simulation",
        icon=":material/simulation:"
    )

    pg = st.navigation(
        pages=[
            customer_analysis_page, 
            customer_segmentation_page, 
            sales_analysis_page, 
            campaign_analysis_page, 
            campaign_simulation_page
        ]
    )

    pg.run()