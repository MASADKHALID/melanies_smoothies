# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw:Customize Your Smoothie!:cup_with_straw")
st.write(
    """choose the fruit you want in your custome Smoothie"""
)

cnx =st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
        'choose up to 5 ingredients:',
        my_dataframe
        ,max_selection=5
)
if ingredients_list:
    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit+' '
        st.subheader(each_fruit='Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+each_fruit)
        #st.text(fruityvice_response).json()
        fv_df=st.dataframe(data=ruityvice_response.json(), use_container_width=True)
    st.write(ingredients_string)

 
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
    values ('""" + ingredients_string + """')"""
    
    #st.write(my_insert_stmt)
    time_to_insert=st.button('submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



