import streamlit as st
import bcrypt
import keyboard, os, psutil
import register_page, app, client


if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

def go_to_login():
    st.session_state['page'] = 'login'

def go_to_register():
    st.session_state['page'] = 'register'

def go_to_app():
    st.session_state['page'] = 'app'


def loging_page():
    """
    Displays the login page of the SmartTraid application.
    Allows users to enter their username and password to login.
    """
    st.title("SmartTraid")
    st.title("The Future of Trading.")
    username = st.text_input("Username", key='username')
    password = st.text_input("Password", type='password')

    if st.button("register"):
        go_to_register()
        
    if st.button("Login"):
        # chacck if the password is valid
        # has a min and max length for limiting code injection
        min_char = 8
        max_char = 20
        if len(password) <= min_char or len(password) >= max_char:
            st.error("Please enter a valid password")

        elif register_page.chack_password(password) == False:
            st.error("Password must contain at least 8 characters, one uppercase, one lowercase, one digit, and one special character")

        # check if the username is valid and not a code injection
        elif len(username) <= min_char or len(username) >= max_char:
            st.error("Please enter a valid username")

        else:    
            response = client.send_request('login', {'username': username, 'password': password})
            if response['status'] == 'success':
                st.success("login successful!")
                compenys = response['compenys']
                user = response['user']
                go_to_app()
            else:
                st.error("Invalid username or password")

   
if st.session_state['page'] == 'login':
    loging_page()
elif st.session_state['page'] == 'register':
    register_page.register_page()
elif st.session_state['page'] == 'app':
    app.client_page(user, compenys)



 