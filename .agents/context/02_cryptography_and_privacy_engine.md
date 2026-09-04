# CONTEXT 02: CRYPTOGRAPHY & PRIVACY ENGINE SPECIFICATION

## 1. Core Primitives & Libraries
- **Libsodium X25519 / Ed25519**: Diffie-Hellman key exchange, asymmetric signature authentication.
- **Google Tink Keystore AEAD (`AES256_GCM`)**: Hardware-backed Android Keystore master key wrapping.
- **Argon2id**: High-work-factor Key Derivation Function (KDF) for user master passphrase derivation.
- **HKDF-SHA256**: HMAC-based key derivation for Double Ratchet root, sending, and receiving chains.

## 2. Double Ratchet State Machine
- **Root Chain**: Advances on every DH exchange (new ephemeral X25519 key pair per ratchet step).
- **Symmetric Ratchet Chains**:
  - `Sending Chain`: Generates ephemeral message keys for outbound messages.
  - `Receiving Chain`: Advances on inbound messages; skipped message keys are stored temporarily (max 2000 keys) to handle out-of-order packet delivery.
- **Forward Secrecy & Break-in Recovery**: Compromise of a single message key does not reveal past or future messages.

## 3. Signal-Grade Privacy Engine
- **Sealed Sender Protocol**: The outer transport envelope contains only an encrypted receiver token. Plain sender identity is hidden inside the ciphertext.
- **TURN IP Masking**: Voice and video WebRTC streams route through relay TURN servers to conceal peer IP addresses and geolocation.
- **24-Hour Disappearing Messages**: Local and remote messages are tagged with a deterministic `expiresAt` timestamp. The database executes background zeroization and deletion upon expiration.
- **FLAG_SECURE**: All Android activities and dialogs enforce `WindowManager.LayoutParams.FLAG_SECURE`.
