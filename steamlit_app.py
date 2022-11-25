import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()



#import streamlit
streamlit.title("My Mom's new healthy diner menu")
streamlit.header('🥗🐔 Breakfast Favorites 🥑🍞')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
 
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
friuts_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[friuts_selected]
#my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#From the fruitvise website

#creating function to get data from fruitvise website
def get_fruitvise_data(this_fruit_choice):
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) #from nested semi structured json to a flat table
 return fruityvice_normalized
  
 
streamlit.header("Fruityvice Fruit Advice!")
try:
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 if not fruit_choice:
  streamlit.error('Please select a fruit to get information')
 else:
  back_from_function = get_fruitvise_data(fruit_choice)
  #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) #from nested semi structured json to a flat table
  #streamlit.dataframe(fruityvice_normalized) #to screen
  streamlit.dataframe(back_from_function) #to screen
  
  
except URLError as e:
 streamlit.error()
 
 
 
#streamlit.write('The user entered ', fruit_choice)
#streamlit.text(fruityvice_response.json()) 





#streamlit.stop()

#import snowflake.connector
#my_data_row = my_cur.fetchone()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")




streamlit.header("The fruit load list contains:")
#snowflake related function
def get_friut_load_list():
 with my_cnx.cursor() as my_cur:
  my_cur.execute("select * from FRUIT_LOAD_LIST")
  return my_cur.fetchall()
 
#Add a button to load the fruit
if streamlit.button('Get fruit load list'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_friut_load_list()
 streamlit.dataframe(my_data_row)


#allow the end user to add a fruit to the list
add_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.text('Thanks for adding' + ' ' + add_fruit)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
