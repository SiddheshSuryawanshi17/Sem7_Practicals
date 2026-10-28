# BT Assignment 1 – Installation of MetaMask and study spending Ether per transaction

## Aim
Install the MetaMask wallet and study how much Ether is spent per transaction (gas fee).

## Steps (demo in exam)
1. Open Chrome/Edge → go to **https://metamask.io/download** → *Install MetaMask for Chrome* → *Add to Chrome*.
2. Pin the fox icon in the browser toolbar.
3. Click **Create a new wallet** → agree → set a password (min 8 chars).
4. **Secure wallet**: write down the 12-word Secret Recovery Phrase → confirm it.
   (Never share this phrase. Anyone with it controls the wallet.)
5. Turn on test networks: click the network dropdown (top-left) → **Show test networks** → select **Sepolia**.
6. Get free test Ether from a faucet, e.g. search "Sepolia faucet" (Google Cloud Web3 faucet / Alchemy / Infura faucet) → paste your account address → receive 0.05–0.5 SepoliaETH.
7. **Send a transaction**: create a second account (Account icon → *Add account*) → from Account 1 click **Send** → paste Account 2 address → amount 0.001 → *Next*.
8. On the confirmation screen note the **estimated gas fee** → *Confirm*.
9. Open **Activity** tab → click the transaction → *View on block explorer* (sepolia.etherscan.io).

## Observation table (fill from Etherscan)
| Field | Value |
|---|---|
| Transaction hash | 0x... |
| From / To | 0x... / 0x... |
| Value sent | 0.001 ETH |
| Gas Limit | 21,000 (a simple ETH transfer always uses 21,000 gas) |
| Gas Used | 21,000 |
| Gas Price | e.g. 1.5 Gwei |
| **Transaction Fee** = Gas Used × Gas Price | 21,000 × 1.5 Gwei = 31,500 Gwei = 0.0000315 ETH |

## Theory points
- **Gas**: unit that measures the computational work needed for an operation on Ethereum.
- **Gas price**: Ether paid per unit of gas, in **Gwei** (1 Gwei = 10⁻⁹ ETH; 1 ETH = 10¹⁸ wei).
- **Gas limit**: max gas the sender is willing to spend; unused gas is refunded.
- **EIP-1559 fee** = Gas Used × (Base Fee + Priority Fee/Tip). The base fee is burned and the tip goes to the validator.
- A plain ETH transfer costs 21,000 gas. Contract calls cost more because they run code.
- Fees rise when the network is congested (higher base fee).

## Conclusion
MetaMask was installed and connected to the Sepolia test network. A transaction was sent, and its Ether spending was calculated as Gas Used × Gas Price.
