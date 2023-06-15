import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Police Incident Dashboard in San Francisco",
                   page_icon="bar_chart:",
                   layout="wide")

# Base de datos:

@st.cache_data

def data():
    df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")
    return df

df = data()

# ---- SIDEBAR ----
#Filtros
st.sidebar.header("Please filter here:")
Year = st.sidebar.multiselect(
    "Select Year:",
    options=df["Incident Year"].unique(),
    default=df["Incident Year"].unique()
)

Resolution = st.sidebar.multiselect(
    "Select Resolution:",
    options=df["Resolution"].unique(),
    default=df["Resolution"].unique()
)

PoliceDistrict = st.sidebar.multiselect(
    "Select District:",
    options=df["Police District"].unique(),
    default=df["Police District"].unique()
)

DayWeek = st.sidebar.multiselect(
    "Select Day of Week:",
    options=df["Incident Day of Week"].unique(),
    default=df["Incident Day of Week"].unique()
)


df_filtros = df.query(
    '`Incident Year` == @Year & `Resolution` == @Resolution & `Police District` == @PoliceDistrict & `Incident Day of Week` == @DayWeek'
)


# ---- MAINPAGE ----
st.title(":bar_chart: Police Incident Dashboard")
st.markdown("##")

# Gráficas

# 1 mapa
fig2 = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="Incident Category",
                        color_discrete_sequence=["red"], zoom=10)

fig2.update_layout(
    mapbox_style="carto-positron",
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)
st.plotly_chart(fig2, use_container_width=True)

# 2
df_count = df_filtros["Incident Day of Week"].value_counts().reset_index()
df_count.columns = ["Incident Day of Week", "Count"]
fig = px.bar(df_count, x="Incident Day of Week", y="Count")
fig.update_layout(
    title="Day of Week",
)
fig.update_traces(marker_color='red')


# 3
df_count1 = df_filtros["Incident Category"].value_counts().reset_index()
df_count1.columns = ["Category", "Count"]
fig3 = px.bar(df_count1, x="Category", y="Count")
fig3.update_layout(
    title="Category",
)
fig3.update_traces(marker_color='red')

# 4
df_count2 = df_filtros["Resolution"].value_counts().reset_index()
df_count2.columns = ["Resolution", "Count"]
red_colors = ["#FF0000", "#FF3333", "#FF6666", "#FF9999", "#FFCCCC"]
fig4 = px.pie(df_count2, values="Count", names="Resolution")
fig4.update_layout(
    title="Resolution",
)
fig4.update_traces(marker=dict(colors=red_colors))

# 5
df_count3 = df_filtros["Incident Year"].value_counts().reset_index()
df_count3.columns = ["Incident Year", "Count"]
fig5 = px.line(df_count3, x="Incident Year", y="Count")
fig5.update_layout(
    title="Year",
)
fig5.update_traces(line=dict(color='red'))


# Styling
pt1, pt2 = st.columns(2)

pt1.plotly_chart(fig, use_container_width=True)
pt1.plotly_chart(fig3, use_container_width=True)


pt2.plotly_chart(fig4, use_container_width=True)
pt2.plotly_chart(fig5, use_container_width=True)

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

st.markdown(hide_st_style, unsafe_allow_html=True)