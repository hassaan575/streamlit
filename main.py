import streamlit as st
import pandas as pd


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

				task = st.selectbox("Task",["Add Ticker","Remove Ticker","View Tickers"])
				if task == "Add Ticker":
					st.subheader("Add Your Ticker")
					Ticker = st.sidebar.text_input("Ticker Name")
					if st.button("Add"):
						create_Ticker()
						add_Ticker("Tickers Name: ",Ticker)	
				elif task == "Remove Ticker":
					Ticker1 = st.sidebar.text_input("Ticker Name")
					if st.button("Delete"):					
						remove_Ticker(Ticker1)
				elif task == "View tickers":
					st.subheader("View Tickers")
					user_result = view_all_Tickers()
					clean_db = pd.DataFrame(user_result,columns=[ "Ticker's Name: "])
					st.dataframe(clean_db)
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
