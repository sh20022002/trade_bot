import streamlit as st
import os
import client, loging_page
from datetime import date, timedelta


def register_page():
    """
    This function displays a registration page for the SmartTraid application.
    Users can input their personal information and register for an account.
    """

    st.title("SmartTraid")
    st.title("The Future of Trading.")
    st.subheader("Sign Up")
    first_name = st.text_input("Name", key='first_name')
    last_name = st.text_input("Last Name", key='last_name')
    ID = st.text_input("ID", key='ID')
    date_of_birth = st.date_input("Date of Birth",max_value=date.today() - timedelta(days=365*18), min_value=date.today() - timedelta(days=365*100), key='date_of_birth')
    profetion = st.text_input("Profetion")
    bank_account_number = st.text_input("Bank Account Number", key='bank_account_number')
    bank = st.text_input("Bank", key='bank')
    email = st.text_input("Email",  key='email')
    phone_number = st.text_input("Phone Number", key='phone_number')
    address = st.text_input("Address", key='address')
    city = st.text_input("City", key='city')
    country = st.text_input("Country", key='country')
    postal_code = st.text_input("Postal Code", key='postal_code')
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
            if chack_password(password):
                response = client.send_request('register', {'first_name': first_name, 'last_name': last_name, 'ID': ID, 'date_of_birth': date_of_birth, 'profetion': profetion, 'bank_account_number': bank_account_number, 'bank': bank, 'email': email, 'phone_number': phone_number, 'address': address, 'city': city, 'country': country, 'postal_code': postal_code, 'password': password})
                if response['status'] == 'success':
                    st.success("Registered")
                    login_page.go_to_login()


                else:
                    st.error("Failed to register. Please try again.") 
            else:
                st.error("Password must contain at least 8 characters, one uppercase, one lowercase, one digit, and one special character")         

    
def chack_password(password):
    if len(password) >= 8:
        if any(char.isupper() for char in password):
            if any(char.islower() for char in password):
                if any(char.isdigit() for char in password):
                    if any(char in '!@#$%^&*()' for char in password):
                        return True 
    return False
                        
    
