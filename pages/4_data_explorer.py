import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from deta import Deta

st.set_page_config(st.session_state['page_config'])

# State management
if "file_csv" not in st.session_state:
    st.session_state["file_csv"] = "not done"

def change_file_state():
    st.session_state["file_csv"] = "done"

# Add a title and intro text
st.title('Data Set Explorer')
st.text('This is a web app to explore Data Sets from .csv files')

# Create file uploader object
upload_file = st.file_uploader('Upload a file containing data', on_change=change_file_state)

# Check to see if a file has been uploaded
# if upload_file is not None:
if st.session_state["file_csv"] == "done":
    # Read the file to a dataframe using pandas
    df = pd.read_csv(upload_file) # type: ignore
    progress_bar = st.progress(0)
    for completed in range(100):
        time.sleep(0.03)
        progress_bar.progress(completed + 1)
    st.success('File uploaded successfully')

    # Create a section for the dataframe statistics
    st.header('Statistics of Dataframe')
    st.write(df.describe())

    # Create a section for the dataframe header
    st.header('Header of Dataframe')
    st.write(df.head())

    # Create a section for matplotlib figure
    st.header('Plot of Data')

    fig, ax = plt.subplots(1,1)
    count = df['title'].count()
    ax.bar(height=8, x=df['type'], y=count)
    ax.set_xlabel('type')
    ax.set_ylabel('kiekis')

    st.pyplot(fig)

else:
    st.write('Please upload a .csv file')
