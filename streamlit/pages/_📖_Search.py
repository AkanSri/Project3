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

# Get clerk address
clerk_address = get_clerk_address()

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################
def pin_title(title_name, title_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(title_file.getvalue())

    # Build a token metadata file for the title
    token_json = {
        "name": title_name,
        "title_hash": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json

# Search page format header
page_title = 'Search'
st.write(f"Welcome: {st.session_state.user}")
st.markdown(f"# 📖 Search")
st.markdown("## Register/Search Property Record By Block and Lot")

# Save municipalities as session state variable 
if 'municipalities' not in st.session_state:
    st.session_state.municipalities = ['Bergen', 'Essex', 'Hudson', 'Bordentown']

# Allow clerk to add municipalities
if(clerk_address == st.session_state.user):
    new_municipality = st.text_input("New Municipality: ")    
    if st.button("Add new Municipality"):
        st.session_state.municipalities.append(new_municipality)

# Get Estate Registration/Search Info
municipality = st.selectbox("Municipality:", st.session_state.municipalities)
block = st.text_input("Block: ")
lot = st.text_input("Lot: ")
bank = st.text_input("Bank: ")
owner = st.selectbox("Select owner of estate", options= get_accounts())
tokenId = st.text_input("Enter the token id (leave blank if registering estate)")
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
        bank,
        title_ipfs_hash).transact({'from': clerk_address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))

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