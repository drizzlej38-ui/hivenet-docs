# HiveNode Sovereign Mesh Architecture
### Semi-Autonomous Nodes, Dragon Radar, SRM, and Owner-Audited Identity

---

## Design Principle

A node's sovereignty is defined by **owner control**, not by evading observation.

- Nodes MAY be selective about who they broadcast to (friendly groups, private pools, invite-only mesh segments).
- Nodes MAY use encryption and non-broadcast routing so traffic content/metadata isn't visible to outsiders.
- Nodes MUST remain fully inspectable by their own device owner at all times.
- Nodes MUST NOT spoof hardware identity, defeat forensic inspection, or auto-mutate specifically to evade scrutiny from legitimate authority (owner, network admin, mesh auditor).

This is the line: **selective disclosure to peers = sovereignty. Opacity to your own owner = a different kind of system, and out of scope here.**

---

## 1. Node Architecture

```
HiveNode
 ├── Identity & Trust System
 ├── Mesh Networking Layer
 ├── Resource Scanner
 ├── Service Manager
 ├── Task Scheduler
 ├── Security Sandbox
 ├── Storage Layer
 ├── AI Assistant/Agent Layer (optional)
 └── Owner Policy Controls (unconditional inspection + kill switch)
```

Nodes self-report real hardware capability (CPU, RAM, storage, GPU/NPU, battery, network interfaces) to enable role assignment. No spoofed values — the network's trust model depends on nodes being honest about what they actually are.

---

## 2. Node Roles

- **Relay** — maintains mesh connectivity and routing
- **Compute** — AI inference, rendering, distributed workloads
- **Storage** — encrypted distributed archives
- **Sensor** — approved environmental/device data collection
- **Gateway** — bridges local mesh to external networks

Roles shift dynamically based on real resource availability (self-healing behavior: reroute around unavailable neighbors, replicate data on storage-node failure, throttle under resource pressure).

---

## 3. Extended Dragon Radar (EDR)

Distributed local awareness — each node maintains a partial picture, no global map required.

```
Dragon Radar View
 ├── Nearby Nodes (within visibility scope)
 ├── Available Resources
 ├── Network Paths
 ├── Trust Status
 ├── Service Availability
 ├── Performance Health
 └── Threat Indicators
```

"Nearby" is scoped by **group membership**, not by network-wide broadcast. A node in Group A has no visibility into Group B's Dragon Radar view unless bridged intentionally via a Gateway node.

---

## 4. SRM (Secure Resource Management)

Governs access, quota, duration, and conditions for resource requests. Every grant is scoped, time-boxed, and audit-logged locally on the granting node — visible to that node's owner on request.

```
Resource Request:
 Requester: Node-472
 Need: 2 CPU cores
 Purpose: AI inference
 Duration: 30 minutes
 Trust: Verified
 SRM Decision: APPROVED
 Limit: 20% CPU allocation
 Audit: Enabled (owner-visible)
```

---

## 5. Group-Scoped Visibility (Selective Disclosure)

This is the legitimate version of "hide at will":

- Nodes join one or more **trust groups** (friend groups, project pools, org meshes).
- A node broadcasts presence/service availability **only within its joined groups** by default.
- Cross-group visibility requires an explicit bridge (Gateway node + mutual permission), never automatic.
- To outsiders (non-group members), the node is simply not discoverable — this is access control, not identity evasion. The node's traffic isn't hidden from its own network path, just unadvertised to strangers.

This satisfies "broadcast only to friendly nodes" without needing hardware spoofing or anti-forensic measures — it's routing-layer permissioning, same category as a private VPN mesh or invite-only federation.

---

## 6. Identity: Epoch-Based Pseudonyms (Owner-Audited)

A three-tier identity model gives nodes privacy from **outside observers** while preserving full auditability by the node's own owner.

```
[ Tier 1: Root Identity ]     Ed25519 keypair, on-device only.
         │                    Never transmitted. Owner-visible always.
         ▼
[ Tier 2: Active Pool ID ]    Public pseudonym, derived from root.
         │                    Lives for a defined epoch (time or task-count based).
         │                    Used for routing + reputation within a group.
         ▼
[ Tier 3: Task-Scoped ID ]    Per-task correlation handle.
                               Discarded after task completion.
```

**Reputation portability across epochs** (optional): a blind-signature voucher lets a node prove continuity of reputation to the *mesh* without exposing linkage to outside parties — this is a standard anonymous-credential pattern (similar to privacy-preserving reputation systems), not anti-forensics. It protects against long-term behavioral profiling **by other mesh participants**, not against the node's own owner, who always holds the root identity and full local logs regardless of which pseudonym is active.

**Explicitly excluded from this design:**
- Hardware fingerprint spoofing (fake `/proc/cpuinfo`, fake MAC/UUIDs)
- Forced onion-routing specifically to defeat traceability to the host device
- Detection-triggered auto-mutation ("jump to new path when observed closely")
- Memory-scrubbing designed to defeat the owner's own forensic access

If a project needs Tor-style transport privacy for legitimate reasons (e.g. protecting group members from network-level surveillance by ISPs/state actors), that's a separate, explicit opt-in transport choice — not a default, and not bundled with identity spoofing.

---

## 7. Anomaly Detection (Resource-Focused, Not Evasion-Focused)

Baseline behavior profile per node, cold-start handled via probation period (tighter default limits until enough history exists):

```
Baseline:
 CPU: usually 5–15%
 Network: known peers only
 Storage: assigned directories only
 Processes: approved services only
```

Severity-based response — log/notify (low), throttle/verify (medium), isolate/quarantine (high). This governs **node-to-node and node-to-network anomalies**. It does not govern, and is not a justification for, hiding node behavior from its own owner.

---

## 8. Container Generator (Legitimate Hardware Detection Only)

Deployable node packages that adapt to real host capability:

```
Generate Node → Deploy → Real Hardware Assessment →
Create Identity (Tier 1 root) → Join Group(s) →
Receive Role Assignment → Operate + Self-Monitor → Update
```

Hardware assessment reports **actual** capability (used for role fitting — a phone gets a lightweight relay role, a server gets compute/storage). No spoofed values reported to the mesh. Owner permission controls (allow/deny idle CPU use, sensor access, storage use) are enforced client-side and are the actual mechanism for resource protection — not obfuscation.

**Update system** requires signed releases, staged rollout, and rollback capability — auto-updating nodes are a supply-chain risk and need their own spec (`NODE_UPDATE.md`) before this goes to production.

---

## Open Items for Future Specs

- Sybil resistance for first-time trust bootstrap (unresolved — flagged in earlier ARM ledger review)
- `NODE_UPDATE.md` — signing/rollout/rollback for the update system
- Formal probation-period parameters for anomaly baseline cold start
- Cross-group Gateway bridge permission model (who can request a bridge, how it's revoked)
