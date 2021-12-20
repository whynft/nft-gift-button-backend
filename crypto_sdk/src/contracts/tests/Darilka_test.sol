// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

import "remix_tests.sol"; // this import is automatically injected by Remix
import "remix_accounts.sol"; // this import is automatically injected by Remix

import "../contracts/Darilka.sol";
import "./ERC721TestMintable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.4.1/contracts/token/ERC721/ERC721.sol";


contract DarilkaTest {
    uint256 comission = 0.05 ether;
    uint256 amountForReceiver = 0.05 ether;

    address owner;
    address sender;
    address receiver;

    uint256 nftTokenId = 0;

    string password = "123";
    bytes32 passwordKeccakk256Hash = 0x64e604787cbf194841e7b68d7cd28786f6c9a0a3ab9f8b0a0e87cb4387ab0107;

    Darilka darilka;
    ERC721TestMintable collection;

/// #sender: account-0
    function beforeAll () public {
        owner = TestsAccounts.getAccount(0);
        sender = TestsAccounts.getAccount(1);
        receiver = TestsAccounts.getAccount(2);
        darilka = new Darilka(comission, amountForReceiver);
        darilka.setOwner(owner);
        collection = new ERC721TestMintable();
        collection.safeMint(sender, nftTokenId);
    }

/// #sender: account-0
    function testContractAfterInit() public {
        Assert.equal(msg.sender, owner, "Wrong msg sender");
        Assert.equal(darilka.getComission(), comission, "Wrong comission");
        Assert.equal(darilka.getAmountForReceiver(), amountForReceiver, "Wrong amountForReceiver");
        Assert.equal(darilka.getOwner(), owner, "Unexpected owner");
    }

/// #sender: account-1
    function testOuterContractOwnerChange() public {
        Assert.equal(msg.sender, sender, "Wrong msg sender");
        try darilka.setOwner(msg.sender) {
            require(false, "Should revert");
        } catch (bytes memory /*lowLevelData*/) {}
    }

    function testNftPermissions() public {
        Assert.equal(sender, collection.ownerOf(nftTokenId), "Wrong owner");
        Assert.equal(address(0), collection.getApproved(nftTokenId), "Expect nobody approved");
    }

// /// #sender: account-0
// /// #value: 0.01 ether
//     function testDarilkaBadSenderConfirmation() public payable {
//         Assert.equal(msg.value, comission, "expect value = comission");
//         Assert.equal(msg.sender, owner, "wrong msg sender");
//         darilka.setConfirmation(address(collection), nftTokenId, passwordKeccakk256Hash);
//     }

/// #sender: account-1
/// #value: 10000000000000000
    function testDarilkaGoodSenderConfirmation() public payable {
        Assert.equal(msg.value, comission + amountForReceiver, "Expect value = comission + amountForReceiver");
        Assert.equal(msg.sender, sender, "Wrong msg sender");
        darilka.setConfirmation{value:msg.value}(address(collection), nftTokenId, passwordKeccakk256Hash);
    }



//todo: make that test works local
// /// #sender: account-1
//     function testDarilkaPipelineSenderPart() public {
//         Assert.equal(msg.sender, sender, "wrong msg sender");
//         Assert.equal(sender, collection.ownerOf(nftTokenId), "wrong owner");
//         collection.approve(darilkaAddress, nftTokenId);
//         Assert.equal(darilkaAddress, collection.getApproved(nftTokenId), "expect darilka approved");
//     }
}
