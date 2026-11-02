# BT Assignment 3 – Bank Account Smart Contract

**Problem Statement:** Write a smart contract on a test network, for Bank account of a customer for the following operations: Deposit money | Withdraw Money | Show balance.

File: `Bank.sol`

## How to run in Remix (5 minutes)
1. Open **https://remix.ethereum.org** → *File explorer* → create `Bank.sol` → paste the code.
2. **Solidity Compiler** tab → compiler `0.8.x` → *Compile Bank.sol* (green tick).
3. **Deploy & Run** tab:
   - Environment: **Remix VM (Cancun)**. Works without MetaMask and gives 100 fake ETH accounts.
   - For a real *test network*: choose **Injected Provider – MetaMask** and set MetaMask to Sepolia.
4. Click **Deploy**. The contract appears under *Deployed Contracts*.
5. Demo:
   | Action | How |
   |---|---|
   | `createAccount` | click |
   | `deposit` | set **VALUE** box (top of Deploy tab) to `2` and unit `ether` → click `deposit` |
   | `showBalance` | click → shows `2000000000000000000` (wei = 2 ETH) |
   | `withdraw` | enter `1000000000000000000` (1 ETH in wei) → click |
   | `showBalance` | now `1000000000000000000` |
   | error demo | withdraw more than balance → transaction reverts with "Insufficient balance" |
6. Open the transaction in the Remix terminal to show **gas** and **transaction cost**.

## Key concepts
- `payable` function can receive Ether; `msg.value` = Ether sent (in wei), `msg.sender` = caller address.
- `mapping(address => uint)` stores each customer's balance.
- `require()` validates conditions and reverts with an error message (unused gas is refunded).
- `view` functions only read state, so calling them is free (no transaction).
- Balance is updated **before** transfer to prevent the re-entrancy attack.
- `event`s are logs stored on the blockchain that front ends can listen to.
