#to stop previus trouble shoot
#streamlit.stop()
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
#adding def define what get_fruityvice_data is going to mean
def get_fruityvice_data (this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please select the fruit to get information:")
  else:
    back_from_function =get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  stremlit.error()
#importing snowflake 
#streamlit.stop()
streamlit.header("Fruit load list contains:")
def get_fruit_load_list():
 
  with my_cnx.cursor() as my_cur:
       my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
       return my_cur.fetchall()
    #add a button to load
if streamlit.button('Get friut load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  
def insert_row_snowlake(new_fruit):
  with my_cnx.cursor() as my_cur:
       my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
       return "Thanks for adding fruit " + new_fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?') 
if streamlit.button('Add a Fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function=insert_row_snowlake(add_my_fruit)
  streamlit.text(back_from_function)
  



