import os
import json
import requests
from dotenv import load_dotenv
from web3 import Web3
from pathlib import Path
import streamlit as st
load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
accounts = w3.eth.accounts

# Get clerk address (first address in list of wallet accounts)
def get_clerk_address():
    return (accounts[0])

# Get dictionary of accountname : account wallet
def get_accounts():
    if (len(list(accounts))== 5):
        account_name =  {
            "Dan" : accounts[0],
            "Akanksha" : accounts[1],
            "Wadeeha" : accounts[2],
            "Ranny" : accounts[3],
            "Hakob" : accounts[4],
            }
        return (account_name)
    else:
        account_name = {}
        userNumber = 0
        for a in accounts:
            account_name = {a: f"User{userNumber}"}
        return (account_name)

# Load_Contract Function
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

json_headers = {
    "Content-Type": "application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

def convert_data_to_json(content):
    data = {"pinataOptions": {"cidVersion": 1}, "pinataContent": content}
    return json.dumps(data)

def pin_file_to_ipfs(data):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        files={'file': data},
        headers=file_headers
    )
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_json_to_ipfs(json):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        data=json,
        headers=json_headers
    )
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash


# Helper functions to pin files and json to Pinata
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