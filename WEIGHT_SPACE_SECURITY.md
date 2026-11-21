# Weight-Space Security

This document is the concise architecture-facing baseline for model-artifact integrity in HiveNet.

## Principle
Model weights, checkpoints, adapters, quantized variants, and related artifacts are security-sensitive inputs. Weight-space programming research shows that direct parameter editing can introduce backdoors in controlled experiments. Consequently, artifact integrity and behavioral verification are required before trusted admission.

## Required controls (proposed; not yet implemented)
1. Keep untrusted artifacts in quarantine until owner-authorized review.
2. Record provenance, source/version, digests, signatures where available, transformations, custody, and approvals.
3. Treat hashes as byte-identity checks, not proof of safety.
4. Inspect artifacts and run independent behavioral tests in an isolated environment.
5. Never allow the model that edits an artifact to be its sole verifier.
6. Bind runtime-loaded files to the exact artifact digest that passed admission.
7. Detect post-admission changes; quarantine and preserve evidence.
8. Require explicit owner approval for admission, modification, replacement, and rollback.

## Threats
Backdoored contributions, malicious adapters/deltas, supply-chain substitution, unauthorized local modification, runtime substitution, sabotage, and false assurance from reputation or single-model audits.

## Source distinctions
- [OpenAI: Combatting adversarial distillation](https://openai.com/index/combatting-adversarial-distillation/) addresses capability extraction through outputs and protected reasoning. It is not a weight-space editing study.
- [Wang et al., arXiv:2611.17395](https://arxiv.org/abs/2611.17395) report LLM-driven backdoor insertion through direct weight editing in controlled experiments; GPT-6 Astra was the only tested editor reported to succeed across all three target architectures.
- [Goworek et al., arXiv:2611.21449](https://arxiv.org/abs/2611.21449) report small-network weight writing/reading and limited weight-only poisoned-model/adapter detection, with important limitations.

## Status
These are proposed requirements. They do not imply current implementation, complete detection, or proof of safety.
