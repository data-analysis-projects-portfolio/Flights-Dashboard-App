import streamlit as st
import pandas as pd
from dbhelper import Database
import plotly.graph_objects as go

db = Database()
db.load_data_db()
db.close()
st.sidebar.title('Flights Analytics')
user_option = st.sidebar.selectbox('Menu', ['Select', 'Check Flights', 'Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flight Information')
    col1, col2 = st.columns(2)
    cities = db.fetch_city_names()
    with col1:
        source = st.selectbox('Source', cities)
    with col2:
        destination = st.selectbox('Destination', cities)
    if st.button('Search'):
        flight_info = db.fetch_all_flights(source, destination)
        if flight_info.empty:
            st.warning(f"There are no flights between {source} and {destination}")
        else:
            st.dataframe(flight_info)
elif user_option == 'Analytics':
    st.title('Analytics')
    flight_count = db.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(labels=flight_count['Airline'],
               values=flight_count['number_of_flights'],
               hoverinfo="label+percent",
               textinfo="value")
    )
    st.header("Airline Pie Chart")
    st.plotly_chart(fig)

    flight_frequency = db.busy_airport()
    fig = go.Figure(
        go.Bar(
            x=flight_frequency['Source'],  # x-axis labels
            y=flight_frequency['aircraft_movements'],  # y-axis values
            hoverinfo="x+y",  # correct format for hover text
            text=flight_frequency['aircraft_movements'],  # show values on bars
            textposition='auto'  # auto places the text nicely
        )
    )
    fig.update_layout(
        title="Flight Frequency by Airport",
        xaxis_title="Airport",
        yaxis_title="Frequency of Aircraft"
    )
    st.header("Aircraft Frequency Bar Chart")
    st.plotly_chart(fig)

    daily_frequency = db.daily_frequency()
    fig = go.Figure(
        go.Bar(
            x=daily_frequency['Date_of_Journey'],  # x-axis labels
            y=daily_frequency['daily_number_of_flights'],  # y-axis values
            hoverinfo="x+y",  # correct format for hover text
            text=daily_frequency['daily_number_of_flights'],  # show values on bars
            textposition='auto'  # auto places the text nicely
        )
    )
    fig.update_layout(
        title="number_of_flights_per_day",
        xaxis_title="Date_of_Journey",
        yaxis_title="daily_number_of_flights"
    )
    st.header("Frequency of number of flights per day Line Chart")
    st.plotly_chart(fig)

else:
    st.title('An Overview about the Application')
    st.info("""
    This app shows flight analytics and route information.
    - View busiest airports
    - Explore flight frequency trends
    - Select two cities to see direct routes between them
    """)


