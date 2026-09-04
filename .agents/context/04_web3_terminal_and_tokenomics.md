# CONTEXT 04: WEB3 TERMINAL, TOKENOMICS & ROUTING PROTOCOL

## 1. Web3 Terminal Invariants
- **Non-Custodial Seed Vault (`SeedVault`)**: BIP39 12-word mnemonic phrases derived using BIP44 standard paths (`m/44'/60'/0'/0/0` for EVM, `m/44'/501'/0'/0'` for Solana).
- **Private Key Isolation**: Private keys are encrypted using Tink Keystore AEAD blobs prior to local database storage. Plain keys are never stored in SharedPreferences or plaintext Room columns.

## 2. In-Chat Syntax & Transaction Routing
- **Syntax Parser (`TransactionParser`)**: Detects `$send <amount> <symbol> <recipient>` in active chat inputs.
- **Developer Protocol Routing Fee**:
  - `DEV_FEE_PERCENT = 0.005` (0.50% protocol tax on all transfers, tips, and swaps).
  - EVM Treasury: `0x71C836021A5d36e2d93e1176b6C1b7Ec89931b26`
  - Solana USDT Treasury: `ExefqgPCryGs91WSo8p9AwNPM3aB7fKPoyb9iwx2bqbD`
  - SPL Mint Addresses: USDT (`Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB`), USDC (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`).

## 3. External Wallet Bridges & DEX Aggregators
- Integrates Reown AppKit / WalletConnect v2 for pairing external wallets (Phantom, Trust Wallet, MetaMask).
- In-app swap simulator interfaces Jupiter DEX routing rules on Solana and Uniswap v3 routing on EVM.
