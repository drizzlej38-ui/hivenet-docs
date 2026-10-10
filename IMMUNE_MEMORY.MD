markdown
# IMMUNE_MEMORY.md
## Collective Immune Memory & Phenotype Sharing Protocol
### HiveNet Architecture Document v1.0

## 1. Overview
The Collective Immune Memory allows the HiveNet mesh to warn itself of new threats without leaking private data or creating a centralized library of exploits. It operates on the principle of **Zero-Knowledge Phenotype Sharing**. 

Nodes do not share *what* was said or *how* an exploit was executed. They share the cryptographic hash of the *system's behavioral reaction* to the anomaly.

## 2. The Phenotype Record
When a local ASH Swarm successfully diagnoses and contains an anomaly, it generates a Phenotype Record. This record contains no raw logs, no user prompts, and no payload data.

**Schema:**
```json
{
  "phenotype_id": "uuid-v4",
  "timestamp": "2026-09-01T14:00:00Z",
  "classification": "RESOURCE_PREDATION | AUTHORITY_ESCALATION | PROTOCOL_DEVIATION",
  "behavioral_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "trigger_signature": {
    "cpu_spike_duration_ms": 4500,
    "agp_requests_per_second": 42,
    "peer_connection_attempts": 15
  },
  "recommended_mitigation": "REVOKE_AGP_SCOPE: write | THROTTLE_CPU: 20%",
  "confidence_score": 0.95
}
