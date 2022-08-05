import streamlit as st
import pandas as pd
import json
import requests  # pip install requests
import streamlit as st
from PIL import Image


# Security
# passlib,hashlib,bcrypt,scrypt
import hashlib


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


# DB Management
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()


# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def main():
    """Stock Prediction Website"""

    st.title("Stock Prediction Website")

    st.markdown("""
		# Trading Through Machine Learning
		We use Machine Learning Algorithm to predict the future price of a stock
		""")
    menu = ["Home or LogOut", "Login  as User", "SignUp as User", "Login As Admin", "SignUp As Admin"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home or LogOut":
        st.subheader("Home")
    elif choice == "Login As Admin":
        st.subheader("Admin Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                task = st.selectbox("Navigation",["homepage","Stockdata"])


    elif choice == "Login  as User":
        st.subheader("User Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:

              st.success("Logged In as {}".format(username))
              task = st.selectbox("Navigation",["homepage","Stockdata","Progress","recommendation","Sto","FuturePrediction","prediction"])
              if task == "FuturePrediction":
			              image = Image.open('1.PNG')
			              st.image(image)
				
				
			              image = Image.open('3.PNG')
			              st.image(image)
				
				
			              image = Image.open('2.PNG')
			              st.image(image)
				
				
			              image = Image.open('4.PNG')
			              st.image(image)

				

            else:
                st.warning("Incorrect Username/Password")





    elif choice == "SignUp as User":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
    elif choice == choice == "SignUp As Admin":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


if __name__ == '__main__':
    main()
