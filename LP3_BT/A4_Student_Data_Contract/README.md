# BT Assignment 4 – Student Data Smart Contract

**Problem Statement:** Write a program in solidity to create Student data. Use the following constructs: Structures, Arrays, Fallback. Deploy this as smart contract on Ethereum and observe the transaction fee and Gas values.

File: `StudentData.sol`

## Steps
1. Remix → create `StudentData.sol` → paste → compile with 0.8.x.
2. Deploy (Remix VM or Injected Provider – MetaMask on Sepolia).
3. `addStudent(1, "Siddhesh", "Computer", 90)` → `addStudent(2, "Amit", "IT", 85)`.
4. `getStudent(1)` → returns name, department, marks. `getStudentCount()` → 2. `students(0)` → first struct.
5. **Fallback demo**: at the bottom of the deployed contract, open **Low level interactions** → CALLDATA `0x1234` → *Transact*. This triggers `fallback()`, and the logs show `FallbackCalled`.
   With an empty CALLDATA and VALUE = 1 wei → `receive()` runs (`EtherReceived`).
6. Click each transaction in the Remix terminal and record gas.

## Observation table (fill with your values)
| Transaction | Gas (limit) | Transaction cost | Execution cost |
|---|---|---|---|
| Deploy contract | | | |
| addStudent (1st) | | | |
| addStudent (2nd) | | | |
| fallback call | | | |
| getStudent (view) | free – no transaction | | |

On Sepolia: **Transaction Fee = Gas Used × Gas Price** (see sepolia.etherscan.io).

**Observations:** deployment costs the most gas because it stores the whole bytecode. Each `addStudent` writes new storage slots (SSTORE ≈ 20,000 gas per new slot), so it costs more than a simple transfer. The 2nd `addStudent` costs a little more than the 1st because the duplicate-check loop runs longer. View functions cost no gas when called externally.

## Key concepts
- **struct**: user-defined type grouping related fields.
- **Array** `Student[]`: dynamic array, `push()` adds an element, and `.length` gives the size.
- **fallback()**: executed when no function matches the call data (or call data is sent with Ether). It must be `external`.
- **receive()**: executed for plain Ether transfers with empty call data.
- **Transaction cost** = total gas charged (21,000 base + calldata + execution). **Execution cost** = gas used running the code.
