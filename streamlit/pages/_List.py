import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from pinata import *
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
#making an instance of Nominatim class
geolocator = Nominatim(user_agent="my_request")
load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

st.write(f"# Welcome: {st.session_state.user_name}")

# Load the contract
contract = load_contract()

# Get clerk address
clerk_address = get_clerk_address()

indices = ['Municipality', 'Block', 'Lot', 'Address', 'Bank', 'Title IPFS Hash']
col = 'Estate Info'

if(clerk_address == st.session_state.user):
        st.write("## All Estate Tokens:") 
else:
        st.write("## Your Estate Tokens:")

for t in range(contract.functions.totalSupply().call()):
    if(clerk_address == st.session_state.user):
        st.write(f"Token: {t}")
        st.table(pd.DataFrame(contract.functions.estateTitles(t).call(), index=indices, columns=[col]))
    elif (contract.functions.ownerOf(t).call() == st.session_state.user):
        st.write(f"Token: {t}")
        st.table(pd.DataFrame(contract.functions.estateTitles(t).call(), index=indices, columns=[col]))
