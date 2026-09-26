---
doc_id: CPD-DDR-001
title: ColdPod TRL 2 review decisions
project: ColdPod
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); item O2 now decided, see CPD-DDR-002
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D11; item O2 accepted through CPD-DDR-002; item O1 remains proposed

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eleven items as "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. The one item without a recommendation stays open. TRL 4 work is on hold by the same instruction.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (TRL 2 session) and in CPD-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Phase-change material | 5 °C organic PCM (RT 5 HC class), rather than water ice or a 3 °C PCM, to prevent freezing. Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Cold path | Gravity thermosiphon as a one-way thermal link, with a mechanical disconnect as the fallback, rather than bolting the Peltier module to the liner. Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Evaporator position | On the outer face of the PCM, not on the liner. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Battery | LiFePO4 4S1P, 12.8 V 6 Ah (76.8 Wh), rather than 4S2P (153.6 Wh). Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | R6 shortfall | Accept about 16 h off-grid at 43 °C and rely on vehicle or solar power for long hot trips, rather than a larger battery or thicker insulation. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | R12 shortfall (mass) | Relax the empty-mass target to 5.5 kg, rather than cutting shell and liner mass. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Insulation | 25 mm vacuum-insulated panels, with a polyurethane foam version documented as a low-cost variant. Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | Connectivity | Local alarms plus Bluetooth Low Energy only in the first build; cellular or LoRa later. Decided by Amish, 2026-09-25: go with recommendation. |
| D9 | Alarm defaults | Warn after 10 min outside 2 to 8 °C; alarm at once at 0 °C or lower on the payload probe; early freeze warning at 1 °C on the liner probe; adjustable per product. Decided by Amish, 2026-09-25: go with recommendation. |
| D10 | Budget | Raise `budget_usd` from $250 to $300. Decided by Amish, 2026-09-25: go with recommendation. |
| D11 | First user | Outreach vaccinators first (sets the 43 °C design case), then travellers with insulin. Decided by Amish, 2026-09-25: go with recommendation. |

Notes on the decided items:

- **D5.** Requirement R6 in CPD-REQ-001 v0.3 is redefined from 24 h to 16 h or more at 43 °C off-grid, with longer hot trips run from external power under R7.
- **D6.** Requirement R12 in CPD-REQ-001 v0.3 is relaxed from 5.0 kg to 5.5 kg empty. The TRL 3 mass estimate is 5.60 kg (CPD-CAL-001, K2), so R12 is still not met; see `docs/REVIEW.md`.
- **D10.** `budget_usd` in `project.yaml` is now 300. R15 is redefined to $300. The TRL 3 BOM totals $295 (CPD-CAL-001, L2).
- **D2 and D3.** At TRL 3 the evaporator on the outer face of the PCM is sized as an aluminium can around the PCM jacket, fed by a two-phase loop thermosiphon (CPD-CAL-001, sections G and H). This sizes the decided choice; it is listed for confirmation in `docs/REVIEW.md`.
- **SwapCell.** The TRL 2 review did not propose the SwapCell 48 V pack (about 468 Wh and 2.8 kg, far larger than ColdPod needs). The portfolio decisions of 2026-09-25 on the SwapCell interface (v0.3 items: wake without CAN, charge-while-discharging mode, latch vibration rating) and on pricing shared packs once therefore do not change the ColdPod design or BOM.
- **Pitch and problem lines.** The review recommended no change to the `pitch` or `problem` wording, so `project.yaml` keeps them.

*Table 2. Items left open by this record, and their state after CPD-DDR-002.*

| # | Item | State |
| --- | --- | --- |
| O1 | Co-design partner (an immunization program, a diabetes association or a humanitarian logistics group) | Proposed, awaiting Amish. No recommendation was made; the portfolio decision is to pick partners per area later |
| O2 | New TRL 3 proposals: lid pack cold path, liner freeze cut-out, mass, evaporator can and loop thermosiphon, Peltier class and drive, vehicle input headroom, budget margin | Decided by Amish, 2026-09-25: go with recommendation. Recorded item by item, with what changed in the repo, in CPD-DDR-002 (`0002-recommendations-accepted.md`). The thermosiphon tilt limit carried no separate recommendation; it stays a test question for after TRL 3 |

## Consequences

- CPD-PRB-001, CPD-PRC-001 and CPD-REQ-001 are revised to v0.3 to show the decisions: design choices 1 to 9 of the precis are no longer "proposed", R6, R12 and R15 carry the new targets, and the first user is named.
- `project.yaml` carries `budget_usd: 300`.
- The partner question (O1) stays open in CPD-PRB-001.
