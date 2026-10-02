---
doc_id: CPD-DDR-003
title: ColdPod design for construction
project: ColdPod
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish (2026-10-02), with A1 to A4 as recommended (A4: R-134a); status kept Draft"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Table 1 and its knock-on changes, and the recommendations for A1 to A4 in Table 3, which are now decided and recorded in the design decisions register (CPD-DEC-001). Nothing in this record changes what ColdPod does or its pitch; A3 and A4 add safety rules (below).

## Context

On 2026-09-30 Amish asked for a build plan that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model (CPD-DDR-002) showed what ColdPod does and sized it, but many of its parts were massing shapes: they touched only by coincidence, had no fixing, or could not be made or put together as drawn. Checking the model with build123d (every pair of parts tested for overlap and gap) found one overlap, the payload probe inside the pens (2.35 cm³), and showed that the loop, the cold block stack, the end housings, the liner, the lid cold plate, the handle, the electronics and the cables had no fixing or route. A closer look at the way the parts go together found the rest.

The governing constraint is the vacuum-insulated panels: a VIP behind every wall of the shell means no screw, rivet or drill may ever pass through a shell wall. Every outside fixing therefore lands on a printed pad or tower on the shell, with a heat-set insert that stops short of the panel.

The changes keep what ColdPod does: the same payload space and pen layout, the same layers (liner, 5 °C PCM jacket and lid pack, evaporator can, 25 mm VIPs, printed shell), the same loop thermosiphon, Peltier module, heat sink, battery, electronics, cut-outs and alarms, and the same overall length and height. Every change is in `cad/src/model.py`, which now builds 48 separate components (49 with the payload) and runs 63 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must clear do clear, and no other pair of the 1,176 overlaps. All 63 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The buffered payload probe (14 x 36 mm, standing in the corner of the liner) overlapped the pens of the first column by 2.35 cm³. | A 10 x 40 mm buffered vial lying across the top layer of pens at the cooling end, held by a printed clip on the liner's end wall, 1.8 mm above the pens and 1.5 mm below the lid tray. | Keeps 24 pens of up to 172 mm. The space above the top layer (12.5 mm) was empty. Where the probe should sit to read the warmest pen stays an open question in CPD-PRC-001. |
| P2 | The evaporator loop floated 5 mm inside the PCM jacket, touching nothing, with sharp corners. Sealed pouches cannot be "formed around the tubes". | The ring lies in the bottom inside corner of the can, touching floor and wall, bonded with thermally conductive epoxy; corners bent to 25 mm radius. | The can is the evaporator; a tube bonded to it feeds the whole can. The condenser now sits 81 mm above the loop (76 mm), so the tilt limit with the cooling head down rises from 18° to 19°. |
| P3 | Each riser turned 90° to horizontal inside the 14 mm gap between liner and can, which no tube bender can do, and left through round holes in the can and the shell, so a one-piece loop could never be put in. | Risers bend at 17.5 mm radius (a lever bender for 8 mm tube), with most of the bend inside the foam strip. The can has two riser slots and the shell three slots (two pipes, one cable) open at the rim; three printed slot fillers close the shell slots after assembly. The foam strip grows from 20 to 28 mm tall (18 mm below to 10 mm above the pipes) so the bend clears the lower VIP panel by 1 mm or more. | The whole loop, block and charge stub can then be made, leak tested and charged on the bench by a refrigeration technician, and lowered into the case as one sealed unit. |
| P4 | The cold block had no condensing passage and no joint to the copper tubes. | Two 8.1 mm tube sockets in its back face, a 6 mm condensing passage drilled through both, and a 6 mm copper charge stub in the passage mouth; tubes and stub joined with aluminium-to-copper brazing rod; the stub is pinched shut after charging. | A sealed refrigerant circuit with the aluminium block as condenser, as sized in CPD-CAL-001 section H. |
| P5 | The Peltier module, heat sink and fan hung on the two copper tubes. | A printed block frame (3.5 mm, thinner than the 4 mm module) holds the block against the shell end and is screwed to two printed towers on the shell. Two M3 screws through the heat sink base into the block clamp the module. The fan and a finger guard screw to the sink. | The stack is held by the shell, not the tubes. The frame never touches the hot sink (0.5 mm gap), so it is not a heat path, and the clamp force goes through the module. |
| P6 | The end housings had no fixing, and the shell can take no screw through its walls. | Four printed pads with M3 heat-set inserts on each end face of the shell, and four ears on each housing; one M3 screw per ear. | Respects the VIP rule; the housings come off for service with four screws. |
| P7 | The handle pivots and the two draw latches had no fixing. | Printed pads on the shell: two with M5 inserts for the handle pivots, two with M3 inserts for the latches; keepers on the lid cap with short inserts. The strap clips to D-rings under the pivot screws. The handle arms move out 4 mm each side. | Same VIP rule. Overall width rises from 212 to 220 mm, inside R13's 250 mm. Latch and strap positions follow the recommendations already made for the appearance model (`docs/REVIEW.md`, 2026-09-26, items 4 and 7). |
| P8 | The liner rested on the PCM pouch with no location; the lid cold plate was a flat sheet that "seats on the can rim" on a 1 mm edge, with no fixing to the lid. | The can gets a 5 mm inward rim flange. The liner stands on four printed feet (12 x 12 x 14 mm) on the can floor and is centred by a printed collar inside the flange. The lid cold plate becomes a folded tray (204 x 139 x 16.5 mm, 6 mm inward lip) that holds the lid pack, bonded to the lid VIP plug, which is bonded to the cap; the tray lands on the flange with 5.5 mm of overlap. | Plastic feet and collar keep the liner off the can (design choice 3). The flange gives the tray a real landing for the 0.5 K/W seat that CPD-CAL-001 assumes. Cap, plug, tray and pack lift off as one. |
| P9 | The VIPs were one solid box. | Seven panels bought to size (floor, front, back, battery end, cooling end lower and upper, lid plug), butt jointed on acrylic foam tape, with the foam strip cut round the pipes and cable; the lid plug and tray 0.5 mm under the opening. | VIPs are ordered to size and can never be cut; the list in BOM line 4 is the order. |
| P10 | The power board, logger, cells and display touched nothing. | Power board on four M3 standoffs on the head floor; cells in a printed cradle with the BMS on top and a strap; logger on four standoffs on the bay's back wall; display under a window in the bay top; alarm light in a hole. | Standard fixings for bought modules. |
| P11 | Condensate from the cold block and pipes would drip onto the power board below them. | A drip tray printed on the block frame, draining through a 4 mm tube and a hole in the head floor, clear of the board. | The concept says the cooling head drains outward; this is how. |
| P12 | No route for the sensor cable out of the cavity, nor for the battery and sensor leads between the two housings; no inlet positions. | The sensor cable leaves through grommets in the liner and can and its own shell slot at the cooling end. A printed cable duct cover on the shell's back face links the two housings. The 12 V and USB-C inlets sit low on the cooling head's end wall; the lid switch is a reed switch inside the head with a magnet in the lid cap. | Keeps every wire out of the VIP joints except the existing crossing; inlet position as recommended for the appearance model (item 3). |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| PCM | 0.972 to 0.935 kg (jacket 0.670, lid 0.265), now measured on the model rather than estimated [C2] | Feet, collar, cable and the tray walls take space; the analytic estimate had ignored them |
| Hold times | No power at 43 °C 14.0 to 13.3 h; off-grid 28.4 to 27.3 h at 32 °C and 17.5 to 16.7 h at 43 °C [D2, F2]. R4, R5 and R6 stay at risk | Less PCM and a slightly larger foam strip (0.093 W/K overall) |
| Refreeze | All PCM 8.4 to 8.0 h, a few minutes over the 8 h target [G4]; R8 still not met | Less PCM to freeze |
| Mass | 5.53 to 5.70 kg empty [K2]; R12 now missed by 0.20 kg | Pads, towers, ears, feet, collar, frame, fillers, duct, cradle, inserts and the folded tray |
| Size | 366 x 212 x 207 to 366 x 220 x 207 mm [A6]; R13 met | Handle pivot pads |
| Cost | $303 to $308 against the $310 value-engineering target [L2]: line 2 $12 to $13, new line 17 at $4; R15 within the target | Parts added for construction |
| Drawings | CPD-DWG-001 Rev P4; making sketches CPD-DWG-101 to 115 added | Follows the model |
| Documents | CPD-CAL-001 v0.4, CPD-REQ-001 v0.6, CPD-PRC-001 v0.6, BOM and BOM notes; new CPD-BLD-001 and CPD-DEC-001 | Follows the model |

*Table 3. Items proposed to Amish; all accepted on 2026-10-02 as recommended in the register (A4 with R-134a named).*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Accept the design-for-construction changes in Table 1. | (a) accept; (b) accept with changes. | (a). |
| A2 | Mass: R12 is now missed by 0.20 kg, not 0.03 kg (this replaces the earlier question CPD-DDR-002 N2). Every added gram is a fixing the case needs. | (a) relax R12 to 5.75 kg; (b) keep 5.5 kg and settle it by weighing at TRL 4; (c) look for mass now: a 1.0 mm tray (about 0.05 kg, slower lid refreeze), a lighter handle and strap. | (a), because the extra mass is what it takes to build the case; (c) if the target must stay. Accepted 2026-10-02: R12 is 5.75 kg for the prototype, weighed at TRL 4, with the base bumper left off. |
| A3 | Battery removal (R14 asks for a removable battery or a shipping switch): the pack now comes out by removing the battery bay (four screws) and unplugging the duct leads. | (a) count that as removable for the prototype; (b) add a shipping switch in the bay. | (a) for the prototype; revisit with airline guidance before field use. Accepted 2026-10-02: before any field or air travel use, add the shipping switch and check the carrier's lithium battery rules. |
| A4 | Refrigerant for the loop: CPD-CAL-001 sizes the loop by its conductance and does not name a working fluid, and the charge must be set before the technician fills it. | Choose with the technician, for example R-134a or R-1234yf, by the charge needed and local rules. | Decide with the technician at TRL 4. Accepted 2026-10-02 as changed in the register: R-134a (non-flammable, A1) for the prototype, charge set by the technician from the loop volume; R-1234yf (A2L) only for a product version under local rules. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CPD-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement counts are unchanged at 10 met, 3 at risk, 2 not met (R8, R12), 2 not verifiable at TRL 3 (CPD-CAL-001 v0.4); R12's miss is larger and R8's smaller. With the decisions of 2026-10-02, R12 is relaxed to 5.75 kg and R8 restated as 9 h, so both are met on paper: 12 met, 3 at risk, 2 not verifiable (CPD-REQ-001 v0.8).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept handle position, a flat lid plate and no pads, towers, slots or duct; they need regenerating on Amish's Mac, where Blender is.
- Building the loop needs a refrigeration technician; this is called out as a safety stop in the build plan.
