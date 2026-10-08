# Slice 1 — MC Chain Mechanics and Eligibility Inventory

Status: active. Started 2026-10-08.

## Objective
Locate game assets/code proving MC Blueprint identities and eligibility, upgrade 1A, post-Wave-40 choose-1-of-5 triggers and finite bounds, and category-specific reward behavior. Produce verified mechanics and explicit unresolved questions before model implementation.

## Starting evidence
- `docs/MECHANICS.md` §3: Blueprint weights T1=100, T2/T3 base start negative then clamp after modifiers; 32 normal bundle Blueprints (12/10/10). Blueprint acquisition does not remove ordinary Blueprint from future pool.
- §9: D1_45 / D2_42 provide Amplifiers; targeted Blueprint and building-Doctrine weight doubled; effect stacking additive at item-specific layer.
- §10: Tander has four cards of two items vs baseline three.
- §10: Eleanor F3H08S01 recurring Blueprint-only choose-1-of-3; F3H08S02 additive higher-tier effect needs exact trace.
- User: Red reinforcement Blueprint selection grants two copies (not more choices); mandatory first MC Amplifier; conditional second; immediate 1A; after Wave 40 two immediate choose-1-of-5 drafts; MC always picked when offered; MC hand+built indicates chain maturity.

## Open verification
- Locate MC family Blueprint IDs, rarity, availability, duplicate/quantity behavior and finite acquisition bounds.
- Identify chain draft producer, trigger timing, effect of 1A, recursion and pool exhaustion.
- Verify Red duplication scope and validity of faction/commander category combinations.
- Verify additive Eleanor arithmetic and special-draft selector.
- Clarify conditional second Amplifier policy and operational chain threshold after empirical behavior is known.

## Current state / next action
Plan and active report initialized. Inspect `maps/`, `isil/`, and game asset mappings; record precise symbol/file anchors and findings. No simulation results yet.
