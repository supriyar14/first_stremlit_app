#to stop previus trouble shoot
streamlit.stop()
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My MOM  healthy food')
streamlit.header('Breakfast')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)
#new fetch from api
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
streamlit.text(fruityvice_response.json())

# normalize jason
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# pandas dataframe
streamlit.dataframe(fruityvice_normalized)
#importing snowflake 

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("Fruit load list contains:")
streamlit.dataframe(my_data_rows)
streamlit.header("Fruityvice Fruit Advice!")
fruit_add = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding fruit ', fruit_add)
#
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")

