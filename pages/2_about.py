import streamlit as st

st.title("About")
st.write("This is the about page")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.link_button("Home", url="/home")
    with right_column:
        st.metric(label="Temperature", value="60 Celsius", delta="3 Celsius")

with st.container():
    st.write("---")
    with st.expander("Click to read more"):
        st.write("Hello, here are more details on this topic that you are interested in.")
