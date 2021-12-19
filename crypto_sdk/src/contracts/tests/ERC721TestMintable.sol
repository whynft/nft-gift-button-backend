// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "remix_tests.sol"; // this import is automatically injected by Remix
import "remix_accounts.sol"; // this import is automatically injected by Remix
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.4.1/contracts/token/ERC721/ERC721.sol";


contract ERC721TestMintable is ERC721 {
    constructor() ERC721("Test", "Test") public {
    }
    function safeMint(address to, uint256 tokenId) public returns (bool) {
        _safeMint(to, tokenId);
        return true;
    }
}
