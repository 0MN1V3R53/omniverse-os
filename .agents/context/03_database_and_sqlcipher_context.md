# CONTEXT 03: DATABASE & DETERMINISTIC SQLCIPHER STORAGE CONTEXT

## 1. Storage Architecture
- **Engine**: Android Room Database with SQLCipher 4.5+ full database encryption.
- **Passphrase Management**:
  - Master database passphrase is generated randomly (256-bit secure entropy) on initial application setup.
  - The passphrase is encrypted using Google Tink Keystore AEAD and persisted in `DatabaseKeyStorage`.
  - Raw passphrase bytes are unwrapped in memory only during Room open hooks and immediately zeroized.

## 2. Core Database Entities
- `UserEntity`: Local user profile, Ed25519 identity public key, registration timestamp.
- `ContactEntity`: Peer public keys, ratchet state session IDs, trust verification status.
- `MessageEntity`: Encrypted message ciphertext, sender public key, conversation ID, timestamp, expiration timestamp (`expiresAt`), delivery status (`PENDING`, `SENT`, `DELIVERED`, `READ`).
- `TransactionEntity`: In-chat transaction hash, sender, recipient, gross amount, developer fee (0.5%), token symbol, chain type (`EVM`, `SOLANA`), block status.

## 3. Security & Concurrency Guidelines
- All database read/write queries must execute on background threads (`Dispatchers.IO`).
- Write operations with multiple entity updates must execute within `@Transaction` blocks to prevent database state corruption during power loss.
- Periodic cleanup worker queries and purges expired messages (`WHERE expiresAt < :currentTimeMillis`).
