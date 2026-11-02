# BT Assignment 6 – Create a Business Network using Hyperledger

**Problem Statement:** Write a program to create a Business Network using Hyperledger.

Business network built here: **Vehicle Trading Network**.
- **Participant**: `Trader` (id, name, balance)
- **Asset**: `Vehicle` (vin, make, model, price, owner → Trader)
- **Transaction**: `Trade` (transfers a vehicle to a new owner and moves the money)
- **Event**: `TradeNotification`

| File | Purpose |
|---|---|
| `model.cto` | Modeling language: defines participants, assets, transactions and events |
| `logic.js` | Transaction processor function (business logic) |
| `permissions.acl` | Access-control rules |

## How to demo (Hyperledger Composer Playground)
> Composer is deprecated but is still what most colleges show for this assignment. If the online playground is unavailable, run it locally:
> `npm install -g composer-playground@0.20.9` then `composer-playground` (needs Node 8/10). Or simply explain the files below.

1. Open Composer Playground → **Deploy a new business network** → *empty-business-network* → name `trading-network` → *Deploy* → *Connect now*.
2. **Define** tab:
   - Model file → replace with `model.cto`
   - *Add a file* → Script file → paste `logic.js`
   - Access control → replace with `permissions.acl`
   - Click **Deploy changes**.
3. **Test** tab:
   - *Trader* → Create New Participant:
     ```json
     {"$class": "org.example.trading.Trader", "traderId": "T1", "firstName": "Siddhesh", "lastName": "S", "balance": 500000}
     ```
     ```json
     {"$class": "org.example.trading.Trader", "traderId": "T2", "firstName": "Amit", "lastName": "P", "balance": 900000}
     ```
   - *Vehicle* → Create New Asset:
     ```json
     {"$class": "org.example.trading.Vehicle", "vin": "V100", "make": "Tata", "model": "Nexon", "price": 300000, "owner": "resource:org.example.trading.Trader#T1"}
     ```
   - **Submit Transaction** → Trade:
     ```json
     {"$class": "org.example.trading.Trade", "vehicle": "resource:org.example.trading.Vehicle#V100", "newOwner": "resource:org.example.trading.Trader#T2"}
     ```
   - Check: Vehicle V100 owner is now **T2**, T1 balance = 800000, T2 balance = 600000. *All Transactions* shows the history (ledger).

## Hyperledger Fabric theory (viva)
- **Hyperledger**: open-source umbrella project (Linux Foundation) for **permissioned** enterprise blockchains. Includes Fabric, Besu, Indy, Iroha, Sawtooth, Composer (deprecated tool).
- **Fabric architecture**: Peers (endorsing + committing), **Orderer** (orders txns into blocks, Raft), **CA** (issues identities via MSP), **Channels** (private sub-ledgers), **Chaincode** (smart contract in Go/Node/Java).
- **Transaction flow**: Execute → Order → Validate. Client proposal → endorsing peers simulate and sign → orderer creates block → peers validate against the endorsement policy → commit to ledger.
- **Ledger** = blockchain (immutable log) + **world state** (CouchDB/LevelDB key-value).
- No cryptocurrency and no mining, so it is fast.
- Business network in Composer = model (.cto) + script (.js) + ACL (.acl) + queries (.qry), packaged as a `.bna` file.
