---
name: migration-review
description: Review a database migration for reversibility and lock risk before it ships.
---

# Migration Review

## Apply When
A change adds or alters a file under `migrations/`.

## Policy
- Every migration is reversible or documents why it cannot be.
- A migration that takes a table lock names the expected lock duration.
