import streamlit as st
import keyboard, os, psutil


st.title("SmartTraid")
st.title("The Future of Trading.")
st.subheader("Sign Up")
first_name = st.text_input("Name")
last_name = st.text_input("Last Name")
ID = st.text_input("ID")
date_of_birth = st.date_input("Date of Birth")
profetion = st.text_input("Profetion")
bank_account_number = st.text_input("Bank Account Number")
bank = st.text_input("Bank")
email = st.text_input("Email")
phone_number = st.text_input("Phone Number")
address = st.text_input("Address")
city = st.text_input("City")
country = st.text_input("Country")
postal_code = st.text_input("Postal Code")
password = st.text_input("Password", type='password')
confirm_password = st.text_input("Confirm Password", type='password')

# create a post request to the server
# send the user data to the server



if st.button("Register"):
    # add the user to the database
    # wait for response
    if password != confirm_password:
        st.error("Passwords do not match")
    else:
        response = client.send_request('register', {'first_name': first_name, 'last_name': last_name, 'ID': ID, 'date_of_birth': date_of_birth, 'profetion': profetion, 'bank_account_number': bank_account_number, 'bank': bank, 'email': email, 'phone_number': phone_number, 'address': address, 'city': city, 'country': country, 'postal_code': postal_code, 'password': password})
        if response['status'] == 'success':
            st.success("Registered")
            loging_page.loging_page()  
    
        
        
    else:
        

# exit button


exit_app = st.button("Shut Down")

if exit_app:

    # Give a bit of delay for user experience

    time.sleep(5)

    # Close streamlit browser tab

    keyboard.press_and_release('ctrl+w')

    # Terminate streamlit python process

    pid = os.getpid()

    p = psutil.Process(pid)
    p.terminate()
 