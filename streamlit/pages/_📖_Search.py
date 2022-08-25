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
# st.write(transfers_reports[len(transfers_reports)-1]['args']['to'])

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


page_title = 'Search'
st.markdown("# Register Property Record By Block and Lot")
st.text("\n")
st.text("\n")

municipality = st.selectbox("Municipality:", ('Bergen', 'Essex', 'Hudson', 'Bordentown'))
block = st.text_input("Block: ")
lot = st.text_input("Lot: ")
bank = st.text_input("Bank: ")
owner = st.selectbox("Select owner of estate", options= get_accounts())
tokenId = st.text_input("Enter the token id (leave blank if registering estate)")

file = st.file_uploader("Upload Title", type=["pdf","doc","docx"])
title_name = "title"

if (file):
   title_ipfs_hash, token_json = pin_title(title_name, file)
   st.markdown(f"[{title_name} IPFS Link](https://ipfs.io/ipfs/{token_json['title_hash']})")


st.markdown("---")
   
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
    #st.write(f"Token {token_id} created")

if st.button("Search"): 
   if (tokenId):
      transfer_filter = contract.events.Transfer.createFilter(
         fromBlock=0, argument_filters={"tokenId": int(tokenId)})
      transfers_reports = transfer_filter.get_all_entries()
      st.write(transfers_reports)
        
   else:
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