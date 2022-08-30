import os
import json
from nbformat import write
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from pinata import *
from hexbytes import HexBytes
from numpy import *

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Load the contract
contract = load_contract()

# Get all the accounts dictionary
accounts_dict = get_accounts()

# Remove logged in user from account list
del accounts_dict[st.session_state.user_name]

# Transaction page format header
page_title = 'Transfer Estate'
st.write(f"# Welcome: {st.session_state.user_name}")
st.markdown(f"# 📜 Transfer")
st.markdown("## Approve Transfer of your Estate")

# Set from address as logged in user
from_address = st.session_state.user

# Set transfers as session state variable 
if 'transfers' not in st.session_state:
    st.session_state.transfers = {}

# Get the tokens approved by user, but pending transfer
pending= {}
for pending_trans in st.session_state.transfers.keys():
    if (contract.functions.ownerOf(pending_trans).call() == from_address):
        pending[pending_trans]= "Approved for Transfer"

# Create container to update list of approved/ pending transfers
appTrans = st.empty()
with appTrans.container():
    if (pending):
        st.write(f"Approved Token Ids Pending Transfer: {pending.keys()}")


# Get all of users tokens
tokens = []
for t in range(contract.functions.totalSupply().call()):
   if(contract.functions.ownerOf(t).call() == from_address):
      tokens.append(t)

# Get fields for approving transfers
token_id = st.selectbox( "Token Id: ", options=tokens)
to_address_name = st.selectbox("Select Reciever Account", options=accounts_dict.keys())
to_address = accounts_dict[to_address_name]

# Approve Transfer functionality
if st.button("Approve Transfer"):
    tx_hash = contract.functions.approveTransfer(
        int(token_id),
        to_address).transact({'from': from_address, 'gas': 1000000})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    token = int((receipt["logs"][0]["topics"][3]).hex(),16)
    st.success(f"Token {str(token)} has been approved for Transfer")

    # Add token id to approved transfers
    st.session_state.transfers[token_id] = "Approved for Transfer"
    
    # Update list of approved/ pending transfers 
    pending= {}
    for pending_trans in st.session_state.transfers.keys():
        if (contract.functions.ownerOf(pending_trans).call() == from_address):
            pending[pending_trans]= "Approved for Transfer"
    with appTrans.container():
        if (pending):
            st.write(f"Approved Token Ids pending Transfer: {list(pending.keys())}")


# Only clerk can Transfer Estates after approval from owner 
clerk_address = get_clerk_address()
if(clerk_address == st.session_state.user):
    st.markdown("## Transfer Estate")

    # Create container to display pending transfers   
    placeholder = st.empty()
    with placeholder.container():
        id = placeholder.selectbox( "Token Id to transfer: ", st.session_state.transfers.keys())
    if st.button("Process Transfer"):
        # Process Transfer
        tx_hash = contract.functions.transferEstateTitle(
            int(id)).transact({'from': clerk_address, 'gas': 1000000})

        # Delete token from pending transfers list 
        del st.session_state.transfers[id]
        
        # Update pending transfers list  
        with placeholder.container():
            id = placeholder.selectbox( "Token Id to transfer: ", st.session_state.transfers.keys())
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        token = int((receipt["logs"][0]["topics"][3]).hex(),16)
        temp = list(accounts_dict.items()) 
        res = [idx for idx, key in temp if key == contract.functions.ownerOf(token).call()]
        st.success(f"Token {str(token)} has been transferred to {res}")
        