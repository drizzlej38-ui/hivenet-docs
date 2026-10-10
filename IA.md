
Internal Affairs / Sovereign Auditor Specification
HiveNet Architecture Document v1.0

Overview

Internal Affairs (IA) is the specialized classifier that analyzes ARM logs and learns from the owner's reactions. It is the judgment layer of the HiveNet security stack.

Core Principle:IA does not start with authority. It earns it through alignment with the owner's judgment.

IA is not a chat model. It is not a general-purpose AI. It is a tiny, highly specialized anomaly-detection model trained only to read ARM logs and score intent.

What IA Does

IA performs three functions:

1. Intent Scoring — Analyzes ARM entries and assigns an intent score (0.0 = benign, 1.0 = malicious)
2. Action Prediction — Predicts what action should be taken (e.g., "revoke token," "allow access," "flag for review")
3. Learning from Owner Reactions — Adjusts its weights based on whether the owner upheld or overrode its predictions

Shadow Mode vs Active Mode

IA does not start with the ability to take automated action. It must earn trust.

Shadow Mode (The Default)

When IA is first deployed, it runs in Shadow Mode:

• IA watches the ARM stream
• It predicts what the system should do (e.g., "Intent score 0.85. Predicted action: Revoke token")
• It logs this prediction in the ARM under system_response.ia_prediction
• It does not execute the revocation. It just waits.

The owner reviews the ARM log later and sees IA's predictions.

The Owner Review (The Feedback Loop)

When the owner reviews the ARM log:

Scenario A: IA is right
• The owner agrees with IA's prediction
• The owner marks owner_reaction.status: "upheld"
• IA's confidence score goes up
• IA's internal weights are reinforced

Scenario B: IA is wrong
• The owner disagrees (e.g., "User X is my cousin, they were just clicking too fast")
• The owner marks owner_reaction.status: "overridden" and override_action: "restore_token"
• IA's confidence score goes down
• IA's internal weights adjust to learn the owner's specific tolerance

Active Mode (Earned Trust)

Once IA's confidence crosses a threshold (e.g., 90% alignment with the owner's reactions over 100 events), the owner can flip the switch to ia_mode: "active".

Now, when IA predicts "Revoke" with high confidence, SRM-Management actually executes it automatically.

The owner still reviews the ARM later, but the system is protecting itself in real-time.

The "Owner Friction" Metric (The Safety Brake)

How do we know IA has "good judgment"? We measure friction.

Friction = (Number of owner overrides) / (Total IA predictions)

• If friction > 20%, IA automatically downgrades itself back to Shadow Mode
• IA realizes: "My judgment does not match the Architect's judgment. I need to learn more before I act."
• This prevents the AI from becoming a tyrant. It enforces humility.

IA Architecture

IA is a specialized classifier, not a general-purpose model. It should be:

• Tiny — 10-50MB, runs on low-power devices
• Fast — Can score intent in <100ms
• Transparent — Its weights and decision logic are owner-accessible
• Local — Runs on the node, not in the cloud
• Auditable — Every prediction is logged in ARM

IA is not your local Qwen 1.5b. It is a separate, purpose-built model trained specifically for ARM analysis.

IA Schema

json
{
  "ia_config": {
    "mode": "shadow | active | disabled",
    "confidence_threshold": 0.90,
    "friction_threshold": 0.20,
    "learning_rate": 0.01,
    "model_path": "/path/to/ia_classifier.bin"
  },
  
  "ia_state": {
    "total_predictions": 147,
    "owner_upheld": 132,
    "owner_overridden": 15,
    "confidence": 0.898,
    "friction": 0.102,
    "last_updated": "2026-07-06T15:00:00Z"
  }
}


Relationship to Other Components


Component
IA Relationship

ARM
IA reads ARM entries to learn from behavior

Dragon Radar
Dragon Radar flags anomalies; IA scores intent

SRM-Management
SRM executes IA's recommendations (in Active Mode)

Owner
Owner reviews IA predictions and provides feedback



Design Philosophy

IA exists because an automated security system needs judgment, but judgment must be aligned with the owner's values, not imposed by a central authority.

IA is not a judge. It is a student. It learns what the owner considers acceptable by observing the owner's reactions. It earns the right to act by proving it understands the owner's judgment.

IA is not global. It does not learn a universal standard of "good" or "bad" behavior. It learns the specific preferences of one node's owner. What looks like a malicious scrape to one owner might look like a clumsy researcher to another. IA respects that sovereignty.

IA is humble. If it gets it wrong too often, it steps back. It does not insist. It does not argue. It learns.
