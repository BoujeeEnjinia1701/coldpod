# Review note: ColdPod

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch run)

### What was done

- `docs/01-problem.md` (CPD-PRB-001 v0.2): the problem (heat and freeze damage, fixed cold life of passive carriers, separate monitoring, closed commercial products), users and context, constraints, out of scope and open questions, with sources linked inline.
- `docs/03-requirements.md` (CPD-REQ-001 v0.2): 17 measurable requirements (R1 to R17) with targets, planned verification and status against the concept estimates.
- `docs/02-concept.md` (CPD-PRC-001 v0.2): how it works, components table numbered to the BOM and exploded view, first-order numbers with stated assumptions, nine design choices with options and recommendations, safety section, open questions.
- `cad/src/concept_media.py`: massing model (shell, lid, handle, VIPs, PCM packs, liner and rack with insulin pens, thermosiphon, Peltier module, heat sink and fan, end housings, LiFePO4 pack, power board, logger, sensors, display) with a table top and phone for scale.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `cutaway.png`, `exploded.png` with BOM callouts, `flow.png` (heat flow, all values marked as estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 16 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line added before "## Problem"; problem, concept, key components and safety updated.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem lines still match the concept.
- `cad/src/model.py` (the scaffold placeholder) is unchanged; the parametric model is TRL 3 work.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Payload | about 1.2 L, about 24 insulin pens | R3 met |
| Overall heat leak | about 0.11 W/K (±30 %) | Drives every hold time |
| Passive hold, PCM only, 43 °C | about 12.7 h | R4 met, thin margin |
| Off-grid hold (battery then PCM), 32 °C | about 26 h | R5 met, thin margin |
| Off-grid hold (battery then PCM), 43 °C | about 16 h | R6 **not met** (24 h) |
| Power to hold on external supply, 43 °C | about 17 W | R7 met on estimate |
| PCM refreeze, 25 °C, empty | about 6 h | R8 met |
| Mass, empty | about 5.2 kg | R12 **not met** (5.0 kg) |
| Size | about 370 x 215 x 205 mm | R13 met |
| Battery | 76.8 Wh LiFePO4 | R14 met |
| Parts cost | about $280 | R15 **not met** ($250) |

Requirements not met: R6 (about 16 h against 24 h at 43 °C off-grid), R12 (about 5.2 kg against 5.0 kg) and R15 (about $280 against $250). R4 and R5 are met with thin margins that depend on the VIP heat-leak estimate. R16 (splash and drop) is unverified.

### Proposed, awaiting Amish

1. **PCM:** 5 °C organic PCM (recommended) rather than water ice or a 3 °C PCM, to prevent freezing.
2. **Cold path:** gravity thermosiphon as a one-way thermal link (recommended), with a mechanical disconnect as fallback, rather than bolting the Peltier to the liner.
3. **Evaporator position:** on the outer face of the PCM, not on the liner (recommended).
4. **Battery:** LiFePO4 4S1P, 76.8 Wh (recommended; airline-friendly), or 4S2P, 153.6 Wh (about $30 more, 0.6 kg heavier, about 20 h at 43 °C).
5. **R6 shortfall:** accept about 16 h at 43 °C and rely on vehicle or solar power for long hot trips (recommended); or a larger battery (about 20 h); or thicker VIPs and more PCM (reaches 24 h, but about 400 mm long and over 6 kg).
6. **R12 shortfall (mass):** relax the target to 5.5 kg (recommended, since the PCM and VIPs set most of the mass), or cut about 0.2 kg with thinner shell walls and a lighter liner.
7. **Insulation:** VIPs (recommended), with a polyurethane foam variant documented as a low-cost option (saves about $45, hold at 43 °C drops to about 7 h).
8. **Connectivity:** local alarms plus Bluetooth Low Energy only in the first build (recommended); cellular or LoRa later.
9. **Alarm defaults:** warn after 10 min outside 2 to 8 °C; alarm at once at 0 °C or lower on the payload probe; early freeze warning at 1 °C on the liner probe.
10. **Budget:** parts cost about $280 against `budget_usd: 250`. Options: raise to $300 (recommended); keep $250 with foam insulation; keep $250 with a 0.8 L liner. `project.yaml` is unchanged.
11. **First user and partner:** outreach vaccinators first (recommended; sets the 43 °C case), or travellers with insulin; partner to be chosen (immunization program, diabetes association or humanitarian logistics group).

The SwapCell 48 V pack is not proposed: at about 468 Wh and 2.8 kg it is far larger than this design needs.

### Safety concerns

- Not a medical device and not WHO-prequalified; every document, the README and the proposed box labelling say so, and must keep saying so.
- A stuck-on Peltier driver could freeze the payload. The concept relies on the 5 °C PCM between the cold path and the liner, a hardware cold-block cut-out and liner and payload alarms. This needs a fault analysis at TRL 3.
- LiFePO4 battery (76.8 Wh) in a hot environment: BMS, fuse, charge blocked outside 0 to 45 °C, separate vented bay.
- Paraffin PCM is combustible and can soften some plastics; sealed HDPE pouches, kept away from the battery bay.
- Heat sink may reach about 55 to 65 °C at 43 °C ambient; enclosed, with a guarded fan.
- A punctured VIP loses its insulation invisibly; the design proposes a service warning from rising Peltier duty.

### Recommended next step

Review this note and the media. If approved, run `/advance-trl3` to calculate the heat leak with real VIP data, check the thermosiphon at tilt and the Peltier's off-state conductance, run a freeze-fault analysis, and produce the parametric model and drawing sheet. Settle R6, R12, R15 and the budget first, since they may change the box size.
