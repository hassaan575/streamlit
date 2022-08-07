import streamlit as st
import pandas as pd
from datetime import date
from PIL import Image

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
# DB  Functions
def create_favTicker():
	c.execute('CREATE TABLE IF NOT EXISTS favTickerstable(name TEXT,symbol TEXT)')


def add_favTicker(name,symbol):
	c.execute('INSERT INTO favTickerstable(name,symbol) VALUES (?,?)',(name,symbol))
	conn.commit()

def remove_favTicker(symbol):
	c.execute('DELETE FROM favTickerstable WHERE name =? AND symbol = ?',("Tickers Name: ",symbol))
	conn.commit()
	

def view_all_favTickers():
	c.execute('SELECT symbol FROM favTickerstable')
	data = c.fetchall()
	return data

#----------------------------
# DB  Functions
def create_Ticker():
	c.execute('CREATE TABLE IF NOT EXISTS Tickerstable(name TEXT,symbol TEXT)')


def add_Ticker(name,symbol):
	c.execute('INSERT INTO Tickerstable(name,symbol) VALUES (?,?)',(name,symbol))
	conn.commit()

def remove_Ticker(symbol):
	c.execute('DELETE FROM Tickerstable WHERE name =? AND symbol = ?',("Tickers Name: ",symbol))
	conn.commit()
	

def view_all_Tickers():
	c.execute('SELECT symbol FROM Tickerstable')
	data = c.fetchall()
	return data






def main():
	"""Simple Login App"""

	st.title("Simple Login App")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))
				ticker = st.selectbox("Choose ticker :", ['AAPL [Apple]'
                                 ,'FB [Facebook]',
                                 'HDB [HDFC Bank Limited]',
                                 'MSFT [Microsoft]',
                                 'TSLA [Tesla, Inc.]'
                                ])
			
##### Displaying Slider and Data table #####
				(start_date, end_date) = st.slider("Select date range :", date(2012, 1, 1), date.today(),(date(2012, 1, 1), date.today()),format="DD/MM/YYYY")
				days = st.number_input("Enter Prediction Days")

				st.subheader("Select Your Desired Model")
				if st.button("Linear Regression"):
					st.subheader("Linear Regression")
				elif(st.button("LSTMS")):
					st.subheader("LSTM")
					st.subheader("According to Predictions a RISE is expected so=> BUY")
					st.subheader("RMSE: 15.6")
					st.subheader("Expected Closing Price is: 325.7")
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
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
