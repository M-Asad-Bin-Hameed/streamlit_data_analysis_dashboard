import os
import glob
import time
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
import plotly.express as px
import plotly.figure_factory as ff
from supervised.automl import AutoML
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split


class data_analysis_class:

    def __init__(self, file_path) -> None:
            self.df = pd.read_csv(str(file_path))
            self.automl = None
            self.predictions = None

    def get_dtypes(self):
            return self.df.dtypes.to_dict()

    def correlation_heatmap(self):
        fig = px.imshow(self.df.select_dtypes(include=np.number).corr(),text_auto=True)
        return fig
    def describe_data(self):
        st.markdown('### Data Description: Numeric')
        st.write(self.df.describe())
        st.markdown('### Null values')
        st.write(self.df.isnull().sum().to_dict())

    def get_column_names(self):
        return self.df.columns.tolist()

    def basic_plots(self, column):
        box_plot = px.box(self.df,column)
        hist_plot = px.histogram(self.df,column)
        return box_plot, hist_plot

    def custom_plot(self, graph_name=None, x=None, y=None ,color=None):
        if color == ' ':
            color = None
        if graph_name.lower() == 'bar':
            fig = px.bar(self.df, x, y, color)
        elif graph_name.lower() == 'box':
            fig = px.box(self.df, x)
        elif graph_name.lower() == 'histogram':
            fig = px.histogram(self.df, x)
        elif graph_name.lower() == 'scatter':
            fig = px.scatter(self.df, x, y, color)
        elif graph_name.lower() == 'line':
            fig = px.line(self.df, x, y, color)
        elif graph_name.lower() == 'density heatmap':
            fig = px.density_heatmap(self.df, x, y,color)
        elif graph_name.lower() == 'correlation matrix':
            fig = px.imshow(self.df.select_dtypes(include='number').corr(), text_auto=True)

        return fig

    def show_column_info(self, column_name,col1, col2):
        col_d_type = self.df[column_name].dtype
        if col_d_type == 'float64' or col_d_type == 'int64':
            self._for_numerical_dtype(column_name, col1, col2)
        if col_d_type =='object':
            col1.write('Please convert the column into a specific type')
        if col_d_type =='category':
            self._for_categorical_dtypes(column_name, col1, col2)
        if col_d_type == 'bool':
            self._for_bool_dtype(column_name, col1, col2)
        if col_d_type == 'datetime64[ns]':
            self._for_datetime_dtypes(column_name, col1, col2)
    
    def _for_datetime_dtypes(self, column_name, col1, col2):
        null_value_count = self.df[column_name].isnull().sum()
        col1.write(f'Null values = {null_value_count}')
        if null_value_count>0:
            if col1.button('Drop nulls'):
                self.df.dropna(subset=[column_name],inplace=True)
        col2.write('Year distribution')
        col2.plotly_chart(px.histogram(x = self.df[column_name].dt.year))
        col1.write('Monthly distribution')
        col1.plotly_chart(px.histogram(x = self.df[column_name].dt.month))

    def _for_categorical_dtypes(self,column_name,col1, col2):
        null_value_count = self.df[column_name].isnull().sum()
        col1.write(f'Null values = {null_value_count}')
        if null_value_count>0:
            if col1.button('Drop nulls'):
                self.df.dropna(subset=[column_name],inplace=True)
        col1.write('Unique values')
        col1.write(self.df[column_name].value_counts())
        col2.write('Histogram')
        col2.plotly_chart(px.histogram(self.df,column_name))
        col2.write('Pie chart')
        col2.plotly_chart(px.pie(self.df,column_name))

    def _for_bool_dtype(self, column_name, col1, col2):
        null_value_count = self.df[column_name].isnull().sum()
        col1.write(f'Null values = {null_value_count}')
        if null_value_count>0:
            if col1.button('Drop nulls'):
                self.df.dropna(subset=[column_name],inplace=True)  
        col2.write('Histogram')
        col2.plotly_chart(px.histogram(self.df,column_name))
    
    def _for_numerical_dtype(self,column_name,col1, col2):
        null_value_count = self.df[column_name].isnull().sum()
        col1.write(f'Null values = {null_value_count}')
        if null_value_count>0:
            if col1.button('Drop nulls'):
                self.df.dropna(subset=[column_name],inplace=True)

        col1.write('Describe')
        col1.write(self.df[column_name].describe())
        col2.write('Histogram')
        col2.plotly_chart(px.histogram(self.df,column_name))
        col2.write('Box plot')
        col2.plotly_chart(px.box(self.df,column_name))
        col1.write('Dist plot')
        col1.plotly_chart(ff.create_distplot([self.df[column_name]],[column_name]))

    def change_dtype(self, column_name, change_to, date_time_format = None):
        print(date_time_format)
        if change_to == 'datetime64':
            self.df[column_name] = pd.to_datetime(self.df[column_name],format=date_time_format)
        else:
            self.df[column_name] = self.df[column_name].astype(change_to)


##############################################################################################
################################## A U T O M L  (M L J A R) ##################################
##############################################################################################


    def split_data(self, test_size=0.2, column_name=None):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.df.drop(columns=column_name), self.df[column_name], test_size=test_size
        )
    def auto_ml_run(self):
        self.automl = AutoML(
                        algorithms = ['Random Forest', 'CatBoost', 'Neural Network'],
                        explain_level=2,
                        top_models_to_improve=3
                    )
        st.write('Running AutoML, This may take a few minutes')
        t1 = time.time()
        self.automl.fit(self.X_train, self.y_train)
        self.predictions = self.automl.predict_all(self.X_test)
        self.predictions['Ground_truth'] = self.y_test.reset_index(drop=True)
        st.success(f'Done in {round(time.time()- t1,3) }s')
    def show_automl_results(self,result_path = None):
        
        if result_path is None:
            if self.automl is None:
                st.error('AutoML not run or found')
                return
            self.result_path =  self.automl._get_results_path()
        else:
            self.result_path = result_path

        directories = next(os.walk(self.result_path))[1]

        for file in glob.glob(f'{str(Path(self.result_path)/Path("*.csv"))}'):
            with st.expander('LeaderBoard'):
                st.write(pd.read_csv(file))
        with st.expander('Model Comparison files'):
            col1,col2 = st.columns([1,1])
            count = 0
            for image in glob.glob(f'{str(Path(self.result_path)/Path("*.png"))}'):
                if count%2==0:
                    col1.markdown(f'### {os.path.splitext((os.path.basename(image)))[0]}')
                    col1.image(image)
                else:
                    col2.markdown(f'### {os.path.splitext((os.path.basename(image)))[0]}')
                    col2.image(image)
                count+=1
        directory_dict = {}
        for x in directories:
            directory_dict[x] = glob.glob(f'{str(Path(self.result_path) / Path(x))/Path("*.png")}')
        for directory,file_list in directory_dict.items():
            count = 0
            with st.expander(directory):
                col1, col2 = st.columns([1,1])
                for file in file_list:
                    if count%2 == 0:
                        col1.markdown(f'### {os.path.splitext((os.path.basename(file)))[0]}')
                        col1.image(file)
                    else:
                        col2.write(f'### {os.path.splitext((os.path.basename(file)))[0]}')
                        col2.image(file)
                    count+=1

    def show_predictions(self):
        if self.predictions is None:
            st.error('No AutoML model found')
        else:
            st.write(self.predictions)