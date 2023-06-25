import os
import sys
import pandas as pd
import streamlit as st
from tkinter_folder import folder_select
from pathlib import Path
from data_analysis import data_analysis_class
import numpy as np
import plotly.express as px

if 'directory' not in st.session_state: 
    st.session_state['directory'] = os.path.abspath('.')
    st.session_state['data'] = None
    st.session_state['data_class'] = None
st.set_page_config(layout="wide")


def side_bar_content():
    st.sidebar.write('Select your data folder')
    get_directory = st.sidebar.button('Select folder')
    if get_directory:
        st.session_state['directory'] = folder_select()
    st.sidebar.write(st.session_state['directory'])


def tab1_content():
    col1, col2 = st.columns([1,1])
    file_selected = col1.selectbox('Select a csv file',
                 os.listdir(st.session_state['directory']))
    if col1.button('Analyze'):
        file_path = Path(st.session_state['directory']) / Path(file_selected)
        try:
            st.session_state['data_class'] = data_analysis_class(file_path)
        except Exception as e:

            col1.error(f"Exception = {e}")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            col1.error(f'Exception Type = {exc_type}, File Name = {fname}, Line No = {exc_tb.tb_lineno}')
    if st.session_state['data_class'] is not None:

        st.sidebar.markdown('### Column dtypes')
        st.sidebar.write(st.session_state['data_class'].get_dtypes())
        with col1.expander('Basic description'):
            st.session_state['data_class'].describe_data()
        
        col2.markdown('### Basic Charts section')
        with col2.expander('Basic plots'):
            graph_column = st.selectbox('Column to use',st.session_state['data_class'].get_column_names())
            box,hist = st.session_state['data_class'].basic_plots(graph_column)
            st.plotly_chart(box,use_container_width=True)
            st.plotly_chart(hist,use_container_width=True)

def main():
    tab1, tab2, tab3 = st.tabs(["Data Loading", "Custom Graph", "Machine Learning"])
    with tab1:
        side_bar_content()
        tab1_content()
    with tab2:
        if st.session_state['data_class'] is not None:
            st.markdown('# Custom chart')     
            graph_to_choose = st.selectbox('Choose the graph type',['Bar','Box','Histogram','Scatter','Line'])
            col1, col2 = st.columns([1,1])
            with col2:
                column_list = st.session_state['data_class'].get_column_names()
                column_list.insert(0,' ')
                x = st.selectbox('X-Column', column_list) 
                y = st.selectbox('Y-Column', column_list)
                
                color = st.selectbox('Column Color',column_list)

            with col1:
                if st.button('Create graph'):
                    try:
                        st.plotly_chart(st.session_state['data_class'].custom_plot(graph_to_choose,
                                                                               x, y, 
                                                                               color),
                                                                               use_container_width=True)
                    except Exception as e:
                        st.error(f"Exception = {e}")
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        col1.error(f'Exception Type = {exc_type}, File Name = {fname}, Line No = {exc_tb.tb_lineno}')

    with tab3:
        if st.session_state['data_class'] is not None:
            st.text_input('Enter target column')

if __name__ == '__main__':
    main()