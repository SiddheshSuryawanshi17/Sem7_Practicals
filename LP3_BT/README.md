# LP-III : Blockchain Technology (BT)

| # | Problem statement | Folder | What's inside |
|---|---|---|---|
| 1 | Installation of MetaMask and study spending Ether per transaction | `A1_MetaMask_Install_Ether_per_Txn` | step-by-step + gas/fee observation table |
| 2 | Create your own wallet using MetaMask for crypto transactions | `A2_Create_Wallet` | steps + wallet theory |
| 3 | Smart contract on a test network for a Bank account: deposit, withdraw, show balance | `A3_Bank_Account_Contract` | `Bank.sol` + Remix steps |
| 4 | Solidity Student data using structures, arrays, fallback; deploy and observe gas and transaction fee | `A4_Student_Data_Contract` | `StudentData.sol` + gas table |
| 5 | Survey report on types of blockchains and real-time use cases | `A5_Survey_Report_Blockchain_Types` | full report (print it) |
| 6 | Create a Business Network using Hyperledger | `A6_Hyperledger_Business_Network` | `model.cto`, `logic.js`, `permissions.acl` + steps |
| 7 | Mini project: blockchain-based dApp for e-voting | `A7_MiniProject_eVoting_dApp` | `Voting.sol` + `index.html` front end |

All `.sol` files compile with Solidity 0.8.x (verified with solc 0.8.26).

## Fastest exam path for any contract
remix.ethereum.org → new file → paste → **Compile** → **Deploy & Run** → Environment **Remix VM** → Deploy → call functions → show the transaction in the terminal (gas, transaction cost).
If they insist on a *test network*: Environment = **Injected Provider – MetaMask** with MetaMask on **Sepolia**. Keep some Sepolia ETH in your wallet **before** exam day (faucets can be slow).

## Viva quick answers
- **Blockchain:** a distributed, immutable ledger of blocks linked by hashes. Each block holds data, a timestamp, the previous block's hash, a nonce and a Merkle root.
- **Consensus:** PoW (miners solve a hash puzzle; Bitcoin), PoS (validators stake coins; Ethereum since "The Merge", Sep 2022), DPoS, PBFT, Raft (Hyperledger).
- **Smart contract:** self-executing code on the blockchain (Solidity → bytecode → EVM).
- **Gas:** the unit of computation. **Fee = gas used × gas price** (Gwei). A simple transfer = 21,000 gas.
- **Solidity keywords:** `pragma`, `contract`, `mapping`, `struct`, `address`, `msg.sender`, `msg.value`, `payable`, `view` (reads state), `pure` (no state), `require`, `modifier`, `event`/`emit`, `fallback`, `receive`, `constructor`.
- **Data locations:** `storage` (permanent, costly), `memory` (temporary), `calldata` (read-only function args).
- **Wallet:** stores private keys. Public key → address (last 20 bytes of the Keccak-256 hash).
- **Merkle tree:** hash tree for efficient verification of transactions in a block.
- **Double spending** is prevented by consensus plus the ordering of transactions.
- **Hyperledger Fabric:** permissioned, no cryptocurrency, chaincode, channels, MSP, ordering service. Flow = execute → order → validate.
- **dApp:** front end + smart contract back end + wallet (MetaMask) + web3/ethers.js library.
- **Testnets:** Sepolia, Holesky (Goerli is deprecated). **Remix VM** is a local in-browser simulated chain.
