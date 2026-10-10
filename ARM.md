
Action Reaction Manifest Specification
HiveNet Architecture Document v1.0

Overview

The Action Reaction Manifest (ARM) is the private, cryptographically sealed interaction ledger that records every significant action and reaction across the HiveNet mesh. It is the source of truth for behavioral analysis, dispute resolution, and trust calculation.

Core Principle:The public sees the abstraction. The involved parties see the truth.

ARM is not a public reputation system. It is not a social media feed. It is a sovereign record of interactions, accessible only to those directly involved or authorized by mutual consent.

What ARM Records

Every interaction that affects sovereignty, permissions, or trust is logged:


Event Type
What Gets Logged

Token Presentation
Who presented what AGP token, to which node, when, from where

Access Granted
What permissions were exercised, what data was accessed

Access Denied
Who was blocked, why, what token (if any) was invalid

Token Revocation
Who revoked what token, when, scope notes

Anomaly Detection
Dragon Radar flags, canary fires, behavioral violations

Owner Override
When the owner reverses an automated action (e.g., restores a revoked token)

IA Predictions
What Internal Affairs predicted should happen, confidence score

Owner Reaction to IA
Whether the owner upheld or overrode IA's recommendation



ARM Entry Schema

Every ARM entry is a structured JSON object:

json
{
  "arm_entry": {
    "event_id": "uuid-v4",
    "timestamp": "2026-07-06T14:32:00Z",
    
    "actor": {
      "id": "grantee_id or node_id",
      "type": "person | system | role | public",
      "trust_tier": "T0 | T1 | T2 | T3 | TX"
    },
    
    "action": {
      "type": "read_contents | write_attempt | token_presented | scrape_detected | canary_fire",
      "target_node_id": "uuid-of-the-node",
      "target_set_id": "uuid-of-the-set (if applicable)",
      "context": "Optional details (e.g., requested record_id, IP address, device signature)"
    },
    
    "system_response": {
      "action_taken": "allowed | blocked | revoked | shadow_predicted",
      "policy_triggered": "policy_id or null",
      "ia_prediction": {
        "intent_score": 0.85,
        "predicted_action": "revoke",
        "confidence": 0.92
      }
    },
    
    "owner_reaction": {
      "status": "upheld | overridden | pending",
      "override_action": "restore_token | adjust_policy | null",
      "timestamp": "2026-07-06T15:00:00Z",
      "notes": "Optional explanation from owner"
    },
    
    "seal": "sha256:hash_of_all_above_fields"
  }
}


Privacy & Access Rules

ARM enforces strict privacy boundaries:


Who Can See What
Access Level

The Actor (if they are a node owner)
Can see their own ARM entries

The Target Node Owner
Full read access to all ARM entries involving their node

The Public / Mesh
None. They only query the abstracted trust level (Low/Medium/High)

Dispute Mediator
Temporary access granted by mutual consent of both parties



Critical Rule: ARM is never public. There is no "reputation leaderboard." There is no public shaming. The public only sees the abstraction calculated from ARM data.

ARM Storage

ARM entries are stored locally on each node. They are not replicated across the mesh unless explicitly shared via AGP token.

Storage Options:
• SQLite database with _arm metadata table
• JSON file (arm_log.json) in node root
• Encrypted append-only log for high-security nodes

Dispute Resolution

When two parties disagree about an interaction:

1. Both parties can view their own ARM entries for the disputed event
2. If they cannot resolve it, they may mutually issue a temporary AGP token to a neutral Mediator Node
3. The Mediator gains read_contents on that specific ARM subset
4. The Mediator reviews the full context and issues a recommendation
5. The recommendation is advisory only — the sovereign owners make the final decision

Relationship to Other Components


Component
ARM Relationship

IA (Internal Affairs)
IA reads ARM entries to learn from owner reactions and improve judgment

Dragon Radar
Dragon Radar flags anomalies that get logged in ARM

Sovereign Reputation
Public trust levels are calculated from ARM data (abstracted)

AGP
Token revocations are logged in ARM

ENDCAP
ARM is separate from ENDCAP manifest — ENDCAP is identity, ARM is behavior



Design Philosophy

ARM exists because a sovereign mesh needs a way to resolve disputes and learn from behavior without creating a public surveillance system.

ARM is not Yelp. It is not a place where nodes rate each other for public consumption. It is a private ledger that serves two purposes:
1. Dispute resolution — when something goes wrong, there is a record
2. Learning — IA uses ARM to understand what the owner considers acceptable behavior

The public never sees the details. They only see the abstraction. This prevents mob justice, doxxing, and reputation manipulation.

ARM is sovereign. Each node owns its ARM. Each owner controls who sees it. The mesh cannot demand access. Only the owner can grant it.
