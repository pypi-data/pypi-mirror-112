import pandas as pd
import numpy as np
import streamlit as st
import time
import plotly.express as px
import matplotlib.pyplot as plt
import json
import altair as alt
import getpass
# pwd = getpass.getpass("passsword:")
from toolkit_w.snowflake.snowflakeq import Snowflakeq
SQ = Snowflakeq()
st.title('Analytics Dashboard')

# Draw a title and some text to the app:
'''
Analytics Dashboard
'''
import streamlit as st

class MultiApp:
    """
    Framework for combining multiple streamlit applications.
    """
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):

        app = st.sidebar.selectbox(
            'Navigation',
            self.apps,
            format_func=lambda app: app['title'])


        # customer = st.sidebar.selectbox(
            # 'Design Partner',
            # ['SAFARI_LTD','DAILY_PAPER'])



        # app = st.sidebar.radio(
        #     'Go To',
        #     self.apps,
        #     format_func=lambda app: app['title'])

        app['function']()





