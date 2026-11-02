# BT Assignment 2 – Create your own wallet using MetaMask for crypto transactions

## Aim
Create a crypto wallet with MetaMask, then send and receive test Ether between accounts.

## Steps
1. Install MetaMask (see A1) → **Create a new wallet** → set password → save the **Secret Recovery Phrase**.
2. Your first account (**Account 1**) is created. Click the address to copy it (starts with `0x`, 42 chars).
3. Select network **Sepolia** (enable *Show test networks* in settings if hidden).
4. Fund the wallet using a Sepolia faucet.
5. Create **Account 2**: account icon → *Add account or hardware wallet* → *Add a new account*.
6. **Send**: Account 1 → *Send* → paste Account 2 address → amount → *Next* → review gas fee → *Confirm*.
7. **Receive**: switch to Account 2. The balance increases once the transaction is mined.
8. Check **Activity** → transaction status *Confirmed* → view it on sepolia.etherscan.io.
9. (Optional) **Import account**: *Import account* → paste a private key. **Export private key**: Account details → *Show private key*.

## Wallet concepts to explain in viva
- **Wallet** = software that stores your **private keys**, not your coins. Coins live on the blockchain.
- **Private key** → generates the **public key** (ECDSA, secp256k1) → hashed with **Keccak-256** → last 20 bytes = **address**.
- **Seed phrase** (BIP-39, 12/24 words) can regenerate all accounts (HD wallet, BIP-32/44).
- **Hot wallet** (online: MetaMask, Trust Wallet) vs **Cold wallet** (offline: Ledger, Trezor, paper wallet).
- **Custodial** (exchange holds keys, e.g. WazirX/Binance) vs **Non-custodial** (you hold keys, e.g. MetaMask).
- Every transaction is **signed** with the private key; nodes verify the signature with the public key.

## Conclusion
A non-custodial wallet was created with MetaMask, and test Ether was transferred between two accounts on Sepolia.
