import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from pinata import *

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Load_Contract Function
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    # Project_3/Project3/Contracts/EstateTitleToken_abi.json
    # Project_3/Project3/streamlit/pages/_📖_Search.py
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
accounts = w3.eth.accounts

page_title = 'Transfer Estate'
st.markdown("---")
st.markdown("# Approve Transfer of your Estate")
accounts = w3.eth.accounts
from_address = st.selectbox("Select Your Account", options=accounts)
tokens = []
for t in range(contract.functions.totalSupply().call()):
   if(contract.functions.ownerOf(t).call() == from_address):
      tokens.append(t)

token_id = st.selectbox( "Token Id: ", options=tokens)
to_address = st.selectbox("Select Reciever Account", options=accounts)

if st.button("Approve Transfer"):
   tx_hash = contract.functions.approveTransfer(
    int(token_id),
    to_address).transact({'from': from_address, 'gas': 1000000})

   receipt = w3.eth.waitForTransactionReceipt(tx_hash)
   st.write("Transaction receipt mined:")
   st.write(dict(receipt))

st.markdown("# Transfer Estate")
id = st.text_input( "Token Id to transfer: ")
if st.button("Process Transaction"):
   tx_hash = contract.functions.transferEstateTitle(
    int(token_id)).transact({'from': get_clerk_address(), 'gas': 1000000})

   receipt = w3.eth.waitForTransactionReceipt(tx_hash)
   st.write("Transaction receipt mined:")
   st.write(receipt)

