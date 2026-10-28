# BT Mini Project – E-Voting dApp

**Problem Statement:** Develop a Blockchain based application dApp (de-centralized app) for e-voting system.

| File | Purpose |
|---|---|
| `Voting.sol` | Smart contract: candidates, voter registration, one-vote-per-voter, winner |
| `index.html` | Web front end (talks to MetaMask using ethers.js) |
| `ethers.umd.min.js` | ethers.js v6 library kept locally, so the CDN is not needed |

## Option A – Only Remix (fastest, works without MetaMask)
1. Remix → `Voting.sol` → compile → Deploy (Remix VM). Account 1 = **admin**.
2. `addCandidate("Alice")`, `addCandidate("Bob")`.
3. Copy Account 2 and Account 3 addresses (ACCOUNT dropdown) → `registerVoter(<address>)` for each.
4. `startVoting()`.
5. Switch ACCOUNT to Account 2 → `vote(0)`. Switch to Account 3 → `vote(1)`. Try voting again → reverts "already voted".
6. Switch back to Account 1 → `endVoting()` → `getWinner()`.

## Option B – Full dApp with front end
1. MetaMask on **Sepolia** with test ETH.
2. Remix → Environment **Injected Provider – MetaMask** → Deploy → copy contract address.
3. Open `index.html` through a local server (MetaMask does not inject into `file://` pages):
   ```
   cd A7_MiniProject_eVoting_dApp
   python -m http.server 8000
   ```
   Then browse to http://localhost:8000
4. Paste the contract address → **Connect MetaMask** → add candidates, register voters, start voting → vote → end → show winner.

## Features / security
- Only admin can add candidates, register voters, start/end voting (`onlyAdmin` modifier).
- One vote per registered address (`hasVoted` mapping).
- Votes are stored on chain, so they are transparent, tamper-proof and publicly verifiable.
- Events (`Voted`, `CandidateAdded`) give an audit trail.
