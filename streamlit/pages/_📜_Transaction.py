

import streamlit as st


page_title = 'Search'
st.markdown("# Register Property Record By Block and Lot")



st.text("\n")
st.text("\n")
st.markdown("## All Fields are Mandatory")


option = st.selectbox('Municipality:', ('Choose One', 'Bergen', 'Essex', 'Hudson'))
block = st.text_input( "Block: ")
lot = st.text_input( "Lot: ")
bank = st.text_input("Bank: ")

   
if st.button("Register"):
   st.write("result")