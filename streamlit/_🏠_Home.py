import streamlit as st
from pinata import *

# Save user as session state variable 
if 'user' not in st.session_state:
    st.session_state.user = 'INVALID'

# Home page format header
page_title = '_🏠_Home'
st.markdown("# 🏠 Home")
st.markdown("## Estate Titles Through Blockchain")
st.markdown("### Login")
st.write(get_accounts())
account_dict = get_accounts()
# Get username and password
username = str(st.selectbox("Select User:", options= account_dict.keys()))
password = st.text_input("Password",type='password')

# Login
if st.button("Login"):
    if (username == password):
        st.session_state.user = account_dict[username]
        st.session_state.user_name = username
        st.write(st.session_state.user)
        st.success(f"Logged in as {st.session_state.user_name}")
    else:
        st.session_state.user = 'INVALID USER'
        st.error(f"{st.session_state.user} Unable to log in ")