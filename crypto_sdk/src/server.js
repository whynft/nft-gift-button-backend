'use strict';
import { Transfer } from './rarible-transfer.js';
import { Deploy, PermissionToTransfer, DelegetedTransfer, Setpassword, Book } from './darilka-transfer.js';


import express from 'express';

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App setUp
const app = express();
app.use(express.json());


app.post('/', async (request, response) => {
  // Pass ipfs & user_address
  console.log('get', request.body);
  try {
    const hash = await Transfer(request.body.user_receiver, request.body.contract, request.body.token, request.body.sender_private_ext)
    console.log('Response with hash', hash);
    response.json({hash: hash, status: "OK"});
  } catch (error) {
    console.error(error);
    response.json({error: error, status: "ERROR"});
    return;
  }
});


app.post('/deploy', async (request, response) => {
  // Pass ipfs & user_address
  console.log('get', request.body);
  try {
    const link = await Deploy(request.body.debug, request.body.private_ext)
    console.log('Response with link', link);
    response.json({link: link, status: "OK"});
  } catch (error) {
    console.error(error);
    response.json({error: error, status: "ERROR"});
    return;
  }
});


app.post('/permission', async (request, response) => {
  // Pass ipfs & user_address
  console.log('get', request.body);
  try {
    const link = await PermissionToTransfer(
        request.body.debug,
        request.body.private_ext,  // sender private key
        request.body.owner_address, // transfer contract address
        request.body.nft_contract,
        request.body.nft_token
    )
    console.log('Response with link', link);
    response.json({link: link, status: "OK"});
  } catch (error) {
    console.error(error);
    response.json({error: error, status: "ERROR"});
    return;
  }
});


app.post('/setpassword', async (request, response) => {
  // Pass ipfs & user_address
  console.log('get', request.body);
  try {
    const link = await Setpassword(request.body)
    console.log('Response with link', link);
    response.json({link: link, status: "OK"});
  } catch (error) {
    console.error(error);
    response.json({error: error, status: "ERROR"});
    return;
  }
});


app.post('/book', async (request, response) => {
  // Pass ipfs & user_address
  console.log('get', request.body);
  try {
    const link = await Book(request.body)
    console.log('Response with link', link);
    response.json({link: link, status: "OK"});
  } catch (error) {
    console.error(error);
    response.json({error: error, status: "ERROR"});
    return;
  }
});


app.post('/dtransfer', async (request, response) => {
  // Pass ipfs & user_address
  console.log('get', request.body);
  try {
    const link = await DelegetedTransfer(request.body)
    console.log('Response with link', link);
    response.json({link: link, status: "OK"});
  } catch (error) {
    console.error(error);
    response.json({error: error, status: "ERROR"});
    return;
  }
});


app.get('/healthcheck', async (request, response) => {
  response.json({status: 'ok'});
});


app.listen(PORT, HOST);
console.log(`Express Kostil Server is running on http://${HOST}:${PORT}`);
