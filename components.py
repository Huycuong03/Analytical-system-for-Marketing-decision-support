import streamlit as st
import plotly.express as px

def kpi_container(col, title: str, value, delta: dict = None, template: str = None):
    with col:
        with st.container(border=True):
            st.metric(title, value, delta=template.format(**delta) if template else None)

def hist(data, title: str, bins: int = 10, desc: bool = False):
    st.plotly_chart(
        px.histogram(
            data,
            nbins=bins,
            title=title,
        ).update_layout(
            showlegend=False,
            xaxis={"title": None, "categoryorder": 'total descending' if desc else None}
        )
    )

def donut(data, title, names: list[str] = None):
    st.plotly_chart(
        px.pie(
            data, 
            title=title,
            names=names if names else data.index, 
            values=data.values, 
            hole=0.3
        ).update_layout(
            legend=dict(
                orientation='h',   
                yanchor='top',     
                y=-0.2,            
                xanchor='center',  
                x=0.5              
            )
        )
    )

def line(data, x, y, title):
    st.plotly_chart(
        px.line(
            data,
            x=x,
            y=y,
            title=title
        )
    )

def bar(data, title):
    st.plotly_chart(
        px.bar(
            data,
            title=title
        ).update_layout(
            showlegend=False,
            xaxis={"title": None}
        )
    )

def scatter(data, x, y, c, title):
    st.plotly_chart(
        px.scatter(
            data, 
            x=x, 
            y=y, 
            color=c, 
            color_continuous_scale='Spectral', 
            title=title)
    )