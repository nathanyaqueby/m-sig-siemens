import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="Agriculture", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("# 🌱 Agricultural Production")
# sidebar
with st.sidebar.form(key='Form1'):
    st.title("🌏 Energy efficiency")
    st.image("charts sig/1.png", width=250)
    st.markdown("Energy efficiency is the goal of reducing the amount of energy required to provide products and services. "
                "Energy efficiency is also a resource that can be used to provide other services, such as providing "
                "electricity during times of peak demand.")
    
    st.title("🌏 Gas efficiency")
    st.image("charts sig/2.png", width=250)
    st.markdown("Gas efficiency is the goal of reducing the amount of gas required to provide products and services.")

    generator = st.form_submit_button(label='Download the report')	
st.write(
    """This chart shows the Gross Agricultural Production of various countries from 1961 to 2013. It is based on data from the United Nations."""
)


@st.cache_data
def get_UN_data():
    AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")


try:
    df = get_UN_data()
    countries = st.multiselect(
        "Choose countries", list(df.index), ["China", "United States of America"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        data /= 1000000.0
        st.write("### Gross Agricultural Production ($B)", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )