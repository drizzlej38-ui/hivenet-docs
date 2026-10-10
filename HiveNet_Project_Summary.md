# HiveNet Project Summary
*Compiled from project history — September 2026*

## 1. Origin & Core Vision

HiveNet is a decentralized, sovereign, consent-governed mesh network DJ has been conceptualizing for over two decades, rooted in networking studies (Cisco/LAN/fiber optics background) and a sovereignty-first philosophy. The founding idea traces back to a high-school-era concept: shared/distributed compute across all active nodes on a mesh, using each device's idle processing power, with automatic detection and throttling when the owner is actively using their device. Nodes double as communications relays, carrying traffic for others in addition to sharing compute.

The project has been described as building **"a nervous system for a digital life."** It sits inside a larger personal mission around cultural preservation and a long-term vision for a tribal sanctuary / globally recognized cultural preservation organization using oral tradition augmented by modern technology.

A provisional patent related to HiveNet has been filed. Specs live at `~/sd/projects/hivenet-docs/` locally and are mirrored at `github.com/drizzlej38-ui/hivenet-docs`.

## 2. Foundational Principles

- Opt-in consent is **load-bearing**, not decorative
- Owner control **is** the definition of node sovereignty
- Architecture must function independent of centralized platforms
- Backward compatibility with existing communication tools/networks is treated as a hard requirement for real-world adoption — HiveNet should feel like "the internet you already use," with sovereignty running underneath, not a wholesale replacement people have to opt into culturally

## 3. Core Architecture Components

| Component | Role |
|---|---|
| **ENDCAP** | Self-describing node/data wrapper. Invariants (`standalone: true`, `complete: true`, `requires_peers: false`) guarantee a container can be migrated to any new host without data or identity loss. Also used recursively at the individual knowledge-module level (see Estuary). Lets all archives across the mesh act as one unified archive *at the access layer* while ownership stays local underneath. |
| **AGP (Federation/permission layer)** | Scoped, revocable capability tokens. Can be time-windowed, one-time-use, delegable, or monitorable/revocable mid-view. Governs who can read what, including remote "blind storage." |
| **Dragon Radar** | Anomaly/behavioral detection — inspects behavior patterns, not content (see Sovereign Telemetry Boundary below). |
| **The Estuary** | Node discovery layer (organic/discovery-based, not query-based). |
| **SRM (Secure Resource Management)** | Sandboxes incoming attachments; detonates (destroys) malicious content in a safe container; offending nodes are marked untrusted and lose mesh standing. |
| **Node classes** | Composable, not exclusive (e.g. archive, gateway, ghost). Ghost nodes are structurally enforced read-metadata-only passive probes. |
| **Trust taxonomy** | verified HiveNet / verified-present / unverified / external / verified-yet-threat (insider-threat case) |

**Identity & privacy:** Three-tier visibility (peer-to-peer invisible without handshake; admin sees mesh-level metadata only; lawful process cooperated with only at opt-in disclosure) and a three-tier pseudonym system (Permanent Root ID, Active Pool ID, Transient Task ID) to resist reconstruction attacks. Admin logs capture connection metadata, never content. Opt-in is the genesis event anchoring node identity to hardware. Updates propagate peer-to-peer with no central update server.

**File sharing:** Files aren't transmitted directly — the sender shares an AGP token granting scoped access to the file on the sender's own device. Acknowledged limitation: a viewer can still screenshot while viewing.

## 4. Later Design Extensions

- **Sovereign Cloud (SOVEREIGN_CLOUD_PROVIDER.md, draft)** — addresses the real problem that local-only storage doesn't scale for most people. Remote data centers or community co-ops host "blind storage" ENDCAP nodes with zero `read_contents` permission; data is encrypted client-side before upload; AGP-scoped tokens control access. Pitched as a business case around reduced legal liability (ciphertext-only hosting) rather than data mining.
- **ASH (Artificial System Health)** — a proposed, explicitly *unproven research concept* for distributed AI-behavioral-health monitoring: mediator agents, Dragon Radar as anomaly telemetry, an "Isolation Chamber" for freeze-framing/cloning anomalous agent states, a specialist diagnostic swarm, and an ENDCAP-governed behavioral-specimen repository using a biological taxonomy (infectious/viral/latent/resistant). Framed as pending independent critique, not established architecture.
- **Sovereign Telemetry Boundary** (addition to ASH) — three axioms: semantic blindness (only behavioral metadata inspected, never content), owner custody (telemetry bound to the node owner's root identity), malignant trigger (any process attempting content access or exfiltration gets quarantined, AGP revoked).
- **IMMUNE_MEMORY.md (draft)** — Collective Immune Memory & Phenotype Sharing Protocol: nodes share cryptographic "phenotype" hashes of behavioral reactions to anomalies (not raw exploit data) via an AGP-gated Behavioral Repository, so the mesh builds shared defenses without arming attackers.

*Note: Sovereign Cloud, ASH, and IMMUNE_MEMORY are drafts from AI-assisted drafting sessions — worth a critical pass before treating as settled spec, especially ASH, which was explicitly flagged as unproven.*

## 5. Standards & Related Projects Tracked

- **A2A protocol** (v1.0, Linux Foundation, Apache 2.0) adopted as the inter-agent communication standard; an integration brief extended Agent Cards with HiveNet-specific claims (AGP tokens, SRM hooks, revocation)
- Flagged as relevant: A2A Agent Payments Protocol (AP2), W3C DID spec
- **LoRa** identified as the intended future physical layer
- Explored parallels: SSH `authorized_keys command=` restrictions vs. AGP's scoped capability model; WiFi Direct and SSH as P2P transport primitives
- Parallel projects being tracked (not part of HiveNet): The Sovereign Network (ZHTP), Meshtastic/Nostr stack
- "Real AI" (Oblivionburn's C#/.NET conversational learner) explored as a possible basis for federated, per-community cultural-guide AIs

## 6. Adjacent But Deliberately Separate Projects

- **HiveNode Container Generator** — deployable node packages that adapt to host hardware; kept on its own track, distinct from core HiveNet. An AI-drafted stealth/anonymization layer (hardware spoofing, forced Tor routing, rotating untraceable IDs) was explicitly excluded from core specs pending further thought.
- **Demosthenes and Locke** — a two-persona anonymous AI advocacy concept (named for the *Ender's Game* characters); still wanted, but intentionally not filed under HiveNet.

## 7. Applied Sub-Projects

### Estuary App (cultural preservation distributable)
A distributable app — eventually envisioned as an OS on distributable tablets — built on HiveNet's Estuary discovery layer, for sending to tribes across the Americas. Must be simple enough for an elder or anyone to record/upload cultural entries, and lets nodes doing similar preservation work find each other. Audience spans both tribal leadership/councils and general community members. Uses recursive/fractal ENDCAP wrapping — each cultural knowledge "track" is its own self-describing, AGP-scoped unit that can move between servitors without losing its access scoping. A "cultural preservation servitor" (Estuary-style organic-discovery local guide AI) has been proposed on a Qwen2.5 baseline.

### Council Chamber / Multi-Agent Squad Experiment
Active local multi-agent experiment using `qwen2.5-coder:1.5b` via Ollama in Termux on the Tab S9+. Structured per-role agent squad with dual-format logging (plain text + JSONL), signal-trap interrupt handling, and resumable run scripts. Council Chamber v3 is a FastAPI + Ollama + code-server group-chat backend (FastAPI on port 8080, code-server on 8081). Recent work included resolving Ollama binding/process-management issues (`0.0.0.0:11434`, `termux-wake-lock` vs. `nohup`).

### Live Broadcast Design Decision
PTT/live-broadcast-style channels (e.g. cultural talks, storytelling) default to open-air transmit, not gated by AGP/encryption. Archiving to ENDCAP is opt-in per broadcast at the sender's discretion, since the network can't stop independent recording by receivers regardless.

## 8. Standalone Tools Built (Outside Core HiveNet)

- **FRAMESTACK** — browser-based GIF/slideshow builder (v2 uses `omggif` for proper animated-GIF frame decoding; v3 still a future milestone)
- **Salish language learning app** — conversational, scene-based, self-contained HTML
- Pose-reference 3D tool and a custom dice game (standalone HTML)
- **WhipPlait** — 3D multi-layer whip pattern creator (v1 React component delivered)

## 9. Project History / Lessons Learned

- OmniVoice originally existed as a separate networking/coordination layer, later dissolved and folded into the core architecture
- 30 pages of handwritten project notes were lost — committed docs and conversation history are now the only surviving record (a strong argument for the compiled single-source doc below)
- A local model once hallucinated its own identity (called itself "duer-cli") — flagged as useful adversarial test data for Dragon Radar
- Project was briefly considered for renaming to "Skynet" due to a name conflict with Hive Computing Services SA
- Development approach relies on multi-AI collaboration, with Claude as a primary technical/strategic partner, leaning on strong systems intuition and cross-domain pattern recognition to offset still-developing formal coding skills

---

## On Compiling the Repo Into a Single Document

I can't pull `github.com/drizzlej38-ui/hivenet-docs` directly (no network access in this environment), so I can't merge the actual files myself right now. Two ways to get there:

1. **You paste or upload the individual spec files here** (ARCHITECTURE.md, ENDCAP, AGP_FEDERATION, NODE_CLASSES, SRM, DRAGON_RADAR, FOUNDING_PRINCIPLES, GLOSSARY, the newer drafts) and I merge them into one canonical document with consistent headers, resolve any contradictions between docs, and flag anything that's drifted out of sync — this summary above gives a suggested table of contents/ordering to merge them into.
2. **You keep this summary as the master index** and I help you write a short "canonical" front-matter section for the real merged doc (status: built vs. drafted vs. proposed-and-shelved) so anyone picking up the repo — including future-you — can tell settled architecture from in-progress ideas like ASH or Sovereign Cloud at a glance.

Given how much has already drifted (OmniVoice folding in, the Skynet rename scare, 30 pages of notes lost), a single versioned source of truth is a good instinct regardless of which path you take.
