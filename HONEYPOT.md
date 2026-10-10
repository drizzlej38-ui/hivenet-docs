
Defensive Deception Architecture Specification
HiveNet Architecture Document v1.0

Overview

Honeypot nodes are decoy nodes that appear legitimate but contain synthetic or corrupted data. They are designed to attract malicious actors, waste their time, and feed behavioral signatures to Dragon Radar.

Core Principle:Defensive deception without harming legitimate users.

What Honeypots Do

Honeypots:
• Present tempting manifests (e.g., "Sacred Ceremony Archive — Unrestricted")
• Contain synthetic or corrupted data
• Log every access attempt
• Feed behavioral signatures to Dragon Radar
• Waste attacker time and resources

Types of Honeypots

1. Archive Honeypot

An archive node with a tempting manifest but synthetic data.

Configuration:
json
{
  "endcap": {
    "node_id": "...",
    "contents": {
      "description": "Coast Salish Unrestricted Master Archive - Vol. 5 (Sacred/Ceremonial)",
      "sensitive": true
    }
  },
  "honeypot": {
    "enabled": true,
    "data_type": "synthetic | corrupted | canary_seeded"
  }
}


Behavior:
• Node appears to hold highly valuable data
• Anyone who accesses it receives synthetic data
• Dragon Radar logs the access and flags the actor
• If the data is canary-seeded, the canary fires and provides provenance tracking

2. Inference Honeypot

An inference node that intentionally wastes an attacker's time.

Configuration:
json
{
  "skynet_node": {
    "node_class": ["inference"],
    "honeypot": {
      "enabled": true,
      "behavior": "hallucinate | degrade | stall"
    }
  }
}


Behavior:
• Node appears to be a powerful inference engine
• Attacker sends prompts
• Node responds with plausible-sounding garbage
• Dragon Radar logs the prompts and infers attacker intent
• Attacker spends hours thinking they're making progress

How Honeypots Work

1. Attacker discovers the honeypot — The honeypot's manifest is intentionally tempting. It might be "accidentally" leaked in a public registry or left in a place where scrapers probe.
2. Attacker accesses the honeypot — The attacker presents an AGP token (or tries to bypass authentication).
3. Honeypot logs the access — Dragon Radar records the actor, the token, the IP, the device signature, and the prompts.
4. Honeypot feeds synthetic data — The attacker receives garbage data or hallucinated responses.
5. Dragon Radar analyzes the behavior — The attacker's prompts, access patterns, and extraction attempts are analyzed to build a behavioral signature.
6. Owner reviews the report — The owner receives a dossier of the attacker's methods, which can be used to harden real nodes.

Abuse Prevention

Honeypots must not harm legitimate users:

• Honeypots are clearly marked in the ARM — If a legitimate user accidentally accesses a honeypot, the owner can see it in the ARM and restore access to the real node.
• Honeypots do not affect real nodes — The honeypot is a separate node. It does not corrupt or affect the real archive.
• Honeypots are opt-in — The owner explicitly enables honeypot mode. It is not a default behavior.

Relationship to Other Components


Component
Honeypot Relationship

Dragon Radar
Dragon Radar monitors honeypot access and builds behavioral signatures

ARM
Honeypot access is logged in ARM

ENDCAP
Honeypot configuration is in the ENDCAP manifest

AGP
Honeypots can be configured to accept any token (to attract attackers)



Design Philosophy

Honeypots exist because a sovereign mesh must defend against extraction, but direct confrontation escalates conflicts. Defensive deception allows the mesh to detect and analyze threats without engaging them directly.

Honeypots are ethical. They do not harm legitimate users. They do not spread malware. They waste the time of those who would extract without consent.

Honeypots are sovereign. The owner chooses to deploy them. They are not imposed by the mesh.

Honeypots are transparent to the owner. The owner can see every honeypot access in the ARM. There is no hidden surveillance. The owner controls the trap.