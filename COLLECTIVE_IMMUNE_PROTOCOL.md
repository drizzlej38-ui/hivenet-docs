markdown
# Collective Immune Protocol (CIP)
### HiveNet Architecture Document v1.1

## 1. Overview
When a node encounters a novel threat, behavioral drift, or exploit, it must warn the mesh. However, sharing raw logs violates the Sovereign Telemetry Boundary. The Collective Immune Protocol (CIP) solves this by abstracting threats into **Behavioral Phenotypes**—cryptographically hashed structural signatures that warn other nodes of *how* an attack behaves, without revealing *what* was being attacked or *who* was involved.

**Biological Analogy:** The mesh shares antibodies, not surveillance tapes.

## 2. The Phenotype Record (JSON Schema)
When the local ASH Swarm (Pathology/Epidemiology) identifies a new threat, it generates a Phenotype Record. Notice that **zero semantic data** is included.

```json
{
  "phenotype_id": "uuid-v4",
  "timestamp": "2026-09-01T14:32:00Z",
  "origin_node_class": "archive",
  "threat_classification": "MALIGNANT | INFECTIOUS | LATENT",

<br>

  "behavioral_signature": {
    "description": "Rapid sequential AGP escalation followed by external routing attempt.",
    "sequence_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "trigger_pattern": [
      {"action": "request_agp", "target": "write", "delta_ms": 0},
      {"action": "request_agp", "target": "delegate", "delta_ms": 150},
      {"action": "open_socket", "target": "external_ip", "delta_ms": 300}
    ]
  },

<br>

  "recommended_quarantine": {
    "action": "throttle_and_isolate",
    "revoke_permissions": ["write", "delegate", "link_peers"],
    "duration_sec": 3600
  },

<br>

  "owner_signed": true,
  "signature": "ed25519_signature_of_the_above_json"
}
