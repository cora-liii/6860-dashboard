import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import datetime

# import graph from plot.py
from plots import plot

# set basic
st.set_page_config(layout="wide")


# read Data
dash_data = pd.read_csv("data/dash_map.csv",index_col=0)
rader_line = pd.read_csv('data/Basic_data.csv',index_col=0)
rader = rader_line[['location','restriction_gatherings','school_closures','stay_home_requirements','workplace_closures','containment_index']]
lines = rader_line[['location','Day','new_cases','new_deaths','new_vaccinations']]
statistcs = rader_line.groupby('Day').sum()[['new_cases','new_deaths','new_vaccinations']].reset_index()
country_lst = rader_line["location"].unique()

st.title("😷 Covid-19 Dashboard")
st.caption(f"view at: {datetime.datetime.now().strftime('%Y-%m-%d')}")

with st.sidebar:
        st.image(image="./image/sydlogo.png",width=150)
        st.header("Filter part")
        dates = statistcs["Day"].values
        selected_date = st.selectbox("please select date:",dates)
        st.markdown("---")
        selected_country = st.selectbox("please select country:",country_lst)

tab1,tab2 = st.tabs(["World Data","Country Data"])

with tab1:
        statistc = statistcs[statistcs["Day"] == selected_date]
        with st.expander("Data",expanded=True):
                st.markdown(f"<h3>{selected_date}</h3>",
                            unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                col1.metric("New case", f"{statistc['new_cases'].values[0]}")
                col2.metric("New Death", f"{statistc['new_deaths'].values[0]}",)
                col3.metric("New Vaccination", f"{statistc['new_vaccinations'].values[0]}")

        # Figure dash
        st.plotly_chart(plot.plot_dashmap(dash_data),use_container_width=True)
        


with tab2:
        st.markdown(
                f"<h1 style='color:#025192'>{selected_country}<h1/>",
                unsafe_allow_html=True
        )
        
        # Figure rader
        st.plotly_chart(plot.plot_rader(rader,country=selected_country),use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
                st.plotly_chart(plot.plot_ndnv(rader_line,selected_country),use_container_width=True)
        with col2:
                st.plotly_chart(plot.plot_ncnv(rader_line,selected_country),use_container_width=True)

