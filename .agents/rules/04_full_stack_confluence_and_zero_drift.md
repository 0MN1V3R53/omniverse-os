# RULE 04: FULL-STACK CONFLUENCE & ZERO-DRIFT DIRECTIVE

## 1. Absolute Zero-Drift Mandate
1.1 **Zero Placeholders**: Stubbed implementations, incomplete classes, truncated expressions, and placeholder comments (`// TODO`, `/* Implement later */`, `pass`, `...`) are strictly prohibited in all modules.
1.2 **Zero Synthetic / Mock Data**: Real production patterns, verified cryptographic curves (Curve25519/Ed25519), real SQLCipher database bindings, and standard BIP39/BIP44 derivation paths must be used.
1.3 **Exact Type and Signature Match**: All inter-module calls between `core-crypto`, `core-database`, `core-identity`, `core-network`, `core-web3`, `feature-chat`, `feature-profile`, and `feature-webrtc` must align with exact public signatures.

## 2. Cross-Layer Confluence Rules
- **Crypto <-> Database**: All encrypted message payloads stored in `AegisDatabase` must be generated via `CryptoEngine` Double Ratchet ciphertexts; database keys must be derived deterministically via Keystore AEAD.
- **Web3 <-> In-Chat Engine**: `$send` syntax parsed in `TransactionParser` must invoke `AegisWalletManager.executeInChatTip` with deterministic 0.5% developer protocol routing fees and produce valid cryptographic transaction hashes.
- **Identity <-> Network/Signaling**: WebRTC signaling in `SignalingClient` and Firebase message synchronization in `FirebaseMessageSyncRepository` must authenticate peer identities via Ed25519 public keys without exposing plain IP addresses (Signal-grade TURN masking).
- **UI/UX <-> Theme Engine**: All Jetpack Compose UI components must consume dynamic tokens from `ThemeEngine` (CYBERPUNK_NEON, DARK_MOON, CYBER_SUNRISE, CLASSIC_DARK) with zero hardcoded color values.
