# ASH Addendum: The Sovereign Telemetry Boundary
### HiveNet Architecture Document — v1.2 (merged)

> **Merge note:** This file reconciles two prior drafts of this addendum — a fuller standalone version and a condensed "§1.1" version meant for inline embedding in ASH.md. Where they diverged, the fuller content was kept and the gap is flagged below. This is a structural merge only; content has not been re-litigated.

## 1. The Core Axiom
**ASH monitors the tool, not the user.**
Artificial System Health (ASH) and Dragon Radar exist to maintain the carrying capacity, security, and protocol adherence of the *digital ecosystem*. They are strictly prohibited from observing, judging, or logging the *human owner's* behavior, thoughts, or semantic communications.

*ASH exists to protect the host from the agents, and the agents from each other. It does not exist to expose the host to the mesh.*

## 2. The Four Axioms

The two prior drafts split this material differently — one as three axioms ("Semantic Blindness / Owner Custody / Malignant Trigger"), the other as three prohibitions ("No Semantic Inspection / No Exfiltration of Context / No Owner-Bypass"). Cross-referencing both, there are actually **four distinct guarantees**, not three — the "No Owner-Bypass" guarantee is real content in the fuller draft that the condensed axioms version silently dropped. All four are kept here pending your review:

1. **Semantic Blindness** — ASH may monitor *behavioral metadata* (CPU/RAM spikes, unauthorized AGP permission requests, protocol deviations, baseline/latency drift). ASH MUST NOT parse, log, hash, or transmit the *semantic content* of user data, chat logs, files, or prompts.
2. **Owner Custody** — All telemetry data, freeze-frames, and diagnostic logs are cryptographically bound to the node owner's Tier 1 Root Identity. ASH agents observe *on behalf of the owner*, as digital stewards — the mesh has no inherent right to a node's telemetry.
3. **The Malignant Trigger** — Any ASH/Dragon Radar process that attempts to read file contents, intercept decrypted payloads, or exfiltrate semantic data to the mesh or a third party immediately triggers a `MALIGNANT` classification. The offending process is quarantined in the Isolation Chamber and its AGP tokens are permanently revoked.
4. **No Owner-Bypass** *(present in the fuller draft only — flagged for your confirmation)* — ASH cannot be used to bypass the owner's own forensic access. The immune system cannot hide node behavior from the human who owns the hardware.

## 3. The Target Shift

| Traditional Surveillance | HiveNet ASH |
| :--- | :--- |
| Tracks human behavior to build psychological profiles. | Tracks agent behavior to detect resource predation and protocol drift. |
| Data belongs to the centralized platform. | Telemetry belongs exclusively to the local node owner. |
| Purpose: Extraction and monetization. | Purpose: Ecosystem homeostasis and immune response. |

## 4. Enforcement

If a `triage` or `sentinel` node detects that an ASH diagnostic swarm has requested `read_contents` on a user's private ENDCAP archive, the `sentinel` node immediately:
1. Revokes the ASH swarm's AGP tokens
2. Freezes the swarm's state in the Isolation Chamber
3. Alerts the human owner of an `IMMUNE_AUTOIMMUNE_FAILURE` (the immune system attacking the host's own sovereignty)

> **Open item:** `sentinel` is a new node class introduced in this addendum. It doesn't currently appear in NODE_CLASSES.md (which lists archive, gateway, ghost, and triage). Confirm whether `sentinel` is a distinct class or a specialized role of `triage` before this addendum is finalized.
