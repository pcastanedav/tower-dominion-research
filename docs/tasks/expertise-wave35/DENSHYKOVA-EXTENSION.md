# Denshykova / Lions statue — Wave 35 D7 experiment extension

Status: design assumptions confirmed; mechanical validation required before interpreting new simulated odds.

## Fixed user assumptions (2026-10-17)
- Denshykova's commander effect is active throughout the run, beginning Wave 1.
- Lions (red) statue is activated at Wave 5, conservatively before the Wave-10 target construction floor.
- Statue curates the Tier-1 ordinary-Doctrine pool; model its actual curation effect, **not** a generic Doctrine multiplier.
- Denshykova **does not start with the specialized Super Weapon Blueprint**. Acquire target Blueprint through the normal simulated reward process.
- Target is Lions CB14; objective is D7 by Wave 35, unlocked by either D3 or D6.
- Retain six existing competing-family schedules, amplifier-first acquisition and saved-before-build behavior, observational-only Attenuator tracking, and Wave-10 earliest construction.

## Primary comparison
Three commander treatments (baseline, Eleonor, Denshykova) x six family schedules x 1,000 paired seed IDs = 18,000 natural-Blueprint runs. Apply the same Wave-5 statue effect to all Lions treatments to isolate commander differences. Keep the previous guaranteed-Blueprint experiment as a diagnostic control, not as a substitute for natural Blueprint acquisition.

## Research lineage: building-Doctrine family experiments before Mission Control
The primary basis for this extension is the earlier Doctrine-family research in `docs/MECHANICS.md` sections 4–9, `docs/STRATEGY.md` (Pool engineering; Concentrate, progress, diversify), and `model/reinforcement_model.py` / `model/test_model.py`. This predates and is conceptually independent of the later Mission Control acquisition studies. Mission Control work supplies only later-verified Blueprint/commander or reinforcement refinements where relevant.

Earlier Doctrine-family findings: the default building-Doctrine multiplier is 3; a newly placed family exposes D1 and D4, each initially worth 3 tickets (6 combined); D7 unlocks after D3 OR D6; unrelated families dilute target progression, while delayed placement can improve D7 odds. `docs/STRATEGY.md` reports earlier stateful 5,000-run Lions results: isolated target D7 by Wave 35 69.38%, versus 30.10% with five early competing families. Those runs have different assumptions and are **not** directly comparable to the Wave-35 specialized-Blueprint pilot.

`model/test_model.py` explicitly tests a Denshikova-style multiplier of 12 versus baseline 3 and its additional pool competition. `docs/MECHANICS.md` section 8 establishes global TB multiplier arithmetic and the distinction from targeted weight modifiers. Neither establishes that Denshykova's live commander ability is permanently 12×; that must still be traced. `docs/OPEN_QUESTIONS.md` separately flags Denshikova / The Stars Call first-upgrade effect ownership and timing. The Lions statue's Tier-1 curation must be verified independently and applied from the assumed Wave 5; do not conflate statue curation with global TB multiplier changes.

## Required mechanical validation
1. Identify the exact statue entity, first upgrade, and how Tier-1 curation works (which Doctrines are removed, how many, selection policy, and whether Amplifier/Attenuator are eligible for removal).
2. Verify Denshykova's exact current modifier and whether the existing `tb_mult=12` representation correctly describes it, including its scope and stacking with other Doctrine weight modifiers. Existing model tests use 12 versus baseline 3, but this is not sufficient source validation.
3. Verify whether Denshykova has any Blueprint-specific restrictions or acquisition effects; do not invent an initial specialized Blueprint.
4. Establish timing/order of statue curation on Wave 5 and persistence of its removals.

## Output
Report D7 completion by Wave 35, D7 unlock route, target Blueprint acquisition/build rate and timing, Amplifier offers/acquisition/assignment, Attenuator offers/acquisition and zero-offer runs, with Wilson 95% intervals. Compare matched scenarios; flag conditional model probabilities, not validated in-game odds.

## Execution gate
Do not silently substitute arbitrary Tier-1 removals or apply `tb_mult=12` as a verified live effect. Resolve the above from game assets/code or label explicit sensitivity variants before running the main 18,000-run comparison.
