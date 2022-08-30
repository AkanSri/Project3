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

# Load the contract
contract = load_contract()

# Get clerk address
clerk_address = get_clerk_address()

# Get accounts dictionary 
accounts_dict = get_accounts()

# Search page format header
page_title = 'Search'
st.write(f"# Welcome: {st.session_state.user_name}")
st.markdown(f"# 📖 Search")
st.markdown("## Register/Search Property Record By Block and Lot")

# Save municipalities as session state variable 
if 'municipalities' not in st.session_state:
    st.session_state.municipalities = ['Piscataway', 'New Brunswick', 'Princeton', 'Bordentown']

# Allow clerk to add municipalities
if(clerk_address == st.session_state.user):
    new_municipality = st.text_input("New Municipality: ")    
    if st.button("Add new Municipality"):
        if (new_municipality): 
            st.session_state.municipalities.append(new_municipality)

# Get Estate Registration/Search Info
municipality = st.selectbox("Municipality:", st.session_state.municipalities)
block = st.text_input("Block: ")
lot = st.text_input("Lot: ")
bank = st.text_input("Bank: ")
owner_name = st.selectbox("Select owner of estate", options= accounts_dict.keys())
owner = accounts_dict[owner_name]
loc = st.text_input("Address: ")
if (loc):
    location = geolocator.geocode(loc)
    df = pd.DataFrame({'latitude': [location.latitude], 'longitude':[location.longitude]})
    #plotting a map with the above defined points
    st.map(df)
file = st.file_uploader("Upload Title", type=["pdf","doc","docx"])
title_name = "title"

# Pin title doc and get IPFS title hash 
if (file):
   title_ipfs_hash, token_json = pin_title(title_name, file)
   st.markdown(f"[{title_name} IPFS Link](https://ipfs.io/ipfs/{token_json['title_hash']})")

# Clerk can register estate 
if(clerk_address == st.session_state.user):
    if st.button("Register Estate"):
        tx_hash = contract.functions.registerEstateTitle(
        owner,
        municipality,
        block,
        lot,
        loc,
        bank,
        title_ipfs_hash).transact({'from': clerk_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        token = int((receipt["logs"][0]["topics"][3]).hex(),16)
        st.success(f"Token {str(token)} has been registered to {owner_name}")

tokenId = st.text_input("Enter the token id (leave blank if registering estate)")
# Search button 
if st.button("Search"): 
    # If Token Id is populated, get all transfers for id
   if (tokenId):
       # Create filter by Token Id
       transfer_filter = contract.events.Transfer.createFilter(
           fromBlock=0, argument_filters={"tokenId": int(tokenId)})
       transfers_reports = transfer_filter.get_all_entries()
       st.write(transfers_reports)    
   else:
       # Create filter by populated fields
        filters = {}  
        if(loc):
            filters.update({"real_address": loc})
        else:
            if(municipality):
                filters.update({"estateMunicipality": municipality})
            if(block):
                filters.update({"estateBlock": block})
            if(lot):
                filters.update({"estateLot": lot})
        estate_info_filter = contract.events.RegisteredEstateInfo.createFilter(
            fromBlock=0, argument_filters= filters 
        )
        estate_info_reports = estate_info_filter.get_all_entries()
        st.write(estate_info_reports)   