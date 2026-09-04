# CONTEXT 11: REFLEXION & ANTI-PATTERN GRAVEYARD (COLD MEMORY)

## 1. Purpose & Episodic Memory Vault
This cold-storage memory catalog preserves past failure modes, regression vectors, and hard-learned edge cases. All agents must consult this graveyard prior to modifying cryptographic, database, networking, or Web3 modules to prevent recurring bugs.

---

## 2. Cataloged Anti-Patterns & Invariant Solutions

### Anti-Pattern 01: SQLCipher Immutable String Passphrase Leak
- **Vulnerability**: Constructing the SQLCipher passphrase as a Kotlin `String` (`val password = "secret"`) leaves immutable characters in JVM heap memory susceptible to memory dump extraction.
- **Invariant Fix**: Always handle passphrases as `CharArray` or `ByteArray` directly, wrapping database initialization in a secure block and immediately zeroing out the buffer:
  ```kotlin
  val passphrase: CharArray = keystoreManager.getDatabasePassphrase()
  try {
      val factory = SupportFactory(SQLiteDatabase.getBytes(passphrase))
      // build Room database...
  } finally {
      passphrase.fill('0')
  }
  ```

### Anti-Pattern 02: Double Ratchet Skipped Key Out-of-Order Message Loss
- **Vulnerability**: In P2P mobile messaging, network latency causes messages from ratchet step $N+2$ to arrive before step $N+1$. Dropping intermediate skipped keys destroys future message decryptability.
- **Invariant Fix**: The `DoubleRatchetEngine` must compute and persist intermediate skipped message keys in an encrypted `MKSkipped` table with an expiration TTL (max 2,000 keys / 7 days) before ratcheting forward.

### Anti-Pattern 03: WebRTC DTLS-SRTP Audio Leak on Call Setup
- **Vulnerability**: Initializing local audio tracks and unmuting before DTLS-SRTP handshake completion leaks raw RTP packets over insecure networks.
- **Invariant Fix**: Keep audio/video tracks strictly muted and hold media packet transmission until `PeerConnection.IceConnectionState` reaches `CONNECTED` and DTLS cipher negotiation completes.

### Anti-Pattern 04: Solana RPC Rate-Limit Avalanche
- **Vulnerability**: Firing un-throttled balance and transaction queries against public Solana RPC endpoints causes `429 Too Many Requests` cascading failures.
- **Invariant Fix**: Implement token-bucket rate limiting with exponential backoff and jitter ($t_{wait} = 2^n \times 100\text{ms} + \text{rand}(0, 50\text{ms})$) across all RPC calls.

### Anti-Pattern 05: Unconfined Coroutine Execution in Room DAOs
- **Vulnerability**: Emitting Room Database flows directly on the caller thread risks blocking UI threads during large message history batch reads.
- **Invariant Fix**: Explicitly specify `.flowOn(Dispatchers.IO)` on all DAO flows and encapsulate write transactions in `withContext(Dispatchers.IO)`.
