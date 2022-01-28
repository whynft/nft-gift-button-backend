# nft-gift-button-backend

The backend represents by itself a backend for the [Rarible proposal](https://gov.rarible.org/t/nft-gift-button-grant-proposal/263).

Under the hood we use deployed **Darilka contract** with help of python and HTTPProvider. 

## Requirement
- Created and published Darilka contract [backend should be aware of private key of a contract publisher, ofc]
- Docker & Docker Compose

## Start
Prepare `.env` according to [.env.example](.env.example) and
```
docker-compose -f docker-compose.prod.yml up
```

## ToDo
- [ ] make subscriber for emit event on finally transferred: 
we want to clean redis to make it possible to even send A gift to Bob again through the backend, e.g. A -> B -> A -> B, ... 
- [ ] to async provider when the one will be developed
- [ ] test when on next service growth
