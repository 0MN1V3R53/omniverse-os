# CONTEXT 05: WEBRTC CALLING & NETWORKING PIPELINE

## 1. WebRTC Architecture
- **P2P Audio/Video**: Google WebRTC native Android bindings.
- **Signaling Pipeline (`SignalingClient`)**: WebSocket / Firebase Realtime Database signaling transport.
- **NAT Traversal & TURN Relays**:
  - Encrypted STUN/TURN servers deployed to mask IP addresses.
  - Media packets encrypted via SRTP with DTLS 1.3 key exchange.

## 2. Real-Time Message Synchronization
- **Transport**: `FirebaseMessageSyncRepository` handles decentralized message delivery.
- **Offline Outbox**: Unsent messages are persisted locally in `MessageEntity` with `PENDING` state and dispatched automatically via WorkManager / Coroutine event bus upon network availability.
- **Push Notification Decryption**: FCM notifications contain only silent wake-up payloads; the device initiates background sync, pulls ciphertexts, and decrypts locally to prevent notification snooping.
