import time
import pandas as pd
import seaborn as sns
import streamlit as st

from Home import footer_section

# ------ Hide Streamlit elements ------
hide_st_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

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
    df = pd.read_csv(upload_file)  # type: ignore
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

    # Create a section for the dataframe data types
    st.header('Data Types of Dataframe')
    st.write(df.dtypes)

    # Plot the data Pair Plot
    st.header('Pair Plot of Data')
    sns.set_theme(style="ticks")
    fig = sns.pairplot(df)
    if fig:
        left_column, right_column = st.columns(2, gap="medium", vertical_alignment="center")
        with left_column:
            st.write("Choose variable for data colored mapping:")
        with right_column:
            user_input = st.text_input("", placeholder="Type in...")
        if user_input:
            fig = sns.pairplot(df, hue=user_input)
    st.pyplot(fig)
else:
    st.write('Please upload a .csv file first.')

footer_section()
