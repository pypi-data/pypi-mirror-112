import streamlit as st

from . import api

def st_app():
    st.title('RasPi-Node Sensor Board')

    # get all sensors
    sensors = api.collection.get_sensor(

if __name__ == '__main__':
    st_app()