import HDWalletProvider from "@truffle/hdwallet-provider"
import Web3 from "web3"
import { erc721Abi } from "./contracts/raribleTransferContractAbi.js"

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

//****************** DEPLOY DARILKA CONTRACT ******************/

export async function Deploy(debug, privateKeyExt) {
    const maker = new HDWalletProvider(privateKeyExt, config.rinkebyRpc)
    const web3 = new Web3(maker)
    return deployImpl(web3)
}


import fs from "fs"

export async function deployImpl(web3) {
    try {
        console.log('Running deployWithWeb3 script...')

        const contractName = 'Darilka' // Change this for other contract
        const constructorArgs = ['10000000000000000']    // Put constructor args (if any) here for your contract - comission - 0.01 eth

        // Note that the script needs the ABI which is generated from the compilation artifact.
        // Make sure contract is compiled and artifacts are generated

        const artifactsPath = `/usr/src/app/src/contracts/${contractName}.json` // Change this for different path

        const content = await fs.readFileSync(artifactsPath, 'utf8');


        const metadata = await JSON.parse(content)
        const accounts = await web3.eth.getAccounts()

        let contract = new web3.eth.Contract(metadata.abi)

        contract = contract.deploy({
            data: metadata.data.bytecode.object,
            arguments: constructorArgs
        })

        const newContractInstance = await contract.send({
            from: accounts[0],
            gas: 1500000,
            gasPrice: '30000000000'
        })
        console.log('Contract deployed at address: ', newContractInstance.options.address)
        return newContractInstance.options.address
    } catch (e) {
        console.log(e.message)
    }
}

//**************************** GIVE PERMISSION TO TRANSFER **********************************/


export async function PermissionToTransfer(debug, privateKeyExt, ownerAddress, nftContract, nftToken) {
    // grant permission to ownerAddress. Thus, to contract
    const maker = new HDWalletProvider(privateKeyExt, config.rinkebyRpc)
    const web3 = new Web3(maker)
    permissionToTransferImpl(web3, nftContract, ownerAddress, nftToken)
}

export async function permissionToTransferImpl(web3, nftContract, ownerAddress, tokenId) {
    try {
        // const contractName = 'Darilka' // Change this for other contract
        // const constructorArgs = []    // Put constructor args (if any) here for your contract

        // Note that the script needs the ABI which is generated from the compilation artifact.
        // Make sure contract is compiled and artifacts are generated

        // const artifactsPath = `/usr/src/app/src/contracts/${contractName}.json` // Change this for different path

        // const content = fs.readFileSync(artifactsPath, 'utf8');

        // const metadata = JSON.parse(content)
        const accounts = await web3.eth.getAccounts()

        let contract = new web3.eth.Contract(erc721Abi, nftContract)

        const tx = await contract.methods.approve(ownerAddress, tokenId).send({
            from: accounts[0],
            gas: 1500000,
            gasPrice: '30000000000'  // todo
        }).then((result) => {
            }, (error) => {
        console.log(error);
        });
        console.log("tx: ", tx)
    } catch (e) {
        console.log(e.message)
    }
}

/****************** TRANSFER FROM ALLOWED ACC VIA OUR CONTRACT ************/



export async function DelegetedTransfer(body) {
    const maker = new HDWalletProvider(body.private_ext, config.rinkebyRpc)
    const web3 = new Web3(maker)
    delegetedTransferImpl(web3, body.sender, body.receiver, body.transfer_contract, body.nft_contract, body.token, body.password)
}

export async function delegetedTransferImpl(web3, fromAddress, toAddress, transferContract, nftContract, token, password) {
    try {
        const contractName = 'Darilka' // Change this for other contract
        const constructorArgs = []    // Put constructor args (if any) here for your contract

        // Note that the script needs the ABI which is generated from the compilation artifact.
        // Make sure contract is compiled and artifacts are generated

        const artifactsPath = `/usr/src/app/src/contracts/${contractName}.json` // Change this for different path

        const content = fs.readFileSync(artifactsPath, 'utf8');

        const metadata = JSON.parse(content)
        const accounts = await web3.eth.getAccounts()

        let contract = new web3.eth.Contract(metadata.abi, transferContract)

        const tx = await contract.methods.performTransferNFT(fromAddress, toAddress, nftContract, token, password).send({
            from: accounts[0],
            gas: 1000000,
            gasPrice: '5000000000'
        })
        console.log("tx: ", tx)
    } catch (e) {
        console.log(e.message)
    }
}

/********************* CONFIRM TRANSFER VIA SET PASSWORD AND COMISION MONEY (should run on client) ******************/

export async function Setpassword(body) {
    const maker = new HDWalletProvider(body.private_ext, config.rinkebyRpc)
    const web3 = new Web3(maker)
    setpasswordImpl(web3, body.transfer_contract, body.nft_contract, body.token, body.password)
}

export async function setpasswordImpl(web3, contract_address, nftContract, tokenId, password) {
    try {
        const contractName = 'Darilka' // Change this for other contract
        const constructorArgs = []    // Put constructor args (if any) here for your contract

        // Note that the script needs the ABI which is generated from the compilation artifact.
        // Make sure contract is compiled and artifacts are generated

        const artifactsPath = `/usr/src/app/src/contracts/${contractName}.json` // Change this for different path

        const content = fs.readFileSync(artifactsPath, 'utf8');

        const metadata = JSON.parse(content)
        const accounts = await web3.eth.getAccounts()

        let contract = new web3.eth.Contract(metadata.abi, contract_address)

        const passwordHash = await web3.utils.keccak256(password)

        console.log("passwordHash", passwordHash)

        const tx = await contract.methods.setConfirmation(nftContract, tokenId, passwordHash).send({
            value: '10000000000000000',
            from: accounts[0],
            gas: 1500000,
            gasPrice: '30000000000'
        }).then((result) => {
            }, (error) => {
        console.log(error);
        });
        console.log("tx: ", tx)
    } catch (e) {
        console.log(e.message)
    }
}

/****** book NFT for receiver (son anyone else can't get NFT until receiver prove himself or sender withdraw NFT) *******/



export async function Book(body) {
    const maker = new HDWalletProvider(body.private_ext, config.rinkebyRpc)
    const web3 = new Web3(maker)
    bookImpl(web3, body.transfer_contract, body.nft_contract, body.token, body.receiver)
}

export async function bookImpl(web3, contract_address, nftContract, tokenId, receiver) {
    try {
        const contractName = 'Darilka' // Change this for other contract
        const constructorArgs = []    // Put constructor args (if any) here for your contract

        // Note that the script needs the ABI which is generated from the compilation artifact.
        // Make sure contract is compiled and artifacts are generated

        const artifactsPath = `/usr/src/app/src/contracts/${contractName}.json` // todo: Change this for different path

        const content = fs.readFileSync(artifactsPath, 'utf8');

        const metadata = JSON.parse(content)
        const accounts = await web3.eth.getAccounts()

        let contract = new web3.eth.Contract(metadata.abi, contract_address)

        const tx = await contract.methods.bookTransfer(receiver, nftContract, tokenId).send({
            from: accounts[0],
            gas: 1500000,
            gasPrice: '30000000000'
        }).then((result) => {
            }, (error) => {
        console.log(error);
        });
        console.log("tx: ", tx)
    } catch (e) {
        console.log(e.message)
    }
}
