import streamlit as st
import os


def register_page():
    """
    This function displays a registration page for the SmartTraid application.
    Users can input their personal information and register for an account.
    """

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
    password = st.text_input("Password")
    confirm_password = st.text_input("Confirm Password")

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
                    pg = st.navigation([st.Page("register_page.py"), st.Page("loging_page.py")])
                    pg.run()


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
                        
    
