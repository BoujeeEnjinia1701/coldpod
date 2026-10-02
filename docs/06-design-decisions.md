---
doc_id: CPD-DEC-001
title: ColdPod design decisions register
project: ColdPod
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, the decision records and the build plan work
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for open decisions 1 to 7 (2026-10-02); moved to decisions made (CPD-DDR-003 accepted)"
---

# ColdPod design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The VIP maker can supply the seven panels to plus 0, minus 1 mm, with a quote and aged conductivity and edge data | The panels fill the shell exactly; joints and edges are about 45 % of the heat leak | CPD-DDR-003; CPD-CAL-001 |
| 2 | The gasket still seals with the lid tray landed on the can flange, and the tray seat gives about 0.5 K/W | Lid seal and lid-pack refreeze both rest on it | CPD-DDR-002; CPD-CAL-001 |
| 3 | The PCM maker can supply the eight pouch shapes, and the usable latent heat between 2 and 8 °C | Pouch fit round the risers and feet; hold times | CPD-DDR-003; CPD-CAL-001 |
| 4 | The bought handle's pivot eyes take M5 screws and clear the 4 mm pads | Handle pivot pads | CPD-DDR-003 |
| 5 | The off-state conductance and real COP of the chosen module with the chosen heat sink and fan | Hold power and the thermosiphon diode ratio | CPD-PRC-001 |
| 6 | The Peltier driver can run the module from a 10 V input | R7 at the low end of the vehicle range | CPD-DDR-002 |
| 7 | Whether a motorbike carrier stays within about 19° of tilt with the cooling head down; if not, the mechanical disconnect fallback | The loop thermosiphon works only below that tilt | CPD-DDR-001, D2; CPD-CAL-001, H5 |

## Value engineering

Value-engineering target: USD 310 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 308 (USD 2 under the target).

- **Main cost drivers:** the vacuum-insulated panel set (about USD 60, still an estimate until quoted), the thermosiphon loop (about USD 28), the buck-boost Peltier driver (USD 22 to 26), the lid cold plate tray (USD 13) and the liner cut-out (USD 10 to 13).
- **Savings worth trying:** a VIP quote before any purchase; thinner printed parts, which already saved about USD 4 of filament; and re-pricing the driver and thermosiphon parts at purchase.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D11: 5 °C organic PCM, thermosiphon with a mechanical disconnect as fallback, evaporator on the outer face of the PCM, 76.8 Wh LiFePO4 pack, R6 redefined to 16 h, R12 relaxed to 5.5 kg, VIPs with a foam variant documented, local alarms and Bluetooth only, alarm defaults, budget $300, outreach vaccinators first | Amish, going with the recommendation | CPD-DDR-001 |
| 2026-09-25 | TRL 3 recommendations: lid cold plate, 3 °C liner cut-out, thinner printed parts, evaporator can and loop thermosiphon, TEC1-12703 class with smooth DC, buck-boost driver, budget kept at $300 | Amish: "i accept all your recommendations, go with them across all repos." | CPD-DDR-002 |
| 2026-09-26 | Budget top-up to $310 (R15 met) | Amish: "I am ok with the budget top ups" | CPD-DDR-002, N3 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The changes themselves were accepted on 2026-10-02 (below) | CPD-DDR-003 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P12 (pads and towers on the shell, rim slots, foam strip, loop in the can corner, block frame, liner feet and collar, folded lid tray, fixings, drip tray, cable duct) and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | CPD-DDR-003, A1 |
| 2026-10-02 | Mass (R12): option (a). R12 relaxed to 5.75 kg for the prototype, which is weighed at TRL 4; the base bumper is left off so the 0.05 kg margin is not spent before weighing | Amish: "i approve your recommendations for all 555 open decisions." | CPD-DDR-003, A2; CPD-DDR-002, N2 |
| 2026-10-02 | Refreeze (R8): option (a). R8 restated as 9 h or less for all the PCM at 25 °C, still an overnight refreeze | Amish: "i approve your recommendations for all 555 open decisions." | CPD-DDR-002, N1; CPD-CAL-001 v0.4, G4 |
| 2026-10-02 | Battery removal (R14): option (a) for the prototype; the battery bay on four screws counts as removable. Before any field or air travel use, add the shipping switch and check the carrier's lithium battery rules | Amish: "i approve your recommendations for all 555 open decisions." | CPD-DDR-003, A3 |
| 2026-10-02 | Loop working fluid: R-134a (non-flammable, safety class A1) for the prototype, with the charge set by the refrigeration technician from the loop volume; a lower-impact fluid such as R-1234yf (A2L, mildly flammable) is revisited only for a product version and under local rules | Amish: "i approve your recommendations for all 555 open decisions." | CPD-DDR-003, A4 |
| 2026-10-02 | Co-design partner: an immunization program, consistent with outreach vaccinators first (CPD-DDR-001, D11). First candidate to approach: PATH, or a national immunization program's outreach team reached through it | Amish: "i approve your recommendations for all 555 open decisions." | CPD-DDR-001, O1 |
| 2026-10-02 | Appearance model: round bail in the model; heat sink kept solid (no window); second status light adopted; labels and wordmark under BOM line 16; base bumper left out until the prototype is weighed | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26 |
