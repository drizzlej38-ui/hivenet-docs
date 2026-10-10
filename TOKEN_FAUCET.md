
Automated Minting Policy Specification
HiveNet Architecture Document v1.0

Overview

The Token Faucet is a mechanism that allows nodes to automatically issue public AGP tokens without human oversight, within strict policy boundaries defined by the owner.

Core Principle:The owner sets the rules. The node executes them. Dragon Radar watches for abuse.

What the Token Faucet Does

The Token Faucet allows a node to:
• Automatically mint public, single-use, time-limited AGP tokens
• Distribute them via a web interface, QR code, or other mechanism
• Enforce policy constraints (max issuance, expiry, permissions, scope)
• Shut off automatically when the policy cap is reached

Use Cases

• Community flyers — A node holds a community event flyer. The owner sets a policy: "Mint up to 500 single-use, read-only tokens. Expire in 48 hours." The node hosts a web page where anyone can click "Download" and receive a token.
• Public domain zines — A poet releases their work. The faucet mints 1,000 tokens. Each reader gets one.
• Emergency alerts — A community node broadcasts an emergency map. The faucet ensures everyone can access it without manual token issuance.
• Coupons / Giveaways — A business node offers a promotion. The faucet distributes tokens automatically.

Minting Policy Schema

json
{
  "minting_policy": {
    "policy_id": "uuid-v4",
    "target_record_id": "uuid-of-the-record",
    "max_issuance": 500,
    "permissions": {
      "read_contents": true,
      "read_metadata": true,
      "write": false,
      "link_peers": false,
      "categorize": false,
      "delegate": false
    },
    "expires_in_seconds": 172800,
    "tokens_minted": 0,
    "tokens_consumed": 0,
    "active": true
  }
}


How It Works

1. Owner sets the policy — The owner defines the minting policy (max issuance, expiry, permissions, scope).
2. Node hosts the faucet — The node exposes a web interface, QR code, or other mechanism for requesting tokens.
3. Visitor requests a token — The visitor's HiveNet app (or web browser) requests a token from the faucet.
4. Node mints the token — The node checks the policy: 
◦ Has max_issuance been reached? If yes, faucet is closed.
◦ Is the policy active? If no, faucet is closed.
◦ If yes, mint a new AGP token with the specified permissions and expiry.
5. Visitor consumes the token — The visitor's app presents the token to access the record.
6. Token burns — The token is single-use. Once consumed, it cannot be reused.

Abuse Prevention

Dragon Radar monitors the faucet for abuse:


Threat
Defense

Bot scraping
Rate limit: 1 token per IP per minute. If a bot hits it 50 times, Dragon Radar flags the IP and temporarily blocks the faucet for that IP.

Token hoarding
Tokens are single-use and non-transferable. Once consumed, they burn.

Scope creep
The automated token is strictly scoped. It grants read_contents only for the specific record_id. It cannot be used to read the node's metadata or other records.

Exhaustion
The policy has a hard cap (max_issuance). Once reached, the faucet shuts off automatically.



Relationship to Other Components


Component
Faucet Relationship

AGP
Faucet mints AGP tokens

Dragon Radar
Dragon Radar monitors faucet for abuse

ENDCAP
Faucet is configured in the ENDCAP manifest

SRM
SRM enforces the minting policy



Design Philosophy

The Token Faucet exists because sovereignty does not mean isolation. Owners should be able to share freely without manual overhead, but within boundaries they control.

The faucet is sovereign. The owner sets the rules. The node executes them. No central authority can override the policy.

The faucet is constrained. It cannot mint beyond the policy cap. It cannot grant permissions beyond what the owner specified. It is a tool, not a loophole.

The faucet is monitored. Dragon Radar watches for abuse. If a bot tries to scrape 10,000 tokens, the faucet shuts down for that IP. Sovereignty includes the right to defend against extraction.
