# Blockchain Technology (410243) Lab: Practical 3 - Smart contract for a customer's bank account

Tools used: MetaMask (browser extension), Remix IDE (app.remix.live), Sepolia test network, Sepolia Etherscan

## Aim

To write a smart contract on a test network for a customer's bank account with the following operations:

- Deposit money
- Withdraw money
- Show balance

## Theory

**Smart contract.** A program stored at an address on the blockchain. Every node runs it in the Ethereum Virtual Machine (EVM). Once deployed, its code cannot be changed. Each new deployment creates a separate contract at a new address.

**Solidity.** A statically typed language for writing Ethereum smart contracts. It compiles to EVM bytecode and an ABI (Application Binary Interface), the JSON description of the contract's functions that tools like Remix use to call them.

**Remix IDE.** A browser-based IDE for writing, compiling, deploying and testing Solidity contracts. Selecting **Browser Extension → MetaMask** as the environment deploys to the network MetaMask is connected to (Sepolia here). **Remix VM** is a simulated blockchain inside the browser.

**Wei.** The smallest unit of ether. Contracts work in wei so they never need decimals.

| Ether | Wei |
|---|---|
| 1 ETH | 1,000,000,000,000,000,000 (10¹⁸) |
| 0.01 ETH | `10000000000000000` |
| 0.005 ETH | `5000000000000000` |
| 1 gwei | 1,000,000,000 (10⁹) |

**Solidity concepts used**

| Concept | Meaning |
|---|---|
| `mapping(address => uint256)` | Key-value store from each customer's address to their balance |
| `msg.sender` | Address that called the function |
| `msg.value` | Amount of ether (in wei) sent with the call |
| `payable` | Allows a function to receive ether |
| `view` | Function only reads data. Calling it is free and needs no transaction |
| `require(condition, "msg")` | Stops execution and reverts all changes if the condition is false |
| `event` / `emit` | Writes a log entry to the blockchain, visible in the explorer's Logs tab |
| `receive()` | Special function that runs when plain ether is sent to the contract with no function call |

**Checks-effects-interactions.** In `withdraw`, the balance is reduced before the ether is sent. This prevents a reentrancy attack, where a malicious contract calls `withdraw` again before its balance is updated. That kind of bug caused the 2016 DAO hack.

## Program (Bank.sol)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Bank {
    // each customer's address maps to their balance (in wei)
    mapping(address => uint256) private balances;

    event Deposited(address indexed customer, uint256 amount);
    event Withdrawn(address indexed customer, uint256 amount);

    // Deposit money: send ether along with this call
    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    // Withdraw money: amount is in wei
    function withdraw(uint256 amount) public {
        require(amount > 0, "Amount must be greater than 0");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount;          // update balance first
        (bool sent, ) = payable(msg.sender).call{value: amount}("");
        require(sent, "Transfer failed");

        emit Withdrawn(msg.sender, amount);
    }

    // Show balance of the caller
    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }

    // Deposit by sending ether directly to the contract address
    receive() external payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }
}
```

## Procedure

### A. Write the contract

1. Open `app.remix.live`. From the workspace dropdown, create a new workspace using the **Blank** template.
2. Create a new file named `Bank.sol`, paste the program and save it.

### B. Compile

3. Open the **Solidity Compiler** tab, choose a 0.8.x compiler version and click **Compile Bank.sol**.
4. A green tick on the compiler icon means it compiled successfully. The "infinite gas" notes next to `deposit` and `withdraw` are only estimation warnings, not errors.

### C. Connect MetaMask

5. Open **Deploy & Run Transactions** and set Environment to **Browser Extension → MetaMask**. Approve the connection in MetaMask using Account 1.
6. Check that Remix shows **Sepolia (11155111)** and the correct account address and balance.

### D. Deploy

7. Turn off **Verify Contract on Explorers**. Without an Etherscan API key it only produces extra messages.
8. Make sure Value on the Deploy tab is `0`.
9. Click **Deploy** once. The MetaMask popup should say "Deploy a contract" with "No changes" under Estimated changes. Click **Confirm**.
10. After the green tick appears in the terminal, the contract is listed under **Deployed Contracts** with its address. Expand it to see the functions:
    - Red dot: `deposit` (payable)
    - Orange dot: `withdraw` (changes state, no ether)
    - Blue dot: `getBalance` (view, free)

### E. Deposit 0.01 ETH

11. Scroll to the bottom of the deployed contract's panel. Under **Low level interaction** there is a **Value** field. Set the unit to **wei** and enter `10000000000000000`.
    - In the newer Remix (app.remix.live), the deposit button reads this Value field, not the one on the Deploy tab.
    - The field only accepts whole numbers in wei. Typing `0.01` does not work.
12. Click **Transact** next to `deposit`. In MetaMask, Estimated changes should show **−0.01 SepoliaETH** with no warning. Click **Confirm**.

Alternative way to deposit (uses `receive()`): copy the contract address, then in MetaMask click **Send**, paste the contract address, enter `0.01` and confirm.

### F. Show balance

13. Click **Call** next to `getBalance`. Output: `uint256: 10000000000000000` (0.01 ETH). No MetaMask popup appears because it is a free read.

### G. Withdraw 0.005 ETH

14. Set the Value field at the bottom of the contract panel back to `0`.
15. Enter `5000000000000000` next to `withdraw`, click **Transact**, and confirm in MetaMask.
16. Call `getBalance` again. Output: `uint256: 5000000000000000` (0.005 ETH). The withdrawn ether returns to the wallet, minus the gas fee.

### H. Verify on Etherscan

17. Copy the contract address and search for it on `sepolia.etherscan.io`. The transaction list shows the contract creation, deposit and withdraw transactions, each with its gas used and fee.

## Observations

| Operation | Input | Result | Gas cost |
|---|---|---|---|
| Deploy | Value 0 | Contract created (block #12049625) | Yes |
| deposit | 10000000000000000 wei | Balance = 10000000000000000 | Yes |
| getBalance | none | 10000000000000000 | Free (view) |
| withdraw | 5000000000000000 | Balance = 5000000000000000 | Yes |
| getBalance | none | 5000000000000000 | Free (view) |
| withdraw (more than balance) | 999999999999999999 | Reverted: "Insufficient balance" | Yes |

Contract address: `0x________________________________________` (fill in from Remix)

## Troubleshooting notes

| Problem | Cause | Fix |
|---|---|---|
| MetaMask says "This transaction is likely to fail" on deposit | Value was 0, or more than the wallet balance (it once showed 61 ether) | Cancel. Set Value to `10000000000000000` wei in the field at the bottom of the contract panel |
| Value field won't accept `0.01` | The field only takes whole numbers | Use wei (`10000000000000000`) or gwei (`10000000`) |
| Several "Bank.(constructor)" entries in the terminal | Deploy was clicked more than once | Each one is a separate contract. Use one and remove the rest from the list |
| "Etherscan verification skipped: API key not provided" | Verify Contract on Explorers was on | Harmless. Turn the toggle off before deploying |
| getBalance shows 0 after depositing | Called on a different contract instance | Use the same contract address for every operation |
| Receiving account's Activity list is empty | MetaMask lists only sent transactions on testnets | Check the sender's Activity, or search the address on Etherscan |
| remix.ethereum.org opens app.remix.live | Remix moved to a new domain | Use app.remix.live. The steps are the same |

## Output

The Bank smart contract was deployed on the Sepolia test network. 0.01 ETH was deposited, 0.005 ETH was withdrawn, and `getBalance` returned 0.005 ETH (`5000000000000000` wei). All transactions were verified on Sepolia Etherscan.

## Conclusion

We wrote a Solidity smart contract that keeps a separate balance for each customer using a mapping, and deployed it on Sepolia through Remix and MetaMask. Deposit and withdraw changed the contract's state and cost gas, while `getBalance` was a free read. The `require` checks rejected invalid operations such as withdrawing more than the available balance.
