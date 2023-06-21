import os
import sys
import pandas as pd
import streamlit as st
from tkinter_folder import folder_select
from pathlib import Path
from data_analysis import analyze_data
import numpy as np
import plotly.express as px

if 'directory' not in st.session_state: 
    st.session_state['directory'] = os.path.abspath('.')
    st.session_state['data'] = None
st.set_page_config(layout="wide")


def side_bar_content():
    st.sidebar.write('Select your data folder')
    get_directory = st.sidebar.button('Select folder')
    if get_directory:
        st.session_state['directory'] = folder_select()
    st.sidebar.write(st.session_state['directory'])


def main():
    side_bar_content()
    col1, col2 = st.columns([1,1])
    file_selected = col1.selectbox('Select a csv file',
                 os.listdir(st.session_state['directory']))
    if col1.button('Analyze'):
        file_path = Path(st.session_state['directory']) / Path(file_selected)
        try:
            st.session_state['data'] = pd.read_csv(str(file_path))
        except Exception as e:

            col1.error(f"Exception = {e}")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            col1.error(f'Exception Type = {exc_type}, File Name = {fname}, Line No = {exc_tb.tb_lineno}')

        # if st.session_state['data'] is not None:
        #     analyze_data(col1, col2)

    column_dict = st.session_state['data'].dtypes.to_dict()
    # with col1.expander('Pair Plot',False):
    #     sns.pairplot(st.session_state['data'])
    #     st.pyplot(plt)
    # fields = []    
    # for k,v in column_dict.items():
    #     fields.append(col2.text_input(f'{k}, {v}'))
    
    with col1.expander('Describe'):
        st.write(st.session_state['data'].describe())
    
    with col2.expander('Missing values'):
        st.write(st.session_state['data'].isnull().sum())
    
    with col1.expander('Box plot'):
        column_to_plot = \
            st.selectbox('Choose column to plot',
                         st.session_state['data'].select_dtypes(include=np.number).columns.tolist())
        st.plotly_chart(px.box(st.session_state['data'],column_to_plot),use_container_width=True)

    with col2.expander('Histogram'):
        column_to_plot = \
            st.selectbox('Choose column to plot',
                         st.session_state['data'].columns.tolist())
        st.plotly_chart(px.histogram(st.session_state['data'],column_to_plot),use_container_width=True)
  
    with col1.expander('Correlation'):
        st.plotly_chart(px.imshow(st.session_state['data'].select_dtypes(include=np.number).corr(),text_auto=True),use_container_width=True)
if __name__ == '__main__':
    main()