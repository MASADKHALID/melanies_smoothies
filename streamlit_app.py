# Import python packages
import streamlit as st

# Write directly to the app
st.title("Example Streamlit App :balloon:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

cnx =st.connection("snowflake")
session=cnx.session()
from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
        'choose up to 5 ingredients:',
        my_dataframe
)
if ingredients_list:
    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit+' '
    st.write(ingredients_string)

 
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
    values ('""" + ingredients_string + """')"""
    
    #st.write(my_insert_stmt)
    time_to_insert=st.button('submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
