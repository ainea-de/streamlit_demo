import streamlit as st
import pandas as pd
import numpy as np

def is_valid_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def format_numbers(x):
    # ist x eine Zahle
    if is_valid_float(x):
        if abs(float(x)) >= 1000: # große Zahlen (achtung performance kann negativ sein)
            return str("{:,}".format(round(abs(float(x)))))
        else:
            return str(round(float(x),2))
    else:
        return x

st.title('Sammelstiftungen')

# Specify your excel file's name
file_name = './bericht/stiftungen.xlsx'
# Read the Excel file
df = pd.read_excel(file_name, sheet_name="stiftungen")
# Get the data from the column
folder_names = list(df['Name:'])

df_gf = pd.read_excel("./bericht/list_gf.xlsx", sheet_name = "detail")


# Create a dropdown menu
selected_item = st.selectbox("Wahl SST:", folder_names)


# create an empty dataframe to store the input text
if selected_item:
    print(selected_item)
    
    # Display link to a PDF file
    st.write(f'[GB 2022](https://ainea.de/wp-content/uploads/ainea/bericht/{selected_item}/2022.pdf)', end="")
    st.write(f'[GB 2021](https://ainea.de/wp-content/uploads/ainea/bericht/{selected_item}/2021.pdf)', end="")
    st.write(f'[GB 2020](https://ainea.de/wp-content/uploads/ainea/bericht/{selected_item}/2020.pdf)')
    
    df2 = pd.read_excel('./bericht/info.xlsx', sheet_name=selected_item, header=None)
    df2 = df2.astype(str)
    my_gf = df2.loc[df2[0] == "Geschäftsführer", 1].values[0]
    # check if name of geschäftsführer can be found
    my_gf_info = df_gf.loc[df_gf["name"]==my_gf,:]
    # if name is not found give person who works there
    if my_gf_info.empty:
        filtered_rows = df_gf[df_gf["Total"].str.contains(selected_item.replace("-", " "), case=False)]
        if not filtered_rows.empty:
            my_gf_info = filtered_rows.iloc[0,:]
    #df = pd.DataFrame(columns=['Input Text'])
    # select output (not too many nans)
    df2_select = df2[0:21]
    df2_select.drop(3, axis=1, inplace=True) # drop year 3
    df2_select.replace("nan", np.nan, inplace=True) # replace nan to drop certain rows
    df2_select = df2_select.dropna(thresh=3) # 4 columns - 2 NaNs + 1 treshold
    df2_select.replace(np.nan, "", inplace=True)
    #st.markdown(f'<style>.dataframe {{ width: 1000px; height: 800px; }}</style>', unsafe_allow_html=True)

    # replace column names with first row
    new_columns = df2_select.iloc[0]
    df2_select.columns = [str(e) for e in new_columns]
    df2_select = df2_select.iloc[1:].reset_index(drop=True)
    df2_select = df2_select.applymap(format_numbers)
    st.dataframe(df2_select, use_container_width=True,hide_index=True,)
    
    #styled_dataframe = df2_select.style.hide_index().hide_columns()
    #styled_dataframe = df2_select.style.set_table_attributes(f'width="{600}" height="{1000}"')
    #st.write(styled_dataframe, unsafe_allow_html=True)

    st.markdown("---")
    # show gf information
    pd.set_option("display.max_colwidth", None)
    gf_text = "<table>"
    if not my_gf_info.empty:
        my_attr_list = ["name","job","location","employer","job1","job2","edu1","company_url","linkedin_link","Birthday"] 
        for attr in my_attr_list:
            try:
                attr_str = my_gf_info[attr].to_string(index=False)
            except:
                attr_str = str(my_gf_info[attr])
            if attr_str!="NaN" and attr_str!="nan":
                #st.write(attr +": "+ attr_str,unsafe_allow_html=True)
                gf_text = gf_text + "<tr><td>" + attr +"</td><td>"+ attr_str + "</td></tr>"
        #st.markdown("[link](" + my_gf_info["linkedin_link"].to_string(index=False)+ ")")
        try:
            # assume education = 25 years
            age = str(2023 - int(my_gf_info["edu3"][:4]) + 30)
            gf_text = gf_text + "<tr><td>Alter (ca.)</td><td>"+ age + "</td></tr>"
            #gf_text = gf_text + "<br>Alter (ca.):" + age
            #st.write("Alter (ca.):" + age)        
        except:
            print("Alter unbekannt.")
        try:
            image_url = my_gf_info["get_image_link"].to_string(index=False)
        except:
            image_url = str(my_gf_info["get_image_link"])
        if image_url[:4] == "http":
        #    print(image_url)
        #    iframe_code = f'<iframe src="{image_url}" width="1000" height="600"></iframe>'
            #st.markdown(iframe_code, unsafe_allow_html=True)            
            st.image(image_url, width=200)
            #markdown_content = f'url: <a href="{image_url}">LINK</a>'
            #st.markdown(markdown_content, unsafe_allow_html=True)
        else:
            st.write("no image" + image_url)
    gf_text = gf_text + "</table>"
    st.markdown(gf_text, unsafe_allow_html=True)        
    #   st.dataframe(my_gf_info)
    st.markdown("---")
    st.write("Rückversicherung:\n" + str(df2.iloc[28,1]))
    st.markdown("---")
    st.write("Strategie:\n" + str(df2.iloc[29,1]))
    st.markdown("---")
    #gf = df2.iloc[1,1] 
    #if gf in df_gf["Name"].values:
    #    l = df_gf.loc[df_gf["Name"]==gf, "LinkedIn"].values[0]
    #    st.write(l)
        
        

# define the label
st.write('Enter name:')

# define the input field
user_input = st.text_input(label='Notizen:')

# If there is some text, show it
if user_input:
    st.write('You wrote:', user_input)

# define the button
button_clicked = st.button('Submit')

# check if button is clicked
if button_clicked:
    # add the user input to the dataframe
    df.loc[len(df)] = [user_input]
    
    # display the table
    st.table(df)
