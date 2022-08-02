import streamlit as st
import pandas as pd
import json
import requests  # pip install requests
import requests  # pip install requests
from apps import progress, h1, newp, recommendation, t1, prediction  # import your app modules here
from streamlit_lottie import st_lottie  # pip install streamlit-lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_bek1x1xd.json")

st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",  # medium ; high
    # canvas
    height=None,
    width=None,
    key=None,
)


class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
def __init__(self):
        self.apps = []
def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })
def run(self):
        # app = st.sidebar.radio(
        app = st.selectbox(
            'Navigation',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
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


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():

	app = MultiApp()
	app1 = MultiApp()
	app.add_app("homepage", h1.app)
	app.add_app("Progress", progress.app)
	app.add_app("recommendation", recommendation.app)
	app1.add_app("Stockdata", t1.app)
	app.add_app("Sto", prediction.app)
	app.add_app("prediction", newp.app)

	"""Stock Prediction Website"""

	st.title("Stock Prediction Website")

	st.markdown("""
		# Trading Through Machine Learning
		We use Machine Learning Algorithm to predict the future price of a stock
		""")
	menu = ["Home or LogOut","Login  as User","SignUp as User","Login As Admin","SignUp As Admin"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home or LogOut":
		st.subheader("Home")
	elif choice == "Login As Admin":
		st.subheader("Admin Section")	
		
		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				
				st.success("Logged In as {}".format(username))
				app1.run()
				

	elif choice == "Login  as User":
		st.subheader("User Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))
				app.run()

			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp as User": 
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")
	elif choice == choice == "SignUp As Admin":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")


if __name__ == '__main__':
	main()
