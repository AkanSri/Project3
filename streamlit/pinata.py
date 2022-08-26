import os
import json
import requests
from dotenv import load_dotenv
from web3 import Web3
import streamlit as st
load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
accounts = w3.eth.accounts

def get_clerk_address():
    return (accounts[0])
def get_accounts():
    return (list(accounts))
    
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
