// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

interface Ownable {
    function ownerOf(uint256 tokenId) external returns(address);
}

interface Transferable {
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
}

/**
 * @title Darilka
 * @dev contract designed to make both centralized & decentralized checks
 * 1) centralized to check if receiver is good
 * 2) decentralized to not trust to this contract owner
 */
contract Darilka {

    address private owner;
    uint256 private commission;
    uint256 private amountForReceiver;

 // modifier to check if caller is owner
    modifier isOwner() {
        // If the first argument of 'require' evaluates to 'false', execution terminates and all
        // changes to the state and to Ether balances are reverted.
        // This used to consume all gas in old EVM versions, but not anymore.
        // It is often a good idea to use 'require' to check if functions are called correctly.
        // As a second argument, you can also provide an explanation about what went wrong.
        require(msg.sender == owner, "Caller is not owner");
        _;
    }

    struct NFT {
        address nftContract;
        uint256 tokenId;
    }

    mapping(bytes32 => bytes32) private confirmationHashes;

    mapping(bytes32 => address) private bookedTransfer;

    /**
     * @dev Set contract deployer as owner
     */
    constructor(uint256 _commission, uint256 _amountForReceiver) {
        owner = msg.sender; // 'msg.sender' is sender of current call, contract deployer for a constructor
        commission = _commission;
        amountForReceiver = _amountForReceiver;
    }

    /**
     * @dev Change owner
     * @param newOwner address of new owner
     */
    function setOwner(address newOwner) public isOwner {
        owner = newOwner;
    }

    function setCommission(uint256 newCommission) public isOwner {
        commission = newCommission;
    }

    function setAmountForReceiver(uint256 newAmountForReceiver) public isOwner {
        amountForReceiver = newAmountForReceiver;
    }

    function getOwner() public view returns (address) {
        return owner;
    }

    function getComission() public view returns (uint256) {
        return commission;
    }

    function getAmountForReceiver() public view returns (uint256) {
        return amountForReceiver;
    }

    function withdraw() public payable isOwner {
        payable(owner).transfer(address(this).balance);
    }

    /**
     * @dev Store confirmation hash to make nft transaction
     * @param nftContract address of nft which will be allowed to transfer
     * @param tokenId uint256 nft order id in contract
     */
    function setConfirmation(address nftContract, uint256 tokenId, bytes32 keccak256ConfirmationHash) payable public {
        require(msg.value >= commission + amountForReceiver, "Expect collateral not less than commission + amountForReceiver");
        require(Ownable(nftContract).ownerOf(tokenId) == msg.sender, "Only nft owner could set confirmation password hash");
        confirmationHashes[keccak256(abi.encodePacked(nftContract, tokenId))] = keccak256ConfirmationHash;
    }

    /**
     * book delegated transfer: call this on backend after get centralized confirmation from receiver
     *  make two things: book transfer for receiver address and send some money to run transfer
     */

    function bookTransfer(address receiver, address nftContract, uint256 tokenId) payable public isOwner {
        bookedTransfer[keccak256(abi.encodePacked(nftContract, tokenId))] = receiver;
        payable(receiver).transfer(amountForReceiver);
    }


    /**
    * performTransferNFT with confirmation, it needed to not trust our backend
    **/
    function performTransferNFT(address sender, address receiver, address nftContract, uint256 tokenId, string memory confirmation) public {
        bytes32 nft = keccak256(abi.encodePacked(nftContract, tokenId));
        require(bookedTransfer[nft] == msg.sender);
        require(confirmationHashes[nft] == keccak256(abi.encodePacked(confirmation)));
        Transferable(nftContract).safeTransferFrom(sender, receiver, tokenId);
    }
}
