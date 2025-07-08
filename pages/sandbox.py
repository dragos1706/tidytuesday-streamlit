import streamlit as st
import pandas as pd
from datetime import time, datetime


df = pd.DataFrame({
     'first column': [1, 2, 3, 4],
     'second column': [10, 20, 30, 40]
     })
st.write(df)


age = st.slider('How old are you?', 0, 130, 25)
st.write("I'm ", age, 'years old')

st.write('**Range slider**')
values = st.slider(
     'Select a range of values',
     0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)

st.write('**Range time slider**')
appointment = st.slider(
     "Schedule your appointment:",
     value=(time(11, 30), time(12, 45))
     )
st.write("You've selected an appointment during:", appointment[0], "and", appointment[1])


st.subheader('Datetime slider')

start_time = st.slider(
     "When do you start?",
     value=datetime(2020, 1, 1, 9, 30),
     format="MM/DD/YY - hh:mm")
st.write("Start time:", start_time)