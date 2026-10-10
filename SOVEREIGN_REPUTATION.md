
Sovereign Reputation System Specification
HiveNet Architecture Document v1.0

Overview

The Sovereign Reputation System is how trust propagates across the HiveNet mesh without creating a central authority or public shaming mechanism.

Core Principle:Trust is earned through behavior, not declared through credentials. The public sees the abstraction. The owner sees the truth.

Two Layers of Reputation

Layer 1: Private (Owner View)

The node owner has full access to:
• Exact trust point count
• Full ARM log (all actions and reactions)
• Detailed interaction history
• Who reacted, when, why

This is the source of truth. It is never public.

Layer 2: Public (Mesh View)

The public (other nodes, the Estuary registry, anyone querying the mesh) sees only:
• Abstracted trust level: Low | Medium | High | Trusted
• No details, no history, no specifics

This is the signal. It allows nodes to make routing decisions without exposing private behavioral data.

Trust Level Calculation

Trust levels are calculated from ARM data:


Trust Level
Criteria

Low
High negative ARM reactions, revoked tokens, anomaly flags

Medium
Mixed history, some positive interactions, some flags

High
Consistent positive behavior, zero or minimal flags

Trusted
Long history of clean behavior, vouched by T0/T1 nodes



The exact algorithm is owner-configurable. The public only sees the abstraction.

Trust Points

Trust points are a private metric. They go up or down based on interactions:

Gain points:
• Successful interactions (granted access, honored tokens)
• Positive reactions from other nodes (e.g., "grantee respected scope")
• Longevity (node exists and behaves well over time)
• Vouched by trusted nodes

Lose points:
• Token revocations (you misbehaved, they revoked)
• Detected anomalies (Dragon Radar flags you)
• Failed access attempts (you tried something you shouldn't)
• Negative reactions from other nodes

Privacy Protection

This system prevents:
• Mob justice — A stranger sees "Medium" and makes their own decision. They can't see why you're Medium.
• Doxxing — No public list of "bad actors." Only the owner knows the details.
• Discrimination — No one can discriminate based on details they can't see.

Integration with ENDCAP

Add a trust_level field to the ENDCAP manifest:

json
{
  "endcap": {
    "node_id": "...",
    "owner_id": "...",
    "trust_level": "high",
    "trust_points": 847,
    "contents": {...},
    "set_membership": [...]
  }
}


The trust_level is readable by anyone with read_metadata permission. The trust_points and detailed ARM are only accessible to the owner (or via a specific AGP token with elevated permissions).

Relationship to Other Components


Component
Reputation Relationship

ARM
ARM is the source of truth for reputation calculation

IA
IA learns from reputation patterns

Dragon Radar
Dragon Radar flags anomalies that affect reputation

AGP
Token revocations affect reputation

ENDCAP
Trust level is part of the ENDCAP manifest



Design Philosophy

The Sovereign Reputation System exists because trust must propagate in a decentralized mesh, but public reputation systems become tools for manipulation and abuse.

Reputation is sovereign. Each node owns its reputation. Each owner controls who sees what. The mesh cannot demand access to the details. Only the owner can grant it.

Reputation is abstracted. The public sees a signal, not a story. This prevents the reputation system from becoming a weapon.

Reputation is earned. You start with baseline trust. You earn more through consistent, sovereign behavior. You lose it through violations. There is no shortcut. There is no credential that grants trust. Only behavior matters.