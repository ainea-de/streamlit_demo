import streamlit as st
import pandas as pd

# create an empty dataframe to store the input text
df = pd.DataFrame(columns=['Input Text'])

# define the label
st.write('Enter name:')

# define the input field
user_input = st.text_input(label='')

# define the button
button_clicked = st.button('Submit')

# check if button is clicked
if button_clicked:
    # add the user input to the dataframe
    df.loc[len(df)] = [user_input]
    
    # display the table
    st.table(df)
