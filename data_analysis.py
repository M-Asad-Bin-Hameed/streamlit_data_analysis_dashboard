import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt

def analyze_data(col1,col2):
    column_dict = st.session_state['data'].dtypes.to_dict()
    # with col1.expander('Pair Plot',False):
    #     sns.pairplot(st.session_state['data'])
    #     st.pyplot(plt)
    fields = []
    
    for k,v in column_dict.items():
        fields.append(col2.text_input(f'{k}, {v}'))
    
    with col1.expander('Describe'):
        st.write(st.session_state['data'].describe())
    
    with col1.expander('Missing values'):
        st.write(st.session_state['data'].isnull().sum())
    
    with col1.expander('Box plot'):
        column_to_plot = \
            st.selectbox('Choose column to plot',
                         st.session_state['data'].select_dtypes(include=np.number).columns.tolist())
        st.plotly_chart(px.box(st.session_state['data'],column_to_plot),use_container_width=True)