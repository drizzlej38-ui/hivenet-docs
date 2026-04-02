# SRM — Secure Resource and Messaging
## HiveNet Communications Subsystem

*Emerged from a design session between DJ, Gemini, and ChatGPT on March 16, 2026.*
*Starting point: a simple question about phishing protection.*
*Destination: a sovereign communications protocol addressing 50 years of internet messaging failures.*

---

## The Problem

The current email and file transfer infrastructure has three fundamental flaws that have existed since the beginning and never been fixed:

**Flaw 1 — Files move.** When you send a file, you create copies on your device, the sending server, the receiving server, and the recipient's device. You lose all control the moment it leaves. Malware travels the same path as legitimate files.

**Flaw 2 — Content executes.** Email clients render HTML, run CSS, load remote images, execute scripts. A message is treated like a mini-website. This is why phishing works. This is why tracking pixels work. This is why opening an email can compromise a device.

**Flaw 3 — Identity is singular.** One email address is used for everything. Compromise one service, expose the address everywhere. The attack surface is your entire digital identity.

SRM solves all three.

---

## Core Principles

**Files never move. Access grants move.**

**Security is a network utility, not an endpoint add-on.**

**Identity is ephemeral and burnable per communication path.**

**Nothing lands on the user's device without explicit verified consent.**

---

## The AGP — Access Grant Pointer

The Access Grant Pointer replaces the attachment entirely.

Instead of sending a file, the sender transmits a cryptographically signed permission token pointing to the file at its source with defined access parameters.

### Token Format
agp:v1:sha256:[content_hash]:[access_level]:ttl=[seconds]:thresh=[n/m]
### Access Levels

| Level | Description |
|---|---|
| PREVIEW_ONLY | Flattened static image of content, non-executable |
| READ_ONLY | Raw content access, no modification |
| REMOTE_EDIT | Recipient can modify file at source |

### Key Fields

- **content_hash** — SHA256 hash of the resource at source
- **ttl** — Time to live in seconds. Tokens expire. Entropy is a feature.
- **thresh** — Verification threshold. `2/3` means 2 of 3 triage nodes must validate before access grants.

### The Valet Key Analogy

An AGP token is like a valet key — grants limited access, is revocable at any time by the issuer, and is traceable. When you're done, you revoke it. The file never moved.

---

## Mesh Triage

Security as a network utility. Every incoming message is processed by temporary Hive nodes before reaching the user.

### Triage Pipeline
Incoming message
│
▼
Sanitizer Node
(strip HTML, CSS, tracking pixels, remote loads)
│
▼
Detonation Node(s)
(open attachments in isolated container,
check for outbound calls, malicious scripts)
│
▼
Consensus Check
(n/m nodes must agree message is clean)
│
├── CLEAN → deliver sanitized message + AGP tokens to user
└── FLAGGED → reject, log ORIGIN_STAMP to reputation ledger
### Node Behavior

- **Sanitizer** — strips all active content. HTML becomes plain text. Remote image loads blocked. Tracking pixels killed before they can phone home.
- **Detonation** — opens attachments in non-persistent isolated container. If container attempts outbound connection — flagged. Container self-terminates regardless.
- **Render Proxy** — if user requests "fancy" view, node renders HTML to static screenshot and streams the image. User sees the email. User never runs the code.

### Self-Terminating Infection Containment

If a triage node gets infected during detonation, it self-terminates the container. The infection dies with the session. The user never sees raw potentially malicious content. The Hive moves on.

---

## Ephemeral Routing Identities

Each sender-recipient communication path is unique. No two senders reach you through the same route.

If one path is compromised — burn it. The primary identity is untouched. Other communication paths are unaffected.

This implements perfect forward secrecy at the identity layer — a level of protection most enterprise systems still lack.

---

## Zero Persistence by Default

Content never lives on the user's device unless explicitly pulled after multi-node verification.

When you close the viewport — the session ends. The content disappears with it. Nothing persists without consent.

---

## HAP Integration

SRM extends the HiveNet Agent Protocol with new fields:

### New HAP Fields
[RESOURCE_POINTER: agp:v1:sha256:abc123:read:ttl=3600:thresh=2/3]
[ACCESS_LEVEL: READ_ONLY]
[TTL: 3600]
[ORIGIN_STAMP: 0.97_B229FX]
[CONTAINMENT: LEVEL_1_STRIPPED]
[DETONATION_REF: HIVE_NODE_402/SESSION_V01]
[VERIFICATION_THRESHOLD: 2/3]
[SOURCE: local/cloud]
### Example SRM HAP Message
[ROLE: SANITIZER_AGENT]
[TO: USER_PRIMARY]
[ORIGIN_STAMP: 0.97_B229FX]
[CONTAINMENT: LEVEL_1_STRIPPED]
[SECURITY_STATUS: CLEANED]
[REMOVED_ELEMENTS: 3x tracking pixels, 1x remote CSS load, 2x JS listeners]
[MESSAGE:] Hi. Here are the schematics we discussed.
[RESOURCE_POINTER: agp:v1:sha256:abc123:preview:ttl=86400:thresh=2/3]
[ACCESS_LEVEL: PREVIEW_ONLY]
[END]
---

## HAP Roles

### SANITIZER_AGENT
First contact for all external HAP traffic. Strips active content. Returns plain text and AGP tokens only. Mandatory for all incoming messages.

### TRIAGE_AGENT
Coordinates the detonation and consensus process. Assigns nodes. Collects results. Makes deliver/reject decision. Updates reputation ledger.

### DETONATION_NODE
Opens content in isolated non-persistent container. Reports findings to TRIAGE_AGENT. Self-terminates after report regardless of outcome.

### RENDER_PROXY
On user request, renders HTML/rich content to static screenshot. Streams image to user. Never passes executable content to user device.

---

## Reputation Ledger

Every node in the Hive maintains a shared ledger of sender reputation scores derived from triage outcomes.

- Clean sends increase ORIGIN_STAMP score
- Flagged sends decrease score
- Score propagates instantly across all nodes
- Low-score senders face increased verification thresholds
- Making it pointless and expensive to use SRM as an attack vector

The network becomes safer the more it is used. Innate immunity.

---

## Why This Matters Beyond Email

The most significant long-term application of SRM is not email replacement.

It is **agent communication security**.

As autonomous AI agents communicate across the HiveNet mesh, they need:
- Trusted message validation
- Payload isolation
- Resource access control
- Audit transparency

SRM provides all four at the protocol level. An agent on one node cannot poison another node through a malicious HAP message. The triage layer catches it. The container self-terminates. The ledger updates.

HiveNet's mesh becomes self-immunizing.

---

## Compute Distribution

The primary objection to sandboxing-based security is compute cost. For a centralized system this is a real constraint.

For a distributed mesh it is an asset.

Nodes with excess CPU and low bandwidth can contribute as triage and detonation nodes — earning reputation and sovereignty credits for providing security services to the network. The cost distributes across the mesh. The protection is universal.

Security becomes a contribution, not a burden.

---

## Implementation Priority

1. **AGP token format** — finalize compact string specification
2. **HAP_ROLES definition** — formalize SANITIZER, TRIAGE, DETONATION, RENDER roles
3. **Pointer handshake logic** — step by step how a node requests AGP access
4. **Reputation ledger schema** — how scores are stored, propagated, queried
5. **Triage pipeline implementation** — actual node coordination code

---

## Origin Note

This subsystem was not planned. It emerged from following an instinct.

DJ noticed a phishing attempt, asked Gemini about email security, followed the thread through email masking, sandbox triage, file attachment liability, and arrived — without a map — at a sovereign communications protocol that solves problems the internet has carried for fifty years without fixing.

The same pattern. The same instinct. The same result.

No coincidences.

---

*SRM.md — HiveNet Repository*
*CC0-1.0 — No rights reserved*
*The network becomes safer the more it is used.*