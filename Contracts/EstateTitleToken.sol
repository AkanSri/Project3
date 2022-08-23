pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract EstateTitleToken is ERC721Full {
    address countyClerk = msg.sender; //County Clerk deploys contract
    
    constructor() public ERC721Full("EstateTitleToken", "ETT") {}

    struct EstateTitle {
        string estateInfo; //Will be in format of estateMunicipality-estateBlock-estateLot
        string mortgageBank; 
        string titleJson;//Will hold hash for title on the IPFS
    }

    mapping(uint256 => EstateTitle) public estateTitles; //Collection of titles and their owner
    mapping(uint256 => address) public approvedRecievers;//approvedReciever 
    //registerEstateTitle takes in all the parameters of the property, and the title  
    function registerEstateTitle(
        address payable owner,
        string memory estateMunicipality,
        string memory estateBlock,
        string memory estateLot,
        string memory mortgageBank,
        string memory titleJson
    ) public returns (uint256) {
        //only the county clerk can register titles
        require(msg.sender == countyClerk, "You are not authorized to Register Titles");
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        
        string memory estateInfo = string(abi.encodePacked(estateMunicipality,"-" ,estateBlock,"-" ,estateLot)); //formatting estate info
        estateTitles[tokenId] = EstateTitle(estateInfo, mortgageBank, titleJson);
        return tokenId;
    }

    //transferEstateTitle lets the county clerk transfer estate titles
    function transferEstateTitle(uint256 tokenId) external payable {
        require(msg.sender == countyClerk, "Only the County Clerk can transfer this title if approved by owner. If you are the owner please Approve Transfer");
        address addressTo = approvedRecievers[tokenId];
        safeTransferFrom(ownerOf(tokenId), addressTo, tokenId);
    }

    //approveTransfer lets the owner approve 
   function approveTransfer(uint256 tokenId, address recieverAddress) public {
        require(msg.sender == ownerOf(tokenId), "Only the owner of this token can approve a transfer");
        //call approve and to address = countyclerk address by default
        approve(countyClerk, tokenId);
        approvedRecievers[tokenId] = recieverAddress;
    }
}

