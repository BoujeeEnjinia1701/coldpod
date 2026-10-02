---
doc_id: CPD-CAL-001
title: ColdPod sizing calculations
project: ColdPod
doc_type: Calculation
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (payload, heat leak, PCM, hold times, Peltier and heat sink, refreeze, thermosiphon, freeze fault, logger, mass, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Lid cold plate, liner cut-out, thinner printed parts and buck-boost driver added; hold times pooled through the plate; refreeze of all PCM; results recomputed
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish; budget $310 in the script; R15 met ($303 against $310); counts updated
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Recomputed for the constructable design (CPD-DDR-003, Draft); PCM volumes and masses now taken from the model's components; results updated
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R8 and R12 against the targets restated on 2026-10-02 (now met on paper); R14 removal for the prototype; sizing.py still to be re-run"
---

# ColdPod sizing calculations

On paper, ColdPod meets ten of its seventeen requirements, has three at risk and misses two, each by a small amount; two cannot be verified at TRL 3. Version 0.2 applies the design changes Amish accepted on 2026-09-25 (CPD-DDR-002): an aluminium cold plate under the lid PCM pack, a second hardware cut-out on the liner at 3 °C, thinner printed parts and a buck-boost Peltier driver. The plate couples the lid pack to the evaporator can, so the Peltier now refreezes all of the PCM, the lid pack no longer melts in long powered holds, and the jacket and lid pack melt together. In v0.3 the hold times were about 14.0 h with no power at 43 °C, 28.4 h off-grid at 32 °C and 17.5 h off-grid at 43 °C; they stay at risk against a ±30 % uncertainty in the heat leak (R4, R5, R6). The liner cut-out closes the freeze fault (R2 met), and the plate and buck-boost stage close R1 and R7. In v0.3 the two misses were refreezing all the PCM (R8: 8.4 h against 8 h, because the lid pack shares the module), and mass (R12: 5.53 kg against 5.5 kg). Version 0.3 set the value-engineering target at $310, as Amish decided on 2026-09-26 (CPD-DDR-002 N3). Version 0.4 recomputes everything for the constructable design of CPD-DDR-003 (accepted by Amish on 2026-10-02): the liner now stands on printed feet with a printed collar, the lid pack sits in a folded aluminium tray, the foam strip is 28 mm tall, the loop lies in the can's bottom corner, and every fixing has been added. The PCM space is now measured on the model rather than estimated, so the PCM falls to 0.935 kg and the holds shorten: about 13.3 h with no power at 43 °C, 27.3 h off-grid at 32 °C and 16.7 h off-grid at 43 °C. Refreezing all the PCM takes 8.0 h, just over the 8 h target (R8), and the case now weighs 5.70 kg empty (R12, 5.5 kg). On 2026-10-02 Amish restated R8 as 9 h and relaxed R12 to 5.75 kg for the prototype, so both are now met on paper (Results). Cost (R15: $308 against $310) is met. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B9], is the line of that script's output that carries it.

> **Safety:** These calculations concern a device meant to protect vaccines and insulin, a 76.8 Wh lithium battery, a combustible paraffin PCM and a heat sink near 53 °C. They are first-principles estimates for a paper proof of concept, not a substitute for datasheets, a fault analysis by a qualified engineer or test. ColdPod is a research and educational prototype, not a medical device, and is not WHO-prequalified. See CPD-PRC-001, Safety.

## Scope and method

The note checks every requirement in CPD-REQ-001 v0.6 against the design in CPD-PRC-001 v0.6 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `levels()` and the volume of every component (`component_volumes_cm3()`), so the layer dimensions used here are the ones in the STEP files and in drawing CPD-DWG-001. It reads prices from `bom/bom.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py` (about 2 min; it builds the model and the refreeze is a time-stepped simulation).

Status rule for the hold times: **met** if the target holds even with 30 % more heat leak than the nominal estimate; **at risk** if it holds only at the nominal leak; **not met** otherwise.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Ambient cases | 25 °C clinic, 32 °C hot day, 43 °C WHO hot zone; constant, shaded, no solar gain | CPD-REQ-001 |
| VIP | Aged centre-of-panel conductivity 0.007 W/(m·K), fumed silica core; 25 mm | Inside the 0.006 to 0.008 W/(m·K) range usually quoted |
| VIP edges | Butt joint between two metallized-film edges with a 1 mm gap: ψ = 0.015 W/(m·K) per metre of joint; one edge against foam: 0.0075 W/(m·K) | Engineering judgment; to confirm with the VIP supplier |
| Geometry of the insulation | Langmuir shape factor for a box: walls A/t, edges 0.54 per metre, corners 0.15 t | Standard conduction shape factors |
| Pipe crossing | 28 mm polyurethane foam strip (0.024 W/(m·K)) across the +X wall, from 18 mm below to 10 mm above the pipes (CPD-DDR-003); two 8 mm tubes with a stainless section, 0.3 mm wall, 40 mm long | Model |
| Sensor wires | Six 28 AWG copper conductors, 100 mm path along a VIP joint | Payload and liner probes |
| PCM | RT 5 HC class; PCM space measured on the model (can less liner, feet, collar, loop and cable; tray interior for the lid pack); 85 % pouch fill; 770 kg/m³ liquid, 880 kg/m³ solid; 180 kJ/kg usable inside 2 to 8 °C (of about 250 kJ/kg listed over the full range); solid conductivity 0.2 W/(m·K); cp 2.0 kJ/(kg·K) liquid, 1.8 solid | Rubitherm RT range data, derated |
| Hold end point | Hold ends when the jacket or the lid pack is fully melted, whichever comes first; the sensible heat of the payload and liner is kept as unclaimed margin | Conservative |
| Peltier module | 127-couple modules, Vmax 15.4 V, ΔTmax 67 K at a 300 K hot side; Imax 3, 4 or 6 A (TEC1-12703, 12704, 12706 classes); Seebeck coefficient, resistance and conductance derived from those ratings and held constant | Standard derivation from datasheet maxima |
| Cold path | 0.40 K/W from the can to the module cold face (loop thermosiphon, cold block, interface) | Engineering judgment for 8 mm two-phase tubes |
| Hot path | 0.55 K/W from the module hot face to air (80 x 80 x 30 mm finned sink with a 70 mm fan, 0.50 K/W, plus 0.05 K/W interface) | Typical for this sink class; to confirm |
| Control | Powered hold keeps the evaporator can at 2 °C; refreeze floor −2 °C at the can; module fed smooth DC from a buck-boost driver, 90 % efficient, from 10 V input upward; fan 0.6 W, controller 0.1 W | Design intent; buck-boost by CPD-DDR-002 |
| Battery | 76.8 Wh; 85 % (65.3 Wh) available to cooling, 15 % kept for the logger | CPD-PRC-001 |
| Refreeze | 25 W cap to the module and 12 W to the battery while charging, inside a 45 W USB-C PD budget; can to liquid PCM 40 W/(m²·K) through the pouch film | Design intent |
| Lid cold plate | 1.5 mm aluminium, 237 W/(m·K), folded into a 204 x 139 mm tray round the lid pack, landing on the evaporator can's 5 mm rim flange (CPD-DDR-003); 0.5 K/W from plate rim to can rim through the gasket seat; lateral conductance taken as 8 k t for a square plate with its edge held | CPD-DDR-002; engineering judgment |
| Cut-outs | Bimetal cut-out on the cold block opening at −5 °C, in series with one on the liner opening at 3 °C | CPD-DDR-002 |
| Mass | Model volumes of every component; added construction parts printed at 80 % fill; 0.05 kg for inserts, standoffs, extra screws and the drain tube; PETG 1.27 g/cm³; printed walls with 2.7 mm of solid perimeters and 20 % infill for the rest (solid below 2.7 mm); shell 3 mm, lid cap 5 mm, end housings 2 mm (CPD-DDR-002); VIP 190 kg/m³ including film; LiFePO4 32700 cell 0.14 kg | Model volumes; typical values |

## A. Payload and size (R3, R13)

The liner is 172 x 107 x 78.5 mm inside [A1]. Less the printed rack and the buffered probe (now a 10 x 40 mm vial above the top layer, CPD-DDR-003), the usable volume is 1.37 L [A2]. It holds 24 pens of 16 mm diameter, in four layers of six [A3], using 100 of 107 mm across and 66 of 78.5 mm in height [A4]; pens up to 172 mm long fit [A5]. R3 is met.

Overall, with the handle up, the case is 366 x 220 x 207 mm (14.4 x 8.7 x 8.1 in) [A6, A7]; the handle pivots now sit on 4 mm printed pads, which adds 8 mm of width, inside the 400 x 250 x 250 mm envelope of R13: met.

## B. Heat leak (drives R4 to R7)

The inside of the insulation is 205 x 140 x 112 mm [B1] (1.5 mm taller than in v0.1, for the lid cold plate). With Langmuir shape factors of 4.854 m for the body and 1.536 m for the lid [B2], the centre-of-panel conductance is 0.0340 W/K and 0.0107 W/K [B3]. The other paths are:

*Table 2. Heat-leak paths.*

| Path | Conductance (W/K) | Tag |
| --- | --- | --- |
| Body panels, centre of panel | 0.0340 | B3 |
| Lid plug, centre of panel | 0.0107 | B3 |
| Body VIP joints, 1.54 m | 0.0230 | B4 |
| Lid plug junction | 0.0103 | B5 |
| Foam strip at the pipe crossing, 28 mm | 0.0069 | B6 |
| Thermosiphon stainless sections (reverse path) | 0.0058 | B7 |
| Sensor wires | 0.0019 | B8 |
| **Body / lid / total** | **0.0717 / 0.0211 / 0.0928** | B9 |

With the PCM at 5 °C, the heat leak is 1.86 W at 25 °C, 2.50 W at 32 °C and 3.53 W at 43 °C [B10]; the taller foam strip adds 0.0013 W/K. The TRL 2 estimate was 0.11 W/K [B11]; the explicit edge and joint terms come to less than the 1.8 multiplier it used. Joints and edges are still about 45 % of the total, so the supplier's edge data matter.

## C. Phase-change material

The PCM space is now measured on the model: the can's inside less the liner, its four feet and collar, the loop tubes and the sensor cable for the jacket, and the inside of the lid tray for the lid pack. The jacket holds 1.023 L and the lid pack 0.406 L [C1], which at 85 % fill is 0.670 kg and 0.265 kg, 0.935 kg in all [C2] (0.972 kg in v0.3). At 180 kJ/kg that is 121 kJ in the jacket and 48 kJ in the lid, 168 kJ in all [C3], or 46.8 Wh [C4]. TRL 2 assumed 1.06 kg and 191 kJ.

## D. Passive hold (R4)

*Table 3. Hold with no power, starting with all the PCM frozen.*

| Ambient | Jacket alone (h) | Lid pack alone (h) | Pooled through the plate (h) | Tag |
| --- | --- | --- | --- | --- |
| 25 °C | 23.4 | 31.5 | 25.2 | D1 |
| 32 °C | 17.3 | 23.3 | 18.7 | D1 |
| 43 °C | 12.3 | 16.6 | **13.3** | D1 |

The lid cold plate conducts about 2.8 W/K from its centre to the can rim [D1b], 135 times the lid's heat leak [D1c], so the jacket and the lid pack share their latent heat and melt together. In v0.1, without the plate, the hold ended when the jacket melted (13.0 h). R4 is now 13.3 h at 43 °C [D2] against 12 h (14.0 h in v0.3). With 30 % more heat leak it falls to 10.2 h [D3]; an 11 % rise in heat leak uses up the margin [D4]. R4 is **at risk**.

## E. Peltier module, cold path and heat sink (R7)

A Peltier module that is switched off conducts heat. The derived off-state conductance is 0.268 W/K for the TEC1-12703 class, 0.357 W/K for the 12704 and 0.536 W/K for the 12706 [E1]. Even the smallest is 2.9 times the whole box's heat leak [E2], which is why the thermosiphon diode (section H) is needed.

The same conductance decides which module can hold at 43 °C, because the hot side runs about 50 K above the cold side:

*Table 4. Powered hold, can at 2 °C: current, module power, COP and input power (module through a 90 % driver, plus fan and controller).*

| Module | 25 °C | 32 °C | 43 °C | Tag |
| --- | --- | --- | --- | --- |
| TEC1-12703 | 0.74 A, 3.2 W, 0.67, **4.2 W** | 1.04 A, 6.2 W, 0.45, **7.6 W** | 1.70 A, 16.3 W, 0.23, **18.8 W** | E3 |
| TEC1-12704 | 0.93 A, 3.9 W, 0.55, 5.0 W | 1.32 A, 7.7 W, 0.36, 9.3 W | 2.24 A, 21.5 W, 0.18, 24.5 W | E3 |
| TEC1-12706 | 1.35 A, 5.6 W, 0.38, 6.9 W | 1.95 A, 11.5 W, 0.24, 13.5 W | Cannot lift the load | E3 |

The TEC1-12706 named at TRL 2 cannot hold at 43 °C with this heat sink: its own back-conduction exceeds what it can pump. The **TEC1-12703 class** is chosen. At 43 °C its cold face is at 0.5 °C and its hot face at 54.0 °C [E4]; it needs 9.5 V [E5], and the sink rejects 5.3 W, 9.0 W and 20.1 W at 25, 32 and 43 °C [E6]. The sink base reaches about 53 °C at 43 °C [E7].

R7 asks for an indefinite hold up to 43 °C on 12 V or 45 W USB-C PD. The input is 18.8 W, well inside 41.4 W available from a 45 W PD source [E8], and 1.97 A from a 10 V vehicle input [E9]. The module needs 9.5 V, which left a plain buck driver almost no headroom at a 10 V input; the buck-boost driver adopted in CPD-DDR-002 can raise the module voltage above the input when it must [E9b]. The lid pack is now held frozen by the cold plate in powered hold (section F). R7 is **met** on paper.

The driver matters. Unfiltered on/off pulse-width modulation at 12.8 V, giving the same average heat lift at 43 °C, needs a 0.80 duty and 25.7 W at the module [E10], about 60 % more than smooth DC (16.3 W). The power board therefore uses a buck-boost driver with an LC filter, not on/off PWM. CPD-PRC-001 v0.2 said PWM improves COP; that was corrected in v0.3.

## F. Off-grid hold (R5, R6)

65.3 Wh of the battery is available for cooling [F1]. While the battery runs, the module holds the can at 2 °C and all the PCM stays frozen, including the lid pack on its cold plate. Then the jacket and lid pack hold passively together.

*Table 5. Battery, then PCM.*

| Ambient | Battery phase (h) | Passive phase (h) | Total (h) | With 30 % more leak (h) | Tag |
| --- | --- | --- | --- | --- | --- |
| 25 °C | 15.4 | 25.2 | 40.6 | | F2 |
| 32 °C | 8.6 | 18.7 | **27.3** | 21.4 | F2, F2b |
| 43 °C | 3.5 | 13.3 | **16.7** | 12.6 | F2, F2b |

R5 (24 h at 32 °C) and R6 (16 h at 43 °C, relaxed by CPD-DDR-001 D5) are met at the nominal heat leak and missed at +30 %: both are **at risk**. In v0.3 they were 28.4 h and 17.5 h; R6 now holds by 0.7 h at the nominal leak. For reference, the 153.6 Wh 4S2P pack not chosen in D4 would give 20.2 h at 43 °C [F6].

In powered hold at 43 °C the plate carries the lid's 0.87 W heat leak to the can [F3] with its centre about 0.3 K above the rim [F4], so the lid pack stays frozen near 2.8 °C [F5]. In v0.1 the lid pack melted after about 21 h and settled near 13.8 °C above the top layer of pens; that risk to R1 and R7 is closed.

## G. Refreeze (R8)

The decided evaporator position (outer face of the PCM, CPD-DDR-001 D3) is sized here. A 90 x 60 mm plate on one end of the jacket, as drawn at TRL 2, cannot freeze a paraffin jacket that runs 200 mm around the liner: solid paraffin conducts only about 0.2 W/(m·K). The evaporator is therefore a 1.0 mm aluminium can that lines the outer face of the jacket on four sides and the floor, 0.0943 m² in contact [G1], with an 8 mm copper evaporator loop around its base. The loop now lies in the can's bottom inside corner, bonded to floor and wall (CPD-DDR-003). The frozen jacket is effectively 8.1 mm thick [G2], and the can wall above the loop acts as a fin with 0.66 efficiency [G3].

The lid pack freezes through the 1.5 mm lid cold plate, now a tray that lands on the can's 5 mm rim flange when the lid closes [G6]. A time-stepped model (sensible cooling of all the liquid PCM, the liner, the can and the plate through the pouch film, then two quasi-steady freezing fronts in parallel, one in the jacket and one on the plate, with the module current chosen each step within the 25 W cap and the −2 °C can floor) gives:

*Table 6. Refreeze of all the PCM from 25 °C, box empty, 25 °C ambient.*

| Module | Sensible part (h) | Jacket frozen (h) | Lid pack frozen (h) | All PCM (h) | Tag |
| --- | --- | --- | --- | --- | --- |
| TEC1-12703 | 1.2 | 6.8 | 8.0 | **8.0** | G4 |
| TEC1-12704 | 1.1 | 6.5 | 7.6 | 7.7 | G4 |
| TEC1-12706 | 1.1 | 6.7 | 7.9 | 7.9 | G4 |

Conduction alone would allow about 1.5 h for the jacket [G5] and 2.0 h for the lid pack [G7], so the module, not the PCM, sets the rate. The jacket alone took 5.5 h in v0.1; with the lid pack actively frozen the whole charge took 8.4 h in v0.3, and with the smaller PCM charge of the constructable design it takes 8.0 h, a few minutes over the 8 h target (the script prints the value to two decimals in its R8 line). R8 was not met against 8 h, by a margin far inside the model's uncertainty; against the 9 h restated on 2026-10-02 it is met. Giving the module 30 W and the battery 7 W inside the same PD budget brings it to 7.8 h [G10], and stretches the battery recharge to 11.5 h [G11], because the −2 °C can floor and the module's COP limit the lift. Options are in the design decisions register (CPD-DEC-001). The v0.1 alternative of no lid pack and a 20 mm jacket (1.010 kg, all in the jacket [N1]; body 10 mm longer and wider, 10 mm lower [N2]) is kept for reference only; it was not the recommended option.

The battery recharges in about 6.7 h at 12 W alongside the refreeze [G8], for a total input of 40.5 W [G9], inside the 45 W PD budget.

## H. Thermosiphon: diode ratio and tilt

The loop thermosiphon conducts about 2.50 W/K forward and 0.0058 W/K in reverse (the stainless wall sections), a ratio of 431 [H1]. For comparison, bolting the chosen module to the liner would raise the box conductance to 0.361 W/K [H2] and cut the passive hold at 43 °C to 3.4 h [H3]. The thermosiphon keeps its place (CPD-DDR-001 D2), and the can and loop as sized here are confirmed (CPD-DDR-002), with the mechanical disconnect kept as the fallback.

With the loop now in the can's bottom corner, the condenser sits 81.0 mm above the evaporator loop [H4] (76.0 mm in v0.3). The whole loop stays below the condenser for tilts up to 19° with the cooling head down [H5] and 42° with the front or back down [H7]; with the cooling head down, part of the loop stays below the condenser up to 65° [H6]. Beyond those angles the part of the loop above the condenser dries out and cooling falls; the PCM carries the load meanwhile. Whether a motorbike carrier holds within 19° on average is an open question for a lab or field test after TRL 3.

## I. Freeze fault (R2)

In normal operation the coldest surface (the can, down to −2 °C during refreeze) is separated from the liner by the PCM, and the controller stops cooling at a liner reading of 3 °C, so R2 holds. With a stuck-on driver, the module draws about 3.6 A from the 14.4 V charge rail [I4] until the hardware cut-out on the cold block opens at −5 °C [I1]. With that cut-out alone, once the PCM is fully frozen nothing stops the liner from following the can down to about −4 °C in a cool room [I2], which was why R2 was not met in v0.1.

A second hardware cut-out on the liner, in series with the first, is now in the design (CPD-DDR-002; BOM line 14). A lumped estimate of the liner after the cut-out opens (the payload and liner sharing heat with the colder frozen jacket) gives 1.2 °C for a 2 °C setting and 2.0 °C for a 3 °C setting [I3]. With the adopted 3 °C setting the liner settles near 2.0 °C [I5]. **R2 is met** on paper. The lid cold plate faces the cavity across a 12.5 mm air gap above the top layer of pens and touches no payload (the payload probe vial now lies in that gap, 1.5 mm below the tray); it follows the can, so it sits near 2 °C in hold and reaches −2 °C only during refreezing, which R8 defines with the box empty.

## J. Logger (R9, R11)

Sixty days of one 16-byte record per minute take 1.38 MB of the 2.10 MB flash [J1]: R9 is met on storage, and on accuracy by sensor selection. The logger and standby loads come to about 0.78 mW [J2]; with a 5 mW design allowance [J3], the 15 % reserve lasts about 96 days [J4], far beyond the 14 days of R11: met.

## K. Mass (R12)

*Table 7. Empty mass [K1].*

| Part | kg | Part | kg |
| --- | --- | --- | --- |
| Shell with pads and towers (PETG, printed, 3 mm) | 0.702 | Loop tubes (copper) | 0.094 |
| Lid cap (5 mm), gasket, latches | 0.313 | Cold block (aluminium) | 0.071 |
| Lid cold plate tray (aluminium) | 0.168 | Peltier module | 0.025 |
| Handle and strap | 0.200 | Heat sink | 0.197 |
| VIP set | 0.858 | Fan and guard | 0.060 |
| Foam strip | 0.003 | End housings with ears (PETG, printed, 2 mm) | 0.296 |
| Construction parts, printed | 0.086 | LiFePO4 cells, 4 x 32700 | 0.560 |
| Inserts, standoffs, extra screws, drain tube | 0.050 | BMS, fuse, holder | 0.080 |
| PCM | 0.935 | Electronics, including both cut-outs | 0.170 |
| PCM pouches | 0.080 | Wiring and hardware | 0.150 |
| Liner (aluminium) | 0.257 | Rack (PETG) | 0.083 |
| Evaporator can with rim flange (aluminium) | 0.259 | | |

The thinner printed parts adopted in CPD-DDR-002 save 0.05 kg on the shell, 0.04 kg on the lid cap and 0.11 kg on the end housings [O1]. The constructable design (CPD-DDR-003) adds the parts every fixing needs: printed pads and towers on the shell, ears on the housings, the liner feet and collar, the block frame, slot fillers, the duct cover, the cell cradle, inserts and standoffs, and a folded tray in place of the flat lid plate (0.17 kg in all for the plate [O3]). Less PCM offsets part of it. The total is **5.70 kg (12.6 lb)** empty [K2, K3] and 6.38 kg with 24 pens [K4], against the relaxed target of 5.5 kg: R12 was not met, by 0.20 kg [O4] (0.03 kg in v0.3). On 2026-10-02 Amish relaxed R12 to 5.75 kg for the prototype, to be settled by weighing at TRL 4; against it the case is met on paper with 0.05 kg of margin.

## L. Cost and battery (R14, R15)

All 17 BOM lines are priced [L1]; the estimated cost is $308 [L2] against the $310 value-engineering target (a hypothetical control target, CPD-DDR-002 N3): **R15 is within the value-engineering target**, by $2. The constructable design adds line 17 (printed construction parts, inserts and the foam strip, $4) and $1 for folding the lid tray ($303 in v0.3). The accepted changes add the lid cold plate (about $5), the liner cut-out (about $3) and the buck-boost driver (about $4), and the thinner printed parts save about $4 of filament; v0.1 was $295. There is still no custom PCB. The battery is 76.8 Wh [L3], under the 100 Wh airline limit: R14 is met for the prototype, the battery bay on four screws counting as removable (CPD-DDR-003 A3, 2026-10-02); a shipping switch is added before any field or air travel use.

## P. Foam variant (CPD-DDR-001 D7)

The documented low-cost variant replaces the VIPs with 25 mm polyurethane foam (0.024 W/(m·K)). With the same shape factors and no VIP joints, the conductance is 0.161 W/K [P1] and the passive hold at 43 °C, pooled through the lid cold plate, falls to about 7.6 h [P2] (7.9 h in v0.3; 7.4 h in v0.1, jacket only), so the foam variant does not meet R4. TRL 2 estimated about 7 h.

## Checks against earlier figures

*Table 8. TRL 2 figures in CPD-PRC-001 v0.2 and the README, checked against this note (v0.4 values).*

| Quantity | TRL 2 | TRL 3 | Tag |
| --- | --- | --- | --- |
| Overall conductance | 0.11 W/K | 0.093 W/K | B9 |
| PCM | 1.06 kg, 191 kJ | 0.935 kg, 168 kJ | C2, C3 |
| Payload volume | about 1.2 L | 1.37 L | A2 |
| Passive hold 25 / 32 / 43 °C | 24 / 18 / 12.7 h | 25.2 / 18.7 / 13.3 h, pooled | D1 |
| Input power to hold 25 / 32 / 43 °C | 4.7 / 8.1 / 17.4 W | 4.2 / 7.6 / 18.8 W | E3 |
| Battery then PCM 25 / 32 / 43 °C | 38 / 26 / 16 h | 40.6 / 27.3 / 16.7 h | F2 |
| Refreeze | about 5 h (text), about 6 h (table) | 8.0 h, all PCM (8.4 h in v0.3; 5.5 h, jacket only, in v0.1) | G4 |
| Heat rejected 25 / 32 / 43 °C | 6 / 10 / 21 W | 5.3 / 9.0 / 20.1 W | E6 |
| Heat sink temperature at 43 °C | 55 to 65 °C | about 53 °C | E7 |
| Peltier off-state conductance | 0.3 to 0.5 W/K | 0.27 to 0.54 W/K | E1 |
| Peltier module | TEC1-12706 | TEC1-12703 class | E3 |
| PWM "for better COP" | stated | smooth DC; on/off PWM costs 60 % more | E10 |
| Battery recharge | about 3 h at 25 W | about 6.7 h at 12 W alongside refreeze | G8 |
| Logger reserve | weeks | about 96 days | J4 |
| Log storage, 60 days | about 1.4 MB | 1.38 MB | J1 |
| Size | 370 x 215 x 205 mm | 366 x 220 x 207 mm | A6 |
| Mass empty | 5.2 kg | 5.70 kg | K2 |
| Parts cost | $280 | $308 | L2 |
| Warm-payload pull-down | about 3.7 h | not recomputed; removed from the precis, which keeps the advice to load the payload pre-cooled | |

## Results

*Table 9. Requirements against this note. Status: met, at risk, not met, or not verifiable at TRL 3.*

| ID | Target (CPD-REQ-001 v0.8) | Value | Status |
| --- | --- | --- | --- |
| R8 | Refreeze a fully melted PCM in 9 h or less at 25 °C (restated from 8 h, 2026-10-02) | All PCM 8.0 h (jacket 6.8 h, lid pack 8.0 h) [G4] | Met |
| R12 | 5.75 kg or less empty for the prototype (relaxed, 2026-10-02) | 5.70 kg [K2] | Met on paper |
| R15 | Parts $310 or less; no custom PCB | $308 [L2]; modules on perfboard | Within the value-engineering target |
| R4 | 12 h or more at 43 °C, no power | 13.3 h; 10.2 h at +30 % leak [D2, D3] | At risk |
| R5 | 24 h or more at 32 °C, battery then PCM | 27.3 h; 21.4 h at +30 % leak [F2] | At risk |
| R6 | 16 h or more at 43 °C, battery then PCM (relaxed) | 16.7 h; 12.6 h at +30 % leak [F2] | At risk |
| R1 | 2 to 8 °C at the payload probe | Can at 2 °C, liner 2 to 5 °C; lid pack held frozen near 2.8 °C by the plate at 43 °C [F5] | Met |
| R2 | No payload-contact surface below 1 °C, including a stuck-on driver | Normal: met. Fault: liner near 2.0 °C with the 3 °C liner cut-out [I5] | Met |
| R3 | 1.0 L or more; 20 or more pens up to 170 mm | 1.37 L; 24 pens; up to 172 mm [A2 to A5] | Met |
| R7 | Hold indefinitely up to 43 °C on 12 V or 45 W USB-C PD | 18.8 W input [E8]; buck-boost from 10 V [E9b]; lid pack held [F5] | Met |
| R9 | ±0.5 °C, log every 1 min, 60 days, CSV export | 1.38 MB of 2.10 MB [J1]; accuracy by selection | Met |
| R11 | Logger runs 14 days after cooling stops | About 96 days [J4] | Met |
| R13 | Fits 400 x 250 x 250 mm | 366 x 220 x 207 mm [A6] | Met |
| R14 | Battery 100 Wh or less | 76.8 Wh [L3] | Met |
| R17 | "Research prototype, not a medical device" on box, start screen and logs | By design | Met |
| R10 | Alarm logic and thresholds | Design intent only; no firmware sketch exists at TRL 3 | Not verifiable at TRL 3 |
| R16 | IP54 bays; 0.5 m drop while loaded | Needs a test | Not verifiable at TRL 3 |

Counts: 12 met, 3 at risk, 2 not verifiable at TRL 3, against the targets restated on 2026-10-02 (CPD-REQ-001 v0.8); the script still prints 10 met and 2 not met against 8 h and 5.5 kg until it is re-run. Against the old targets the counts were 10 met, 3 at risk, 2 not met, 2 not verifiable, the same as v0.3 (v0.2: 9 met, 3 at risk, 3 not met; v0.1: 7 met, 5 at risk, 3 not met, 2 not verifiable).

## Limits of this note

- All values are paper estimates. The heat leak (joint ψ, aged VIP conductivity), the thermosiphon resistance, the heat sink resistance and the PCM's usable latent heat inside 2 to 8 °C are the largest uncertainties, in that order.
- The Peltier model uses constant properties derived from datasheet maxima. Real modules vary by maker.
- The lid pack temperature in powered hold and its refreeze rest on an assumed 0.5 K/W seat between the tray and the can's rim flange; a poor seat would slow the lid pack's refreeze. Stratification in the cavity and contact with the rack are not modelled.
- No solar gain is included. A carrier in direct sun would see more heat than the 43 °C shaded case.
