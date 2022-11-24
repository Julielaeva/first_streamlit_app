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

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

#streamlit.text(fruityvice_response.json()) 

#from nested semi structured jsot to a flat table
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#to screen
streamlit.dataframe(fruityvice_normalized)
