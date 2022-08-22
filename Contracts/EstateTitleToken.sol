pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract EstateTitleToken is ERC721Full {
    address countyClerk = msg.sender;
    string public estateInfo;
    constructor() public ERC721Full("EstateTitleToken", "ETT") {}

    struct EstateTitle {
        string estateInfo;
        string mortgageBank;
        string titleJson;
    }

    mapping(uint256 => EstateTitle) public estateTitles;

    //event Appraisal(uint256 tokenId, uint256 appraisalValue, string reportURI);

    function registerEstateTitle(
        address owner,
        string memory estateMunicipality,
        string memory estateBlock,
        string memory estateLot,
        string memory mortgageBank,
        string memory titleJson
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        
        //string memory estateInfo = estateMunicipality + "-" + estateBlock+ "-" + estateLot;
        estateInfo = string(abi.encodePacked(estateMunicipality,"-" ,estateBlock,"-" ,estateLot));
        estateTitles[tokenId] = EstateTitle(estateInfo, mortgageBank, titleJson);

        return tokenId;
    }
    
}
