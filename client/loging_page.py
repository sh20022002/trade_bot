import streamlit as st
import bcrypt
import keyboard, os, psutil
import register_page, app, client

def landing_page():
    """
    Displays the landing page of the SmartTraid application.
    """
    st.title("SmartTraid")
    st.title("The Future of Trading.")
    

def loging_page():
    """
    Displays the login page of the SmartTraid application.
    Allows users to enter their username and password to login.
    """
    st.title("SmartTraid")
    st.title("The Future of Trading.")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("register"):
        register_page.register_page()

    if st.button("Login"):
        response = client.send_request('login', {'username': username, 'password': password})
        if response['status'] == 'success':
            app.client_page(response['messege'], response['compenies'])
        else:
            st.error("Invalid username or password")

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





 