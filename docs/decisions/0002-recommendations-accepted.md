---
doc_id: CPD-DDR-002
title: ColdPod recommendations accepted
project: ColdPod
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all recommendations in CPD-DDR-001 and docs/REVIEW.md, what changed in the repo, and the items still open
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up to $310 decided by Amish (N3); R15 met
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item with a recommendation is decided by Amish; the item without a recommendation, and three new findings from the recalculation, stay open.

## Context

CPD-DDR-001 decided the eleven TRL 2 review items (D1 to D11) and left two groups open: O1, the co-design partner, with no recommendation, and O2, the new proposals from the TRL 3 session of `docs/REVIEW.md` (items 2 to 8 in its list "Proposed, awaiting Amish"), each of which carried a recommendation. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is therefore **decided by Amish, 2026-09-25: go with recommendation**. Where a recommendation offered several options, the recommended option is the decision. Items with no recommendation stay "Proposed, awaiting Amish". TRL 4 remains on hold by Amish's instruction, so decisions that need building, testing, weighing or purchasing are recorded but not carried out.

D1 to D11 in CPD-DDR-001 already read "Decided by Amish, 2026-09-25: go with recommendation" and are unchanged.

## Decision

*Table 1. Items decided by Amish on 2026-09-25 and what changed in the repo. Item numbers follow the TRL 3 session of `docs/REVIEW.md`.*

| # | Decision | What changed in the repo |
| --- | --- | --- |
| T2 | Lid pack cold path: option (a), a 1.5 mm aluminium plate under the lid PCM pack that seats on the evaporator can rim when the lid closes (about $5, 0.12 kg) | Plate added to `cad/src/model.py` (`lid_plate_t`, exported with the lid), BOM line 2 ($8 to $12), drawing CPD-DWG-001 Rev P2, media. CPD-CAL-001 v0.2: the lid pack now freezes through the plate and stays frozen near 2.8 °C in powered hold at 43 °C, so R1 and R7 move from at risk to met; hold times pooled (R4 13.0 to 14.0 h, R5 26.5 to 28.4 h, R6 16.5 to 17.5 h). Refreeze of all the PCM is now 8.4 h (jacket alone was 5.5 h), so R8 stays not met, for a new reason (see Table 2). Checking the gasket seal with the plate is a test on a built lid, on hold with TRL 4 |
| T3 | Freeze fault: a second hardware cut-out on the liner, opening at 3 °C, in series with the cold-block cut-out (about $3) | Cut-out added to the model and to BOM line 14 ($10 to $13); wiring named in BOM line 12. CPD-CAL-001 v0.2 section I: liner settles near 2.0 °C after a stuck-on fault (was about −4 °C); R2 moves from not met to met on paper; R2 target text in CPD-REQ-001 v0.4 names both cut-outs |
| T4 | Mass: option (a), thinner printed parts (shell 4 to 3 mm, lid cap 8 to 5 mm, end housings 3 to 2 mm) | `shell_t`, `lid_cap_t` and `end_wall` changed in `cad/src/model.py`; BOM lines 1 ($18 to $17) and 10 ($8 to $6); drawing notes. Mass 5.60 to 5.53 kg with the plate; R12 still not met, by 0.03 kg (the review estimated about 5.51 kg). Confirming by weighing is TRL 4, decided but on hold |
| T5 | Evaporator can and loop thermosiphon confirmed as sized (1.0 mm aluminium can, 8 mm copper loop), with the mechanical disconnect (D2 fallback) kept ready | Status wording in CPD-PRC-001 v0.4 and CPD-CAL-001 v0.2; no geometry change. Charging a loop is build work, on hold |
| T6 | Peltier class and drive confirmed: TEC1-12703 class, buck driver stage with LC filter for smooth DC, heat sink 0.50 K/W or better with the fan | Status wording only; already in the model and BOM lines 8, 9 and 12. The driver stage becomes buck-boost under T7 |
| T7 | Vehicle input headroom: option (a), a buck-boost Peltier driver | BOM line 12 ($22 to $26); R7 target text in CPD-REQ-001 v0.4 names the buck-boost driver for the 10 to 15 V input; CPD-CAL-001 v0.2 E9b. R7 met on paper |
| T8 | Budget margin: `budget_usd` stays at $300; get a VIP quote before any purchase decision | `project.yaml` unchanged at `budget_usd: 300`. Requesting supplier quotes belongs with purchasing, which is TRL 4 work: decided but on hold |

Other effects:

- **Budget.** `budget_usd` stays at 300 (T8). The BOM moves from $295 to $303 (plate +$5, liner cut-out +$3, buck-boost +$4, thinner prints −$3, lid cap filament −$1), so R15 moves from met to not met by $3. This is a finding, not a decision; see Table 2.
- **Pitch and problem.** No recommendation changed them; `project.yaml` and `README.md` keep the same lines.
- **Size.** The body is 2 mm shorter and narrower and 2.5 mm lower at the lid top; overall 366 x 212 x 207 mm (was 368 x 214 x 207 mm).
- **Controlled documents changed:** CPD-DDR-001 v0.2, CPD-PRB-001 v0.4, CPD-PRC-001 v0.4, CPD-REQ-001 v0.4, CPD-CAL-001 v0.2; drawing CPD-DWG-001 Rev P2.
- `trl` and `trl_target` stay at 3.

## Items still open

*Table 2. Proposed, awaiting Amish.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Co-design partner: an immunization program, a diabetes association or a humanitarian logistics group | Proposed, awaiting Amish. No recommendation was made; partners are picked per area later |
| N1 | R8 refreeze: 8.4 h for all the PCM against 8 h, now that the lid pack is frozen actively. Giving the module 30 W and the battery 7 W only reaches 8.2 h (CPD-CAL-001, G10). Options: (a) restate R8 as 9 h for all the PCM; (b) accept the miss; (c) a thinner lid pack, trading passive hold | New finding from CPD-CAL-001 v0.2. Proposed, awaiting Amish; suggestion (a) |
| N2 | R12 mass: 5.53 kg against 5.5 kg. Options: (a) keep the target and settle it by weighing when TRL 4 resumes; (b) relax to 5.6 kg; (c) a lighter strap and handle | New finding. Proposed, awaiting Amish; suggestion (a) |
| N3 | R15 cost: $303 against the $300 budget. Options: (a) raise `budget_usd` to $310; (b) keep $300 and wait for the VIP quote (on hold with TRL 4); (c) keep $300 and drop the buck-boost stage for an 11 to 15 V vehicle input (saves about $4, reopens R7) | New finding. Budget top-up to $310: decided by Amish, 2026-09-26. `budget_usd` set to 310; R15 met ($303 against $310, CPD-CAL-001 v0.3) |

## Budget top-up, 2026-09-26

Budget top-up to $310: decided by Amish, 2026-09-26 ("I am ok with the budget top ups"). This closes N3 with option (a). `project.yaml` now carries `budget_usd: 310`, R15 in CPD-REQ-001 v0.5 reads $310, and CPD-CAL-001 v0.3 rechecks the $303 BOM against it: met, with $7 of margin.

## Cross-repo actions

None. ColdPod shares no part or interface with another portfolio repo: it does not use the SwapCell pack (CPD-DDR-001), and no recommendation named another repo.

## Consequences

- Requirement status (CPD-CAL-001 v0.3, after the budget top-up): 2 not met (R8, R12, each by a small margin), 3 at risk (R4, R5, R6), 10 met, 2 not verifiable at TRL 3 (R10, R16). In v0.2, before the top-up, R15 was also not met. Before: 3 not met (R2, R8, R12), 5 at risk, 7 met, 2 not verifiable.
- The design has no remaining freeze path on paper and no lid pack that runs warm in long hot holds.
- TRL 4 work (weighing, gasket and plate seat checks, loop charging, VIP quotes and purchasing, climate chamber tests) stays on hold.
