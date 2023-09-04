import pandas as pd
import streamlit as st
import psycopg2
import re
import random
from streamlit_option_menu import option_menu
# -------------CONNECTING WITH POSTGRES SQL DATABASE-------------#
conn=psycopg2.connect(host = "localhost",
                      user = "postgres",
                      password = "Kavidhina@5566",
                      port = 5432,
                      database = "e_commerce_site")
mycursor = conn.cursor()

#================Assenment_Title============#
styled_text = "<p style='font-size: 20 px; font-weight: bold;color:magenta;'>E-Commerce Website:</p>"
st.markdown(styled_text, unsafe_allow_html=True)

#================Page_Creation============#
with st.sidebar:
    options = ["User","Admin"]
    page = st.selectbox("Select the page",options)
    
#================Login_Page============#
if page == "User":
    condition = False
    with st.form(key= 'Submit',clear_on_submit=False) :
        user_name_1 = st.text_input("Username")
        password_1 = st.text_input("Password",type="password")
        submit_button = st.form_submit_button("Login")
        if 'load_state' not in st.session_state:
            st.session_state.load_state = False
            load=st.session_state.load_state
        if submit_button or load : 
          
          try:
            #this is input cardholder
            query =f"select * from user_details where username= '{user_name_1}'"
            mycursor.execute(query)
            result = mycursor.fetchall()
            z=result[0][0]
            y= result[0][1]
            if 'give_rating' not in st.session_state:
                st.session_state.give_rating = True
            if user_name_1 == z and password_1==y : # if the condition is true, then we can consider it is duplicard card
                st.success("login successfully completed")
    #================Product_Review==============#
                tab1,tab2,tab3=st.tabs(["page1",'page2',"page3"])
                with tab1:
                    query1 = "select barcode from product_details" 
                    mycursor.execute(query1)
                    sql_result = mycursor.fetchall()
                    for i in range(5):
                        ran=random.randint(1,100)
                        query1 = f"select name,barcode,brand,description,price,available from product_details where barcode = '{sql_result[i][0]}'" 
                        mycursor.execute(query1)
                        sql_result1 = mycursor.fetchall()
                        df = pd.DataFrame(sql_result1, columns=[desc[0] for desc in mycursor.description])
                        for i in range(len(df.columns)):
                            st.write(f"{df.columns[i]} : {df.iloc[0,i]}")
                            #with st.form(key= 'Submit',clear_on_submit=True):
                        colb1,colb2 = st.columns([1,1])
                       
                        with colb1:
                                   give_rating_option = st.selectbox(f"Give Rating {ran}", ['',1, 2, 3, 4, 5], key=f"Give_Rating_{ran}")
                                   if 'give_rating' not in st.session_state:
                                       st.session_state.give_rating = give_rating_option
                                   
                        with colb2:
                               add_comments_option = st.selectbox(f"Add Comments {ran}", ['',"Yes", "No"], key=f"Add_Comments_{ran}")
                               if 'add_comments' not in st.session_state:
                                   st.session_state.add_comments = add_comments_option
                        st.write(st.session_state.values())
                        submit_button = st.form_submit_button(f"submit review and rating {ran}")
                        if submit_button :
                            st.write(add_comments_option)
                        st.write("") 
            else:
              st.error("invalid username or password")
          except:
                st.error("invalid username or password")


#================New_user_Registration============#
    st.write("Are you a New User ? ")
    tab1,tab2 = st.tabs(["Register_Here"," "])
    with tab1:
        col3,col4 = st.columns([1,1])
        with col3:
            with st.form(key= 'submit',clear_on_submit=True) :
                user_name = st.text_input(" Enter the Username", key="UserName") 
                password = st.text_input("Enter the Password",type="password")
                password_2 = st.text_input("Confirm the Password",type="password")
                submit_button = st.form_submit_button("submit")
                registration = False
                if password == password_2:
                    #================== Password validation==================#
                    if submit_button:
                        if len(password) >= 8 and re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
                            st.success("Registration completed successfully!") 
                            registration= True
                        else:
                            st.error("Password requirements not met:")
                            if len(password) < 8:
                                st.write("Password should be min 8 characters.")
                            if not re.match("^(?=.*[A-Za-z])(?=.*\d)", password):
                                st.write("Password should be alphanumeric.")
                            special_characters_count = len(re.findall(r"[@$!%*#?&]", password))
                            if special_characters_count < 1 or special_characters_count > 3:
                                st.write("Minimum one and maximum three special characters (@$!%*#?&) are required.")
                            if not any(char.isupper() for char in password):
                                st.write("Minimum one uppercase character is required.")
                else:
                    st.error("password mismatch")
                if registration== True:
                    insert_query = "INSERT INTO user_details  VALUES (%s,%s)"
                    mycursor.execute(insert_query, (user_name, password_2))
                    # Commit the changes and close the connection
                    conn.commit()          
        #========Password_Instruction===========
            with col4:
                st.write("Instruction for while entering the password :")
                st.write("1.'Password should be min 8 character'")
                st.write("2.'Password should be  alpha numeric'")
                st.write("3.'Minimum one special character, maximum three'")
                st.write("4.'Minimum one uppercase character'")
if page == "Admin":
    with st.form(key= 'submit',clear_on_submit=True) :
        user_name_2 = st.text_input("Username")
        password_2 = st.text_input("Password",type="password")
        submit_button = st.form_submit_button("Submit")
        condition=False

        admin_user = "admin"
        admin_password = "admin@123"
        try:
            if user_name_2 == admin_user and password_2==admin_password : # if the condition is true, then we can consider it is duplicard card
                condition= True
        except:
            pass
        if condition:
            try:
                upload_product_details = st.file_uploader("upload here",label_visibility="collapsed",type=["csv"])
                # Read the uploaded CSV file into a DataFrame with the current encoding
                df=pd.read_csv(upload_product_details)
                result= data_to_insert = [tuple(row) for row in df.values]
                query1 = "select barcode from product_details" 
                mycursor.execute(query1)
                sql_result = mycursor.fetchall()
                duplicate_barcode = []
                for i in range(len(sql_result)):
                    for j in range(len(result)):
                        if sql_result[i][0] == result[j][1] :
                            #st.write(f"{j+1}. {result[j][1]} this barcode product already available")
                            duplicate_barcode.append(result[j][1])
                for i in result:  
                    if i[1] in duplicate_barcode: 
                        result.remove(i)
                for i in result:  
                    if i[1] in duplicate_barcode: 
                        result.remove(i)
                for i in result:  
                    if i[1] in duplicate_barcode: 
                        result.remove(i)
                for i in result:  
                    if i[1] in duplicate_barcode: 
                        result.remove(i)
                if result !=[] :
                    insert_query = "INSERT INTO product_details  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    mycursor.executemany(insert_query, result)
                    # Commit the changes and close the connection
                    conn.commit()
                    st.success("product details are successfuly uploaded !!!")
                else:
                    st.success("product details are successfuly uploaded !!!")
            except ValueError:
                   pass


    
        

        
    