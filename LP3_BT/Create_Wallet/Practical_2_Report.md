# Blockchain Technology (410243) Lab: Practical 2 - Create your own wallet using MetaMask for crypto transactions

Tools used: MetaMask (browser extension), Remix IDE (app.remix.live), Sepolia test network, Sepolia Etherscan

## Aim

To create a crypto wallet using MetaMask and perform a transaction between two accounts on the Ethereum Sepolia test network.

## Theory

**Crypto wallet.** A wallet does not store coins. It stores the key pair that controls an address on the blockchain.

- Public address (for example `0x839f...e269b`): shared with others to receive funds.
- Private key: signs transactions. Whoever has it controls the funds, so it is never shared.
- Secret Recovery Phrase (12 words): regenerates every private key in the wallet. If it is lost, the wallet cannot be recovered. If it leaks, the funds can be stolen.

**MetaMask.** A non-custodial wallet available as a browser extension and mobile app. The keys stay on the user's device. It signs transactions and connects the browser to Ethereum-based networks and dApps.

**Hot and cold wallets.** A hot wallet is connected to the internet (MetaMask). A cold wallet stays offline (hardware wallets such as Ledger, or paper wallets).

**Testnet.** A copy of the Ethereum network where the ether has no real value. Developers use it to test transactions and contracts for free. Sepolia is the main Ethereum testnet for application development (chain ID 11155111).

**Faucet.** A website that gives out free testnet ether. The PoW (proof-of-work) faucet makes the user's browser solve hash puzzles before it pays out. This stops bots from draining the faucet. The mining only proves effort to the faucet. It does not create Sepolia blocks, because Sepolia itself runs on proof of stake.

**Gas.** Every transaction costs gas, paid in ETH.

```
Transaction fee = Gas used × Gas price
```

A plain ETH transfer always uses 21,000 gas.

**Block explorer.** A website such as Etherscan that reads the public blockchain and shows every transaction, block and address.

## Procedure

### A. Install MetaMask and create a wallet

1. Open Chrome and go to `metamask.io`. Click Download, then "Add to Chrome" in the Chrome Web Store. Pin the fox icon to the toolbar.
2. Open MetaMask and select **Create a new wallet**. Accept the terms.
3. Set a password. This password only unlocks MetaMask on this computer.
4. Write down the 12-word Secret Recovery Phrase in order, then confirm it by filling in the missing words.
5. The wallet opens on **Account 1**. Copy the public address using the copy icon next to it.

### B. Show and select the Sepolia test network

6. Click the ☰ menu, open **Networks**, and turn on **Show test networks**.
7. Go to **Home**, open the **Tokens** tab, click the network filter and select **Sepolia**.

### C. Get test ether from the faucet

8. Open the Sepolia PoW Faucet (`sepolia-faucet.pk910.de`), paste the wallet address and start mining.
9. When enough reward has been collected, stop mining and claim it.
10. The faucet sends the reward as a normal transaction. The SepoliaETH balance appears under Tokens with the Sepolia filter applied.

### D. Perform a transaction

11. Click the account name, choose **Add account**, and create **Account 2**. Copy its address.
12. Switch back to Account 1 and click **Send**.
13. Paste Account 2's address, enter `0.01` as the amount, and check that the network is Sepolia.
14. Note the network fee shown before confirming, then click **Confirm**.
15. The transaction shows as Pending and then Confirmed. Switch to Account 2 to see the balance of 0.01 SepoliaETH.

### E. Verify on the block explorer

16. Switch to **Account 1** (the sender), open **Activity**, click the transaction and select **View on block explorer**.
    - On testnets, MetaMask's Activity tab usually lists only transactions the account sent. The receiving account (Account 2) may show an empty Activity list even though its balance went up.
    - Another option is to search either address directly on `sepolia.etherscan.io`.
17. On the Etherscan transaction page, note these fields:

| Field | Meaning |
|---|---|
| Transaction Hash | Unique ID of the transaction |
| Status | Success or Failed |
| Block | Block number the transaction was included in |
| From / To | Sender and receiver addresses |
| Value | Amount of ETH transferred |
| Gas Limit & Usage | 21,000 gas for a plain transfer |
| Gas Price | Price paid per unit of gas |
| Transaction Fee | Gas used × gas price |

## Observations

| Item | Value |
|---|---|
| Account 1 (sender) | `0x839f9da646036e73df8dc28731c0ed08280e269b` |
| Account 2 (receiver) | `0xD5AF7...A026A` |
| Faucet reward | 2.5 SepoliaETH, confirmed in block #12049135 |
| Faucet transaction hash | `0x03a41b500b0c33f47a1cf41c604d370e9caab1fe2067c2650d158df00e873877` |
| Amount transferred | 0.01 SepoliaETH (Account 1 to Account 2) |
| Account 2 balance after transfer | 0.0100 SepoliaETH |
| Gas used | 21,000 |

## Output

The MetaMask wallet was created and test ether was received from the Sepolia PoW faucet. 0.01 SepoliaETH was transferred from Account 1 to Account 2 on the Sepolia test network, and the transaction was verified on Sepolia Etherscan.

## Conclusion

We created a non-custodial wallet in MetaMask, funded it with testnet ether, and sent a transaction between two accounts. The transfer used 21,000 gas, and the transaction appeared publicly on the block explorer with its hash, block number, sender, receiver and fee.
