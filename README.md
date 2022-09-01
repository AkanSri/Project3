# Project3

## Objective
Provide efficiency and transparency using blockchain technology for recording real estate deed and title ownership by using non-fungible smart contracts

## Current (Outdated) Way
Records of recording real estate transactions are limited to local municipalities, which may be subjected to clerical errors occured in documenting deed ownership can lead to potential problems at sell. 

## Our solution
NFTs will provide fast and secure transactions of real estate ownership and limit the encroachments and easements that may arise. They will also provide fast and secure transactions of real estate ownership and limit the encroachments and easements that may arise. Our project has 2 parts: **Smart Contract** and **Streamlit App**

### Smart Contract
Since we are creating NFTs of estates we extedning the ERC721 Protocol. The information we wanted to include on a NFT is the estate's Municipality, Block, Lot, Street Address, Mortgage Bank and the IPFS Hash of the title document. We created a struct to hold this info and a mapping to related each token id. 

Only the clerk (the address that deployed the contract) has access to register (mint) the token and assign it to a user. 

Once a title transfer has to occur, the owner of the token has to go in and approve a transfer to a specific reciever address. The way we implemented this was have the owner approve the clerk to transfer a specified token id, and create a mapping that holds the token id and the approved reciever address. Then, the clerk has to go in and actually perform the transfer. Since the owner approved the clerk to transfer, the clerk can now transfer the token from the owner to the the approved reciever mapped to the token id. 

### App
We created an app using Streamlit to visualize the smart contract functions. This app has a couple of tabs: **Home**, **List**, **Search**, **Transfer**.

#### Home:
This page has the Login screen that makes sure only certain people have access to certain information. For now, the login process is simplfied so the password is equal to the username. We implemented session state variables that are accessible on all pages, and dont get reset everytime the screen is refreshed. 

#### List:
This tab lists all your tokens and the information about each token. If the clerk is logged in, all the tokens will be listed.

#### Search:
If clerk is logged in, they can register new tokens on this page by inputting all the data and uploading the title to the IPFS. This tab also has the search functionality which can filter by any information inputted and also search by the token id. If the token id is populated, you can see the transfer history of that token.

#### Transfer:
On this tab, the user can see the tokens they own and approve their tokens for transfer to a reciever. If the clerk is logged in, they can see the token ids pending transfers, choose the token and process the transfer. 

