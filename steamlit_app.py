import streamlit
streamlit.title("My Mom's new healthy diner menu")
streamlit.header('🥗🐔 Breakfast Favorites 🥑🍞')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
 
import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
friuts_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[friuts_selected]
my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#streamlit.text(fruityvice_response.json()) 

#from nested semi structured json to a flat table
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#to screen
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from FRUIT_LOAD_LIST")
#my_data_row = my_cur.fetchone()
my_data_row = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
#streamlit.text("The fruit load list contains:")
streamlit.header("The fruit load list contains:")
#streamlit.text(my_data_row)
streamlit.dataframe(my_data_row)

#allow the end user to add a fruit to the list
add_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.text('Thanks for adding' + ' ' + add_fruit)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
