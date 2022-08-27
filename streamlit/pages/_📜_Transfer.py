import os
import json
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

################################################################################
# Load_Contract Function
################################################################################
@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('EstateTitleToken_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    return contract

# Load the contract
contract = load_contract()

# Get all the accounts 
accounts_dict = get_accounts()

# Remove logged in user from account list
del accounts_dict[st.session_state.user_name]

# Transaction page format header
page_title = 'Transfer Estate'
st.write(f"Welcome: {st.session_state.user_name}")
st.markdown(f"# 📜 Transfer")
st.markdown("## Approve Transfer of your Estate")

# Set from address as logged in user
from_address = st.session_state.user

# Get all of users tokens
tokens = []
for t in range(contract.functions.totalSupply().call()):
   if(contract.functions.ownerOf(t).call() == from_address):
      tokens.append(t)

# Get fields for approving transfers
token_id = st.selectbox( "Token Id: ", options=tokens)
to_address = st.selectbox("Select Reciever Account", options=accounts_dict.keys())
to_address = accounts_dict[to_address]

# Set transfers as session state variable 
if 'transfers' not in st.session_state:
    st.session_state.transfers = []

# Approve Transfer functionality
if st.button("Approve Transfer"):
    tx_hash = contract.functions.approveTransfer(
        int(token_id),
        to_address).transact({'from': from_address, 'gas': 1000000})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.session_state.transfers.append(token_id)

# Only clerk can Transfer Estates after approval from owner 
clerk_address = get_clerk_address()

if(clerk_address == st.session_state.user):
    st.markdown("## Transfer Estate")
    st.markdown(f"### Pending Transfer Token Id(s): {st.session_state.transfers}")
    id = st.text_input( "Token Id to transfer: ")
    if st.button("Process Transaction"):
        tx_hash = contract.functions.transferEstateTitle(
            int(id)).transact({'from': clerk_address, 'gas': 1000000})
        st.session_state.transfers.remove(int(id))
        st.markdown(f"### Pending Transfer Token Id(s): {st.session_state.transfers}")
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        token = int((receipt["logs"][0]["topics"][3]).hex(),16)
        to_address = "0x"+(receipt["logs"][0]["topics"][2]).hex()[-40:]
        st.write(f"Token {str(token)} has been transferred to {to_address}")
        st.write("Transaction receipt mined:")
        st.write(receipt)
