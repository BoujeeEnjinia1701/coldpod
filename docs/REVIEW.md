# Review note: ColdPod

## Session 2026-09-26: sources strengthened

Amish asked on 2026-09-26 to "Fix the weaker sources" and approved the budget top-ups ("I am ok with the budget top ups"). Every link kept or added in the README sections Concept rationale, Burning platform, Where it could be used and What sparked the idea was fetched and checked against its claim.

| Where | Old source | New source |
| --- | --- | --- |
| Country row: Latin America, including the Amazon basin | None (claim of multi-day river outreach and distant freezers, uncited) | PAHO stories on river vaccination in Putumayo, Colombia (2024) and boat or plane access in Panama; the row now states only what they report |
| Country row: Sub-Saharan Africa | WHO PQS E004/VC01-VP2 test protocol page (could not be fetched for checking) | WHO PQS E004/VC01.2 vaccine carrier performance specification (cold life at a constant +43 °C) |
| Country row: United States | US FDA (kept; wording narrowed from "hurricanes, wildfires and power cuts" to natural disasters and other emergencies, which is what the page says) | Same |
| Burning platform: Hanson et al., 2017 | Kept; the wording "33 % of storage studies" was corrected to the review's pooled estimate of storage and shipments | Same |

What sparked the idea (vaccine vial monitor, PATH and an Ethiopian Federal Ministry of Health training module on OpenLearn Create) was checked and kept. docs/01-problem.md still uses the "storage studies" wording and the VC01-VP2 link, which are not weak sources and were left for a later pass.

**Budget:** `budget_usd` raised from 300 to 310 (CPD-DDR-002 N3, decided by Amish, 2026-09-26). `sizing.py` now reads the budget from a `BUDGET_USD` constant and was re-run: BOM $303 against $310, R15 met. Counts: 10 met, 3 at risk, 2 not met (R8, R12), 2 not verifiable. Controlled documents: CPD-CAL-001 v0.3, CPD-REQ-001 v0.5, CPD-PRC-001 v0.5, CPD-PRB-001 v0.5, CPD-DDR-002 v0.2; README budget figures updated.

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

## Session 2026-09-25: TRL 3

Amish's instruction for this session (2026-09-25): "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." ColdPod now claims TRL 3 (proof of concept on paper). TRL 4 is on hold by Amish's instruction.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CPD-DDR-001 v0.1): the eleven TRL 2 review items with a recommendation recorded as decided by Amish, 2026-09-25 (D1 to D11), and the items that stay open.
- `docs/04-calcs/01-sizing.md` (CPD-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: first-principles sizing with stated assumptions: payload and size; heat leak by Langmuir shape factors with explicit VIP joint, foam strip, pipe and wire paths; PCM energy; passive hold; a Peltier model for three module classes with cold and hot paths; powered hold and input power; battery-then-PCM hold with a ±30 % heat-leak band; a time-stepped refreeze model; thermosiphon diode ratio and tilt limits; a stuck-on driver fault; logger storage and reserve; mass from model volumes; BOM total; foam variant; options for review. The script imports the model's `PARAMS` and prints every number the note quotes, tagged [A1] to [P2].
- `cad/src/model.py`: parametric build123d model (shell, lid, handle, VIP set with foam strip, PCM jacket and lid pack, liner and rack with 24 pens, evaporator can with a loop thermosiphon and cold block, Peltier, heat sink and fan, end housings, cells, boards, sensors, display), exporting `cad/step/coldpod-assembly.step`, `shell.step`, `lid.step`, `vip-set.step`, `liner-rack.step`, `evaporator-thermosiphon.step`, `cooling-head.step`, `end-housings.step` and matching STL files in `cad/stl/`.
- `cad/src/sheets.py` and `cad/drawings/CPD-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, scale 1:5, with overall dimensions drawn from the model and a main-dimensions box. The sheet carries "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet stays CPD-DWG-010, so DWG-001 was the next free number.
- `bom/bom.csv` and `bom/bom-notes.md`: all 16 lines priced with a supplier type; total $295 against the new $300 budget.
- `cad/src/concept_media.py` now builds the media from `model.py` and takes its figures from the calc script; all media in `media/` were regenerated and checked by eye (a tangent tube that made the PCM solid invalid, and so missing from the cutaway, was fixed); temporary `media/_views*` folders were deleted.
- CPD-PRB-001, CPD-PRC-001 and CPD-REQ-001 revised to v0.3 (decisions recorded, numbers replaced by CPD-CAL-001, status column from the calc); `README.md` updated to TRL 3 with links; `project.yaml` set to `trl: 3`, `trl_target: 3`, `budget_usd: 300`, with the evidence files listed. PDFs are in `docs/pdf/`.

### Requirements (CPD-CAL-001, Table 9)

7 met, 5 at risk, 3 not met, 2 not verifiable at TRL 3. Hold times count as met only if they survive 30 % more heat leak than estimated.

| ID | Status | Value against target |
| --- | --- | --- |
| R2 | **Not met** | Normal operation met; with a stuck-on driver the liner can reach about −4 °C, because the only hardware cut-out is on the cold block at −5 °C |
| R8 | **Not met** | The jacket refreezes in 5.5 h (8 h target), but the lid PCM pack (0.28 kg) has no cold path to the evaporator |
| R12 | **Not met** | 5.60 kg against the relaxed 5.5 kg; the evaporator can adds 0.25 kg |
| R1 | At risk | Liner held at 2 to 5 °C, but in long powered holds at 43 °C the lid pack melts (after about 21 h) and settles near 13.8 °C above the top layer of pens |
| R4 | At risk | 13.0 h at 43 °C with no power; 10.0 h at +30 % leak (12 h target) |
| R5 | At risk | 26.5 h at 32 °C off-grid; 20.1 h at +30 % leak (24 h target) |
| R6 | At risk | 16.5 h at 43 °C off-grid; 12.4 h at +30 % leak (16 h target, redefined by D5) |
| R7 | At risk | 18.4 W input at 43 °C, inside the 45 W PD budget; lid pack melts after about 21 h; a 10 V vehicle input leaves little driver headroom for the 9.5 V module |
| R10 | Not verifiable at TRL 3 | Alarm logic is design intent only; no firmware sketch was written |
| R16 | Not verifiable at TRL 3 | Splash and drop need a test |
| R3, R9, R11, R13, R14, R15, R17 | Met | 1.36 L and 24 pens; 1.38 MB of 2.10 MB; about 96 days of logger reserve; 368 x 214 x 207 mm; 76.8 Wh; $295; labelling by design |

Other key numbers: overall conductance 0.091 W/K (0.11 at TRL 2), of which joints and edges are about 45 %; PCM 0.972 kg and 175 kJ (1.06 kg and 191 kJ at TRL 2, because the evaporator can and tubes take space); input to hold 4.2, 7.5 and 18.4 W at 25, 32 and 43 °C; the TEC1-12706 named at TRL 2 cannot hold at 43 °C at all (its off-state conduction is too high), so the TEC1-12703 class is used; on/off PWM would cost 61 % more power than smooth DC; thermosiphon forward to reverse ratio about 430, full function to 18° of tilt with the cooling head down; heat sink base about 53 °C at 43 °C; foam variant 7.4 h passive at 43 °C. Every TRL 2 number in the docs was checked against the script and corrected where it differed (CPD-CAL-001, Table 8).

### Decisions recorded (CPD-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: D1 5 °C organic PCM; D2 thermosiphon, mechanical disconnect as fallback; D3 evaporator on the outer face of the PCM; D4 76.8 Wh LiFePO4 4S1P; D5 accept about 16 h at 43 °C off-grid (R6 redefined to 16 h); D6 R12 relaxed to 5.5 kg; D7 VIPs, foam variant documented; D8 local alarms and Bluetooth Low Energy only; D9 alarm defaults; D10 `budget_usd` raised to $300 (set in `project.yaml`); D11 outreach vaccinators first. The pitch and problem lines were not asked to change and are unchanged. ColdPod does not use a SwapCell pack, so the SwapCell interface v0.3 items and the shared-pack pricing rule do not affect it.

### Proposed, awaiting Amish

Still open from TRL 2 (no recommendation was made):

1. Co-design partner: an immunization program, a diabetes association or a humanitarian logistics group (O1). Portfolio rule: partners are picked per area later.

New from TRL 3:

2. **Lid pack cold path (R8, R1, R7).** Options: (a) a 1.5 mm aluminium plate under the lid pack that seats on the evaporator can rim when the lid closes (about $5 and 0.12 kg; lid pack refreezes in about 2.3 h); (b) drop the lid pack and use a 20 mm jacket (1.010 kg of PCM, all actively frozen; body 10 mm longer and wider, 10 mm lower; the top of the cavity then sees the lid VIP directly); (c) keep the design and condition the lid pack in a refrigerator. Recommendation: (a), and check the gasket still seals with the plate in place.
3. **Freeze fault (R2).** Add a second hardware cut-out on the liner, opening at 3 °C, in series with the cold-block cut-out (about $3). The liner then settles near 2.0 °C after a stuck-on fault (1.2 °C for a 2 °C setting). Recommendation: adopt.
4. **Mass (R12).** Options: (a) thinner printed parts (3 mm shell, 5 mm lid cap, 2 mm housings), about 5.39 kg, or about 5.51 kg with the lid cold plate; (b) relax R12 again to 5.75 kg; (c) keep and accept the miss. Recommendation: (a), and confirm by weighing after TRL 3.
5. **Evaporator can and loop thermosiphon.** The decided D2 and D3 are sized as a 1.0 mm aluminium can around the jacket fed by an 8 mm copper loop; this is in the model and BOM line 7 ($28). Charging the loop needs refrigeration tools. Recommendation: confirm; keep the mechanical disconnect (D2 fallback) ready if a maker cannot charge the loop.
6. **Peltier class and drive.** TEC1-12703 class module with a buck driver and LC filter (smooth DC), and a heat sink of 0.50 K/W or better with the fan. In the model and BOM. Recommendation: confirm.
7. **Vehicle input headroom (R7).** At 10 V input the 9.5 V module drive leaves little margin. Options: (a) a buck-boost driver; (b) redefine the 12 V input range as 11 to 15 V. Recommendation: (a), if it fits the power board cost.
8. **Budget margin.** The BOM is $5 under the $300 budget, and the VIP set ($60) and thermosiphon ($28) are estimates. Recommendation: get a VIP quote before any purchase decision; `budget_usd` stays at $300.

### Safety concerns

- Not a medical device and not WHO-prequalified; every document, the README and the proposed box labelling say so.
- Freeze fault: with the present single cut-out on the cold block, a stuck-on driver can freeze the liner (R2 not met). Item 3 above fixes it on paper.
- LiFePO4 battery (76.8 Wh): BMS, fuse, charging blocked outside 0 to 45 °C, separate vented bay away from the heat sink.
- Paraffin PCM is combustible and can soften some plastics; sealed HDPE pouches, kept away from the battery bay.
- Heat sink base about 53 °C at 43 °C ambient; enclosed with a guarded fan.
- A punctured VIP loses its insulation invisibly; a rising Peltier duty should raise a service warning.
- The loop thermosiphon holds a working fluid under pressure; charging needs refrigeration tools and practice.
- Loaded mass about 6.3 kg; carry with the strap across the body.

### Other notes

- No existing TRL 4 material was found (`build-log/` holds only its README; `electronics/` and `firmware/` are empty). None was created. STANDARDS section 9 asks for a TRL change to be recorded in the build log; no build-log entry was written this session, since the brief did not name one.
- The TRL 2 review listed no unchecked citations, so no web verification was run. The sources in CPD-PRB-001 and CPD-REQ-001 are unchanged. BOM prices are indicative estimates by supplier type, not quotes.
- `.claude/commands/advance-trl3.md` names the drawing DWG-001; that number was free (the concept sheet is CPD-DWG-010), so the general arrangement is CPD-DWG-001.

### Recommended next step

Stay at TRL 3. TRL 4 is on hold by Amish's instruction. Decide items 2 to 8 above, starting with the lid pack cold path and the liner cut-out (they close R8 and R2), then revise the model, CPD-CAL-001 and the BOM on paper, and request quotes for the VIP set and the thermosiphon.

For reference only, TRL 4 would need: a lab test report (TST, `environment: lab`) on a built case or key subassemblies (heat leak by a steady-state heater test, passive and powered hold times in a climate chamber at 25, 32 and 43 °C, refreeze time, thermosiphon forward and reverse conductance and tilt limit, stuck-on driver fault test, alarm behavior, mass), build-log entries, and the purchasing and build work that goes with them. None of this has been started.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now **decided by Amish, 2026-09-25: go with recommendation**, recorded item by item in `docs/decisions/0002-recommendations-accepted.md` (CPD-DDR-002 v0.1). TRL 4 remains on hold; `trl` and `trl_target` stay at 3.

### Decisions applied and what changed

Items 2 to 8 of the TRL 3 list "Proposed, awaiting Amish" above (D1 to D11 in CPD-DDR-001 were already decided):

| Item | Decision | Change (before to after) |
| --- | --- | --- |
| 2 Lid pack cold path | (a) 1.5 mm aluminium lid cold plate seated on the can rim | Added to model, BOM line 2 ($8 to $12), drawing, media. Lid pack in powered hold at 43 °C: melted after about 21 h and settled near 13.8 °C, to held frozen near 2.8 °C. Passive hold at 43 °C: 13.0 to 14.0 h (jacket and lid pack now pooled). Off-grid: 26.5 to 28.4 h at 32 °C, 16.5 to 17.5 h at 43 °C. Refreeze: jacket only 5.5 h (lid pack could not be refrozen) to all PCM 8.4 h |
| 3 Freeze fault | Liner cut-out at 3 °C in series with the cold-block cut-out | Added to model and BOM line 14 ($10 to $13). Liner after a stuck-on fault: about −4 °C to about 2.0 °C |
| 4 Mass | (a) Shell 4 to 3 mm, lid cap 8 to 5 mm, housings 3 to 2 mm | Model and BOM lines 1 ($18 to $17) and 10 ($8 to $6). Empty mass 5.60 to 5.53 kg (with the plate). Weighing is TRL 4, on hold |
| 5 Evaporator can and loop | Confirmed as sized; mechanical disconnect kept as fallback | Wording only. Loop charging is build work, on hold |
| 6 Peltier class and drive | Confirmed: TEC1-12703 class, smooth DC, 0.50 K/W sink | Wording only |
| 7 Vehicle input headroom | (a) Buck-boost Peltier driver | BOM line 12 ($22 to $26); R7 target text names it. Input at 43 °C 18.4 to 18.5 W (thinner shell, taller lid stack) |
| 8 Budget margin | `budget_usd` stays at $300; VIP quote before any purchase | `project.yaml` unchanged. The quote request goes with purchasing, TRL 4, on hold |

Budget: `budget_usd` unchanged at 300. BOM total $295 to $303. Overall size 368 x 214 x 207 mm to 366 x 212 x 207 mm. Drawing CPD-DWG-001 Rev P1 to P2. Controlled documents: CPD-DDR-001 v0.2, CPD-PRB-001 v0.4, CPD-PRC-001 v0.4, CPD-REQ-001 v0.4, CPD-CAL-001 v0.2, new CPD-DDR-002 v0.1. All media, STEP and STL files, the drawing and every PDF were regenerated (the footers now read designmolecule.com); superseded PDFs that showed the old domain were deleted. The README gained the Concept rationale, Burning platform, Where it could be used and What sparked the idea sections; the idea's origin is the vaccine vial monitor (1996), which records heat but not freezing.

### Requirement status (CPD-CAL-001 v0.2)

| ID | Status | Value against target |
| --- | --- | --- |
| R8 | **Not met** | 8.4 h for all the PCM against 8 h (jacket 6.9 h, lid pack 8.4 h); 30 W to the module only reaches 8.2 h |
| R12 | **Not met** | 5.53 kg against 5.5 kg |
| R15 | **Not met** | $303 against $300 |
| R4 | At risk | 14.0 h at 43 °C; 10.8 h at +30 % leak (12 h) |
| R5 | At risk | 28.4 h at 32 °C; 22.3 h at +30 % leak (24 h) |
| R6 | At risk | 17.5 h at 43 °C; 13.2 h at +30 % leak (16 h) |
| R10, R16 | Not verifiable at TRL 3 | Firmware sketch and tests needed |
| R1, R2, R3, R7, R9, R11, R13, R14, R17 | Met | R1 and R7 were at risk and R2 was not met before this session |

Counts: 9 met, 3 at risk, 3 not met, 2 not verifiable (before: 7, 5, 3, 2).

### Still awaiting Amish

1. Co-design partner (CPD-DDR-001 O1). No recommendation was made.
2. R8 refreeze, 8.4 h against 8 h (CPD-DDR-002 N1). Options: restate R8 as 9 h for all the PCM (suggested); accept the miss; a thinner lid pack.
3. R12 mass, 5.53 kg against 5.5 kg (N2). Options: keep the target and settle it by weighing when TRL 4 resumes (suggested); relax to 5.6 kg; lighter strap and handle.
4. R15 cost, $303 against $300 (N3). **Decided by Amish, 2026-09-26:** budget top-up to $310. `budget_usd` is now 310 and R15 is met (see Session 2026-09-26 below).

### Cross-repo actions

None. ColdPod shares no part or interface with another repo and no recommendation named one.

### TRL 4

Remains on hold by Amish's instruction. Decided but on hold: weighing the case, checking the gasket seal and plate seat on a built lid, charging the loop thermosiphon, VIP and thermosiphon quotes and any purchasing, and all climate chamber tests. No build, test, PCB or firmware work was done.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose ColdPod on 2026-09-26 for the first batch of product renders. This session added an appearance model for photoreal renders; the render images themselves (`media/render-hero.png`, `media/render-exploded.png`) are produced later by the portfolio render pipeline.

### What was done

- `cad/src/product_model.py` (new): `product_parts()` returns 53 named parts (28 shell, 22 internal, 3 accessory, no context) with colour, material class, BOM line, group and exploded-view offset, plus `TITLE` and `RENDER_VIEWS` (hero from the front right, exploded from the front right, and a detail view of the battery bay and logger display from the front left). It imports `PARAMS`, `levels()` and `build_parts()` from `model.py` and keeps every main dimension and interface: 261 x 196 mm tub, 169.5 mm lid top, 207 mm to the top of the handle, 60 mm cooling head and 45 mm bay at 160 mm wide, pipe pass-throughs, cold block, Peltier, sink, fan, cells and boards where `model.py` puts them.
- Appearance detail added: 12 mm plan radius and filleted edges on the tub, lid and end housings; a black EPDM gasket line under the lid; a rubber base bumper; two teal draw latches on the front; a round steel bail with a ribbed rubber grip on pivot bosses; rounded grille, intake and vent slots; housing screws; a raised lid wordmark, lid range marking and a front label plate; a lit e-paper display with an illustrative readout, a lit green status light and a red alarm light; USB-C and 12 V inlets; a vented ambient sensor cap; fan blades; the internal stack split for the exploded view (VIP body set and lid plug, PCM jacket and lid pack, liner and rack, evaporator can, copper loop and cold block); and the padded shoulder strap as a fabric accessory.
- `README.md`: the hero image now points to `media/render-hero.png`, and the links line starts with the exploded render.
- Matplotlib self-check previews were made outside the repo; nothing in `media/` was changed.

### Differences from model.py (each Proposed, awaiting Amish)

1. **Handle form.** `model.py` has square 16 x 8 mm arms from Z = 128 mm and a 16 mm top bar. The appearance model uses a 10 mm round steel bail with 22 mm bends, pivot eyes at Z = 136 mm on 24 mm bosses, and a 16 mm ribbed rubber grip; the grip top stays at 207 mm. Recommendation: adopt the round bail in `model.py` at the next model revision; it matches the bought folding handle in BOM line 3.
2. **Window over the heat sink.** The appearance model has an 83 x 88 mm smoked window in the top of the cooling head so the fins show; `model.py` has a solid top. Options: (a) keep it as render styling only; (b) adopt it, with a check that it cannot be touched hot and does not change the airflow; (c) replace it with more exhaust slots. Recommendation: (a) for now, because it adds a part and a hot-surface question for no thermal benefit.
3. **Inlet positions.** USB-C and 12 V inlets are drawn low on the +X face of the cooling head, next to the power board; `model.py` does not place them. Recommendation: adopt this position (short leads to the power board, away from the battery bay).
4. **Latch positions and no hinge.** The two BOM line 2 draw latches are drawn on the front at X = ±72 mm, and the lid lifts off. Options: one latch front and one back, or a rear hinge. Recommendation: two front latches with a lift-off lid, as drawn, since a lid tether is simpler than a hinge through the VIP.
5. **Second status light.** `model.py` has one alarm light beside the display; the appearance model adds a red light at the mirrored position, matching the red and green LEDs already in BOM line 15. Recommendation: adopt.
6. **Base bumper, labels and wordmark.** A 12 mm rubber bumper around the base, a front label plate and a raised lid wordmark are not in the BOM. Recommendation: keep the labels under BOM line 16 and decide the bumper when the shell is next revised (it adds grams against R12, which is already 0.03 kg over).
7. **Shoulder strap anchors.** The strap is shown loose as an accessory; neither model places its anchor points. Recommendation: decide the anchors (handle pivots or end-housing lugs) with the next model revision.

### Scope

This is an appearance model only: no tolerances, no fabrication detail, and nothing past TRL 3. `trl` stays 3 in `project.yaml`, and TRL 4 remains on hold. `model.py`, the BOM and the controlled documents were not changed.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: kit 1.7.0, design made constructable, prototype build plan

Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with outstanding decisions kept out of the plan and in a separate register. Under his 2026-09-30 instruction ("If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations"), the design was made constructable. Every change is recorded in CPD-DDR-003 (Draft, open for his review). TRL stays 3; nothing was built or tested.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` matches `.kit/CLAUDE.md`.
- `cad/src/model.py`: rebuilt as 49 separate components (`build_components()`), grouped back into the 17 concept groups for the media, product model and calculations; 63 constructability checks (`python cad/src/model.py --check`), all pass. STEP and STL regenerated.
- `docs/decisions/0003-design-for-construction.md` (CPD-DDR-003 v0.1, Draft).
- `docs/05-build-plan.md` (CPD-BLD-001 v0.1): 17 component subsections, 20 assembly steps, first checks, nine safety stops.
- `docs/06-design-decisions.md` (CPD-DEC-001 v0.1): seven open decisions, seven items to confirm when parts are bought, four decisions made.
- `cad/src/build_plan_media.py`: overview, VIP panel picture, 15 making sketches (CPD-DWG-101 to 115), 9 joint close-ups, 20 step pictures and the wiring diagram.
- CPD-CAL-001 v0.4 (PCM volumes now measured on the model), CPD-REQ-001 v0.6, CPD-PRC-001 v0.6, `bom/bom.csv` (lines 1, 2, 4 to 7, 14, 16 changed; line 17 added), `bom/bom-notes.md`, CPD-DWG-001 Rev P4, concept media, README (links line and "Building the prototype"), `project.yaml` (`design_state: constructable`, both new documents in `trl_evidence`).

### Design changes made for construction (CPD-DDR-003)

1. Payload probe: a 10 x 40 mm vial across the top layer of pens; the old probe overlapped the pens by 2.35 cm³.
2. Loop: the evaporator ring bonded into the bottom inside corner of the can (it floated in the PCM); 25 mm corner bends.
3. Risers: 17.5 mm bends lying in the foam strip; can and shell slots open at the rim; three printed slot fillers; foam strip 20 to 28 mm tall.
4. Cold block: two tube sockets, a drilled condensing passage and a charge stub, brazed with aluminium-to-copper rod; the loop is charged on the bench as one sealed unit.
5. Peltier stack: a printed block frame screwed to two printed towers on the shell; two M3 clamp screws through the sink into the block; fan and guard on the sink.
6. End housings: printed pads with M3 inserts on both shell ends, ears on both housings.
7. Handle and latches: printed pads with M5 and M3 inserts; handle arms 4 mm further out (width 212 to 220 mm).
8. Liner and lid: 5 mm inward rim flange on the can; liner on four printed feet and a printed collar; the lid cold plate folded into a tray bonded to the lid VIP plug, landing on the flange.
9. VIPs: seven panels with order sizes; the lid plug 0.5 mm under the opening.
10. Electronics: power board and logger on standoffs, a printed cell cradle, the display under a window.
11. Condensate: a drip tray on the block frame and a drain tube through the head floor.
12. Cables and inlets: grommets and a cable slot at the cooling end, a printed cable duct cover on the back face, 12 V and USB-C inlets low on the head's end wall, a reed lid switch in the head.

### Key results (CPD-CAL-001 v0.4)

PCM 0.972 to 0.935 kg. Passive hold at 43 °C 14.0 to 13.3 h (R4 at risk); off-grid 27.3 h at 32 °C (R5 at risk) and 16.7 h at 43 °C (R6 at risk). Refreeze of all the PCM 8.4 to 8.0 h (8.03 h, R8 **not met** by a few minutes). Mass 5.53 to 5.70 kg (R12 **not met** by 0.20 kg). Size 366 x 220 x 207 mm (R13 met). BOM $303 to $308 against the $310 value-engineering target (R15 within the target). Counts unchanged: 10 met, 3 at risk, 2 not met, 2 not verifiable.

### Proposed, awaiting Amish

All in the design decisions register (CPD-DEC-001): accept CPD-DDR-003 (recommended); mass, now 0.20 kg over (recommend relaxing R12 to 5.75 kg); refreeze R8 (recommend restating as 9 h); battery removal for R14 (recommend counting the four-screw bay as removable for the prototype); the loop's working fluid (decide with the technician); the co-design partner; and the remaining appearance-model items.

### Safety concerns

The loop is a sealed refrigerant circuit: brazing and charging are for a qualified technician, before any plastic, VIP or PCM is near it (build plan S1, S2). No hot work once the paraffin is in (S8). A punctured VIP fails silently; the build plan bans tools near the panels (S3). The battery, first power and first charge stops (S4 to S7) carry over from the concept's safety section.

### Stale until regenerated on Amish's Mac

The photoreal renders (`media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept: no pads, towers, slots or duct, a flat lid plate and the handle 4 mm closer to the shell.

### Recommended next step

Amish reviews CPD-DDR-003 and the register. TRL 4 (building to the plan) stays on hold until he asks for it.

## Session 2026-10-02: open decisions decided

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This approves the recommendation written for every open decision in the design decisions register (CPD-DEC-001). trl stays 3; nothing was built, bought or tested, and TRL 4 remains on hold.

### Decisions recorded (7)

| Register item | Decision |
| --- | --- |
| 1 | CPD-DDR-003 accepted: P1 to P12 and their knock-on changes, as made |
| 2 | R12 relaxed to 5.75 kg for the prototype; weighed at TRL 4; base bumper left off |
| 3 | R8 restated as 9 h for all the PCM at 25 °C |
| 4 | Battery bay on four screws counts as removable for the prototype; shipping switch and carrier rules before any field or air travel use |
| 5 | R-134a (non-flammable, A1) for the prototype loop, charge set by the technician; R-1234yf only for a product version |
| 6 | Partner: an immunization program; first candidate to approach, PATH or a national program's outreach team through it |
| 7 | Round bail in the model, solid heat sink, second status light adopted, labels and wordmark under BOM line 16, no bumper until weighed |

All 7 moved to Decisions made in CPD-DEC-001, dated 2026-10-02; the Open decisions section now reads "None."

### Documents changed

- `docs/06-design-decisions.md` (CPD-DEC-001 v0.3): items 1 to 7 moved to Decisions made; Open decisions reads "None"; the 2026-09-30 row now points to the acceptance
- `docs/decisions/0003-design-for-construction.md` (CPD-DDR-003 v0.3): status accepted (kept Draft); A1 to A4 marked accepted; requirement consequence added
- `docs/03-requirements.md` (CPD-REQ-001 v0.8): R8 restated as 9 h, R12 relaxed to 5.75 kg (both met on paper), R14 status states the prototype removal method and the travel rule; counts updated
- `docs/04-calcs/01-sizing.md` (CPD-CAL-001 v0.6): R8, R12 and R14 text and Table 9 against the restated targets; counts 12 met, 3 at risk, 2 not verifiable
- `docs/02-concept.md` (CPD-PRC-001 v0.8): summary and results table against the new targets; refrigerant and battery removal safety notes; first partner candidate
- `docs/01-problem.md` (CPD-PRB-001 v0.6): partner type and first candidate to approach
- `docs/05-build-plan.md` (CPD-BLD-001 v0.2): section 2 says CPD-DDR-003 is accepted; R-134a named for the loop and in safety stop S2
- `bom/bom-notes.md`: CPD-DDR-003 accepted; R-134a for item 7; labels and wordmark under item 16
- `README.md`: R8 and R12 against the new targets
- `docs/decisions/0001-trl2-review-decisions.md` (CPD-DDR-001 v0.3): item O1 ("Proposed, awaiting Amish") recorded as decided
- `docs/decisions/0002-recommendations-accepted.md` (CPD-DDR-002 v0.3): items O1, N1 and N2 (awaiting Amish) recorded as decided
- PDFs regenerated with `python3 .kit/render.py`; superseded versions removed.

### Follow-up actions to carry approved decisions into the design

The model, BOM quantities and prices, calculations and pictures were not changed in this session. These actions carry the approved decisions into them:

1. Decision 2 and 3 (calculations): Re-run `docs/04-calcs/sizing.py` with R8 at 9 h and R12 at 5.75 kg so its R8, R12 lines, counts and `results.csv` match CPD-REQ-001 v0.8.
2. Decision 2 (test plan): Weigh the prototype at TRL 4 against 5.75 kg before any base bumper is added.
3. Decision 4 (model, BOM, build plan pictures): Before any field or air travel use, add the shipping switch to the battery bay: model, BOM line, wiring picture and build plan section; check the carrier's lithium battery rules.
4. Decision 5 (BOM): Name R-134a and its charge allowance in BOM line 7 (currently the charged loop without a named fluid) and price the charge with the technician.
5. Decision 6 (documents): Approach the first candidate partner (PATH, or a national immunization program's outreach team through it); nothing is agreed yet.
6. Decision 7 (model): Add the second (red) status light at the mirrored position beside the display in `cad/src/model.py`, matching the red and green LEDs of BOM line 1.
7. Decision 7 (pictures): Update `cad/src/product_model.py` and regenerate the photoreal renders, card and social preview on Amish's Mac: round bail, solid cooling head top (no window), second status light, labels and wordmark, no base bumper.

### Points found in the review

Raised when the recommendations were written (2026-10-01) and kept here so they are not lost:

- R14 is shown as 'Met: 76.8 Wh' in CPD-REQ-001 v0.6 while the battery removal question (CPD-DDR-003, A3; register item 4) is still open; the status should read 'met on paper, removal method awaiting Amish'.
- Item 3 options omit the power-split option in CPD-CAL-001 (G10): giving the module 30 W and the battery 7 W brings refreeze to 7.8 h, meeting R8, at the cost of an 11.5 h battery recharge.
- Item 6 lists a diabetes association and a humanitarian logistics group as equal options, but D11 already decided outreach vaccinators first; the options should be narrowed.
- Item 2's 5.75 kg limit leaves only 0.05 kg on estimated masses; if the bumper (item 7) were adopted it would likely use that margin up.
