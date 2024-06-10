import streamlit as st
import bcrypt

def landing_page():
    st.title("Trading Platform")
    

def loging_page():
    st.title("Trading Platform")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("register"):
        st.sw


    if st.button("Login"):
        if username == 'admin' and password == 'admin':
            st.success("Logged in")
        else:
            st.error("Invalid username or password")

def generate_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def register_page():
    st.title("Trading Platform")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')


    server_response = None # wait for response from server

    if st.button("Register"):
        # add the user to the database
        # wait for response
        if password == confirm_password and server_response == 'success':
            st.success("Registered")
        else:
            st.error("Passwords do not match")