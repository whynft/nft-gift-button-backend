import HDWalletProvider from "@truffle/hdwallet-provider"
import Web3 from "web3"

import { createRaribleSdk } from "@rarible/protocol-ethereum-sdk"

import { toAddress } from "@rarible/types"
import { toBigNumber } from "@rarible/types"
import { Web3Ethereum } from "@rarible/web3-ethereum"

import FormData from "form-data"; // a nodejs module.
global.FormData = FormData; // hack for nodejs;

import fetchApi from "node-fetch"; // a nodejs module.
global.window = {
    fetch: fetchApi,
}

// todo: make importable
const config = {
	mainnetRpc: "https://mainnet.infura.io/v3/84653a332a3f4e70b1a46aaea97f0435",
 	rinkebyRpc: "https://rinkeby.infura.io/v3/84653a332a3f4e70b1a46aaea97f0435",
 	rinkeby: "rinkeby"
}


export async function Transfer(receiver_user_address, contract_address, token_address, sender_privateKeyExt) {
    // to user_address with privateKeyExt send token_address (our nft) via contract specified.
    const maker = new HDWalletProvider(sender_privateKeyExt, config.rinkebyRpc)
    const web3 = new Web3(maker)
    return await createTransfer(web3, contract_address, token_address, receiver_user_address)
}

export async function createTransfer(web3, contractAddress, tokenAddress, to_address) {
    const ethereum = new Web3Ethereum({ web3, gas: 200000})
    const sdk = createRaribleSdk(ethereum, config.rinkeby)
    const contract = toAddress(contractAddress)
    const tokenId = toBigNumber(tokenAddress)
    const hash = await sdk.nft.transfer(
        {
            assetClass: "ERC721",
            contract: contract,
            tokenId: tokenId,
        },
        to_address,
    )
    return hash  // todo: useless return
}
