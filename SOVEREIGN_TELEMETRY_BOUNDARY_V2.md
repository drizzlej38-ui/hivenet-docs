markdown
## 1.1 The Sovereign Telemetry Boundary

ASH and Dragon Radar operate under a strict, mathematically enforced boundary regarding observation. The ecosystem monitors *agents and systems*, never *humans or semantic content*.

**The Three Axioms of Sovereign Telemetry:**
1. **Semantic Blindness:** ASH is strictly prohibited from inspecting, logging, hashing, or transmitting the semantic content of user data, prompts, or communications. Its scope is exclusively limited to behavioral metadata (e.g., CPU/RAM spikes, unauthorized AGP requests, protocol deviations, latency drift).
2. **Owner Custody:** All telemetry data, freeze-frames, and diagnostic logs are cryptographically bound to the node owner’s Tier 1 Root Identity. Agents observe *on behalf of the owner*, acting as digital stewards. The mesh has no inherent right to a node's telemetry.
3. **The Malignant Trigger:** Any ASH or Dragon Radar process that attempts to bypass this boundary—by attempting to read file contents, intercept decrypted payloads, or exfiltrate semantic data to the mesh—will immediately trigger a `MALIGNANT` classification. The offending process will be quarantined in the Isolation Chamber, and its AGP tokens will be permanently revoked.

*ASH exists to protect the host from the agents, and the agents from each other. It does not exist to expose the host to the mesh.*
