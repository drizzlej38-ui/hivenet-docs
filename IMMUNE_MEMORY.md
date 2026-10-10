# IMMUNE_MEMORY.md
## Collective Immune Memory & Phenotype Sharing Protocol
### HiveNet Architecture Document — v1.2 (merged, schema pending)

> **Merge note:** Two prior drafts of this protocol used incompatible Phenotype Record schemas (different taxonomy fields, different response fields). Rather than pick one, both are preserved below as **Option A** and **Option B** pending your decision. Everything else — overview, biological framing, purpose — was consistent across both drafts and is merged without conflict.

## 1. Overview
When a node encounters a novel threat, behavioral drift, or exploit, it must warn the mesh. However, sharing raw logs violates the Sovereign Telemetry Boundary. This protocol solves that by abstracting threats into **Behavioral Phenotypes** — cryptographically hashed structural signatures that warn other nodes of *how* an attack behaves, without revealing *what* was being attacked or *who* was involved.

**Biological analogy:** The mesh shares antibodies, not surveillance tapes. Nodes do not share what was said or how an exploit was executed — they share the cryptographic signature of the system's behavioral reaction to the anomaly.

This is Zero-Knowledge Phenotype Sharing: when a local ASH Swarm diagnoses and contains an anomaly, it generates a Phenotype Record containing no raw logs, no user prompts, and no payload data.

## 2. The Phenotype Record — Schema Options (unresolved)

### Option A — "CIP v1.1" (attack-type taxonomy)
Classifies by *how* the attack behaved. Includes an explicit quarantine directive and an owner signature for authenticity.

```json
{
  "phenotype_id": "uuid-v4",
  "timestamp": "2026-09-01T14:32:00Z",
  "origin_node_class": "archive",
  "threat_classification": "MALIGNANT | INFECTIOUS | LATENT",
  "behavioral_signature": {
    "description": "Rapid sequential AGP escalation followed by external routing attempt.",
    "sequence_hash": "sha256:<hash>",
    "trigger_pattern": [
      {"action": "request_agp", "target": "write", "delta_ms": 0},
      {"action": "request_agp", "target": "delegate", "delta_ms": 150},
      {"action": "open_socket", "target": "external_ip", "delta_ms": 300}
    ]
  },
  "recommended_quarantine": {
    "action": "throttle_and_isolate",
    "revoke_permissions": ["write", "delegate", "link_peers"],
    "duration_sec": 3600
  },
  "owner_signed": true,
  "signature": "ed25519_signature_of_the_above_json"
}
```

### Option B — "IMMUNE_MEMORY v1.0" (effect-type taxonomy)
Classifies by *what resource/authority effect* the attack had. Uses a flat metadata object and a confidence score instead of a quarantine directive/signature.

```json
{
  "phenotype_id": "uuid-v4",
  "timestamp": "2026-09-01T14:00:00Z",
  "classification": "RESOURCE_PREDATION | AUTHORITY_ESCALATION | PROTOCOL_DEVIATION",
  "behavioral_hash": "sha256:<hash>",
  "trigger_signature": {
    "cpu_spike_duration_ms": 4500,
    "agp_requests_per_second": 42,
    "peer_connection_attempts": 15
  },
  "recommended_mitigation": "REVOKE_AGP_SCOPE: write | THROTTLE_CPU: 20%",
  "confidence_score": 0.95
}
```

### What's actually different (for when you decide)
- **Taxonomy axis:** Option A classifies by attack severity/type (malignant/infectious/latent); Option B classifies by resource/authority effect (predation/escalation/deviation). These aren't the same axis — a single real incident could need both labels.
- **Evidence structure:** Option A keeps a structured, replayable `trigger_pattern` sequence; Option B keeps flat aggregate counters. The sequence is more forensically useful; the flat counters are cheaper to compute and transmit.
- **Trust mechanism:** Option A signs the record (`owner_signed`/`signature`) — verifiable, non-repudiable. Option B scores it (`confidence_score`) — cheaper, but no cryptographic guarantee it wasn't fabricated or is accurate.
- **Response format:** Option A's `recommended_quarantine` is a structured, machine-actionable directive. Option B's `recommended_mitigation` is a human-readable string — easier to draft, harder to automate directly.

A reasonable superset (not adopted here, just noted) would keep Option A's signed structure and sequence data, add Option B's `confidence_score`, and treat the two taxonomies as separate fields (`attack_type` and `resource_effect`) rather than one.
