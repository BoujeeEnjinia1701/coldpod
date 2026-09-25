---
doc_id: CPD-CAL-001
title: ColdPod sizing calculations
project: ColdPod
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (payload, heat leak, PCM, hold times, Peltier and heat sink, refreeze, thermosiphon, freeze fault, logger, mass, cost)
---

# ColdPod sizing calculations

On paper, ColdPod meets seven of its seventeen requirements, has five at risk and misses three; two cannot be verified at TRL 3. The insulation is better than the TRL 2 estimate (0.091 W/K rather than 0.11 W/K), so the hold times survive a smaller PCM charge: about 13.0 h with no power at 43 °C, 26.5 h off-grid at 32 °C and 16.5 h off-grid at 43 °C. Those margins are thin against a ±30 % uncertainty in the heat leak, so R4, R5 and R6 are at risk. The misses are the freeze fault (R2: a stuck-on driver can pull the liner to about −4 °C past the −5 °C cold-block cut-out), the lid PCM pack (R8: it has no cold path, so the Peltier cannot refreeze it) and mass (R12: 5.60 kg against the relaxed 5.5 kg). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B9], is the line of that script's output that carries it.

> **Safety:** These calculations concern a device meant to protect vaccines and insulin, a 76.8 Wh lithium battery, a combustible paraffin PCM and a heat sink near 53 °C. They are first-principles estimates for a paper proof of concept, not a substitute for datasheets, a fault analysis by a qualified engineer or test. ColdPod is a research and educational prototype, not a medical device, and is not WHO-prequalified. See CPD-PRC-001, Safety.

## Scope and method

The note checks every requirement in CPD-REQ-001 v0.3 against the design in CPD-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and `levels()`, so the layer dimensions used here are the ones in the STEP files and in drawing CPD-DWG-001. It reads prices from `bom/bom.csv`. Run it from the repo root with `python docs/04-calcs/sizing.py` (about 30 s; the refreeze is a time-stepped simulation).

Status rule for the hold times: **met** if the target holds even with 30 % more heat leak than the nominal estimate; **at risk** if it holds only at the nominal leak; **not met** otherwise.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Ambient cases | 25 °C clinic, 32 °C hot day, 43 °C WHO hot zone; constant, shaded, no solar gain | CPD-REQ-001 |
| VIP | Aged centre-of-panel conductivity 0.007 W/(m·K), fumed silica core; 25 mm | Inside the 0.006 to 0.008 W/(m·K) range usually quoted |
| VIP edges | Butt joint between two metallized-film edges with a 1 mm gap: ψ = 0.015 W/(m·K) per metre of joint; one edge against foam: 0.0075 W/(m·K) | Engineering judgment; to confirm with the VIP supplier |
| Geometry of the insulation | Langmuir shape factor for a box: walls A/t, edges 0.54 per metre, corners 0.15 t | Standard conduction shape factors |
| Pipe crossing | 20 mm polyurethane foam strip (0.024 W/(m·K)) across the +X wall; two 8 mm tubes with a stainless section, 0.3 mm wall, 40 mm long | Model |
| Sensor wires | Six 28 AWG copper conductors, 100 mm path along a VIP joint | Payload and liner probes |
| PCM | RT 5 HC class; 85 % pouch fill; 770 kg/m³ liquid, 880 kg/m³ solid; 180 kJ/kg usable inside 2 to 8 °C (of about 250 kJ/kg listed over the full range); solid conductivity 0.2 W/(m·K); cp 2.0 kJ/(kg·K) liquid, 1.8 solid | Rubitherm RT range data, derated |
| Hold end point | Hold ends when the jacket or the lid pack is fully melted, whichever comes first; the sensible heat of the payload and liner is kept as unclaimed margin | Conservative |
| Peltier module | 127-couple modules, Vmax 15.4 V, ΔTmax 67 K at a 300 K hot side; Imax 3, 4 or 6 A (TEC1-12703, 12704, 12706 classes); Seebeck coefficient, resistance and conductance derived from those ratings and held constant | Standard derivation from datasheet maxima |
| Cold path | 0.40 K/W from the can to the module cold face (loop thermosiphon, cold block, interface) | Engineering judgment for 8 mm two-phase tubes |
| Hot path | 0.55 K/W from the module hot face to air (80 x 80 x 30 mm finned sink with a 70 mm fan, 0.50 K/W, plus 0.05 K/W interface) | Typical for this sink class; to confirm |
| Control | Powered hold keeps the evaporator can at 2 °C; refreeze floor −2 °C at the can; module fed smooth DC from a buck driver, 90 % efficient; fan 0.6 W, controller 0.1 W | Design intent |
| Battery | 76.8 Wh; 85 % (65.3 Wh) available to cooling, 15 % kept for the logger | CPD-PRC-001 |
| Refreeze | 25 W cap to the module and 12 W to the battery while charging, inside a 45 W USB-C PD budget; can to liquid PCM 40 W/(m²·K) through the pouch film | Design intent |
| Lid pack | Couples to the cavity through about 12 mm of stably stratified air, 2 W/(m²·K) | Conduction through still air |
| Mass | PETG 1.27 g/cm³; printed walls with 2.7 mm of solid perimeters and 20 % infill for the rest; VIP 190 kg/m³ including film; LiFePO4 32700 cell 0.14 kg | Model volumes; typical values |

## A. Payload and size (R3, R13)

The liner is 172 x 107 x 78.5 mm inside [A1]. Less the printed rack and the buffered probe, the usable volume is 1.36 L [A2]. It holds 24 pens of 16 mm diameter, in four layers of six [A3], using 100 of 107 mm across and 66 of 78.5 mm in height [A4]; pens up to 172 mm long fit [A5]. R3 is met.

Overall, with the handle up, the case is 368 x 214 x 207 mm (14.5 x 8.4 x 8.1 in) [A6, A7], inside the 400 x 250 x 250 mm envelope of R13: met.

## B. Heat leak (drives R4 to R7)

The inside of the insulation is 205 x 140 x 110 mm [B1]. With Langmuir shape factors of 4.809 m for the body and 1.536 m for the lid [B2], the centre-of-panel conductance is 0.0337 W/K and 0.0107 W/K [B3]. The other paths are:

*Table 2. Heat-leak paths.*

| Path | Conductance (W/K) | Tag |
| --- | --- | --- |
| Body panels, centre of panel | 0.0337 | B3 |
| Lid plug, centre of panel | 0.0107 | B3 |
| Body VIP joints, 1.53 m | 0.0229 | B4 |
| Lid plug junction | 0.0103 | B5 |
| Foam strip at the pipe crossing | 0.0056 | B6 |
| Thermosiphon stainless sections (reverse path) | 0.0058 | B7 |
| Sensor wires | 0.0019 | B8 |
| **Body / lid / total** | **0.0700 / 0.0211 / 0.0911** | B9 |

With the PCM at 5 °C, the heat leak is 1.82 W at 25 °C, 2.46 W at 32 °C and 3.46 W at 43 °C [B10]. The TRL 2 estimate was 0.11 W/K [B11]; the explicit edge and joint terms come to less than the 1.8 multiplier it used. Joints and edges are still about 45 % of the total, so the supplier's edge data matter.

## C. Phase-change material

The aluminium evaporator can (section G) and the loop tubes take some of the PCM space. The jacket holds 1.055 L and the lid pack 0.430 L [C1], which at 85 % fill is 0.691 kg and 0.282 kg, 0.972 kg in all [C2]. At 180 kJ/kg that is 124 kJ in the jacket and 51 kJ in the lid, 175 kJ in all [C3], or 48.6 Wh [C4]. TRL 2 assumed 1.06 kg and 191 kJ.

## D. Passive hold (R4)

*Table 3. Hold with no power, starting with all the PCM frozen.*

| Ambient | Jacket melts (h) | Lid pack melts (h) | Pooled (h) | Tag |
| --- | --- | --- | --- | --- |
| 25 °C | 24.7 | 33.4 | 26.7 | D1 |
| 32 °C | 18.3 | 24.7 | 19.8 | D1 |
| 43 °C | **13.0** | 17.6 | 14.0 | D1 |

The jacket melts first, so R4 is 13.0 h at 43 °C [D2] against 12 h. With 30 % more heat leak it falls to 10.0 h [D3]; an 8 % rise in heat leak uses up the margin [D4]. R4 is **at risk**.

## E. Peltier module, cold path and heat sink (R7)

A Peltier module that is switched off conducts heat. The derived off-state conductance is 0.268 W/K for the TEC1-12703 class, 0.357 W/K for the 12704 and 0.536 W/K for the 12706 [E1]. Even the smallest is 2.9 times the whole box's heat leak [E2], which is why the thermosiphon diode (section H) is needed.

The same conductance decides which module can hold at 43 °C, because the hot side runs about 50 K above the cold side:

*Table 4. Powered hold, can at 2 °C: current, module power, COP and input power (module through a 90 % driver, plus fan and controller).*

| Module | 25 °C | 32 °C | 43 °C | Tag |
| --- | --- | --- | --- | --- |
| TEC1-12703 | 0.73 A, 3.1 W, 0.67, **4.2 W** | 1.03 A, 6.1 W, 0.45, **7.5 W** | 1.69 A, 15.9 W, 0.23, **18.4 W** | E3 |
| TEC1-12704 | 0.93 A, 3.9 W, 0.54, 5.0 W | 1.31 A, 7.6 W, 0.36, 9.2 W | 2.21 A, 21.0 W, 0.18, 24.1 W | E3 |
| TEC1-12706 | 1.34 A, 5.5 W, 0.38, 6.8 W | 1.94 A, 11.4 W, 0.24, 13.3 W | Cannot lift the load | E3 |

The TEC1-12706 named at TRL 2 cannot hold at 43 °C with this heat sink: its own back-conduction exceeds what it can pump. The **TEC1-12703 class** is chosen. At 43 °C its cold face is at 0.5 °C and its hot face at 53.8 °C [E4]; it needs 9.5 V [E5], and the sink rejects 5.2 W, 8.9 W and 19.7 W at 25, 32 and 43 °C [E6]. The sink base reaches about 53 °C at 43 °C [E7].

R7 asks for an indefinite hold up to 43 °C on 12 V or 45 W USB-C PD. The input is 18.4 W, well inside 41.4 W available from a 45 W PD source [E8], and 1.94 A from a 10 V vehicle input [E9]. The module needs 9.5 V, so a low vehicle supply of 10 V leaves little headroom for a buck driver; a buck-boost stage may be needed. The cooling side of R7 is met, but the lid pack melts after about 21 h of powered hold at 43 °C (section F), after which the top layer of the payload is at risk. R7 is **at risk**.

The driver matters. Unfiltered on/off pulse-width modulation at 12.8 V, giving the same average heat lift at 43 °C, needs a 0.79 duty and 25.6 W at the module [E10], 61 % more than smooth DC (15.9 W). The power board therefore uses a buck driver with an LC filter, not on/off PWM. CPD-PRC-001 v0.2 said PWM improves COP; that is corrected in v0.3.

## F. Off-grid hold (R5, R6)

65.3 Wh of the battery is available for cooling [F1]. While the battery runs, the module holds the can at 2 °C and the PCM stays frozen; the lid pack melts slowly, because its heat path bypasses the can. Then the PCM holds passively.

*Table 5. Battery, then PCM.*

| Ambient | Battery phase (h) | Passive phase (h) | Total (h) | With 30 % more leak (h) | Tag |
| --- | --- | --- | --- | --- | --- |
| 25 °C | 15.6 | 22.1 | 37.6 | | F2 |
| 32 °C | 8.7 | 17.8 | **26.5** | 20.1 | F2, F2b |
| 43 °C | 3.5 | 13.0 | **16.5** | 12.4 | F2, F2b |

R5 (24 h at 32 °C) and R6 (16 h at 43 °C, relaxed by CPD-DDR-001 D5) are met at the nominal heat leak and missed at +30 %: both are **at risk**. For reference, the 153.6 Wh 4S2P pack not chosen in D4 would give 18.6 h at 43 °C [F6].

In powered hold at 43 °C the lid pack absorbs a net 0.69 W [F3] and is fully melted after about 21 h [F4]. Once melted it settles near 13.8 °C [F5], with only a 12 mm air gap between it and the top layer of pens, which then sit somewhere between the liner (about 3 °C) and the pack. This is why R1 and R7 are at risk in long hot holds.

## G. Refreeze (R8)

The decided evaporator position (outer face of the PCM, CPD-DDR-001 D3) is sized here. A 90 x 60 mm plate on one end of the jacket, as drawn at TRL 2, cannot freeze a paraffin jacket that runs 200 mm around the liner: solid paraffin conducts only about 0.2 W/(m·K). The evaporator is therefore a 1.0 mm aluminium can that lines the outer face of the jacket on four sides and the floor, 0.0943 m² in contact [G1], with an 8 mm copper evaporator loop around its base. The frozen jacket is effectively 8.3 mm thick [G2], and the can wall above the loop acts as a fin with 0.69 efficiency [G3].

A time-stepped model (sensible cooling of the liquid PCM through the pouch film, then a quasi-steady freezing front, with the module current chosen each step within the 25 W cap and the −2 °C can floor) gives:

*Table 6. Jacket refreeze from 25 °C, box empty, 25 °C ambient.*

| Module | Sensible part (h) | Total (h) | Tag |
| --- | --- | --- | --- |
| TEC1-12703 | 0.9 | **5.5** | G4 |
| TEC1-12704 | 0.9 | 5.3 | G4 |
| TEC1-12706 | 0.8 | 5.5 | G4 |

Conduction through the freezing PCM alone would allow about 1.6 h [G5], so the module, not the PCM, sets the rate. The jacket meets the 8 h target.

The lid pack has no cold path to the evaporator: only the air gap and the lid gasket [G6]. The Peltier cannot refreeze it, so **R8 is not met** for the whole PCM, and the TRL 2 hold times quietly assumed a lid pack frozen some other way. Two fixes are sized for review (not adopted): an aluminium plate under the lid pack that seats on the can rim when the lid closes, which would refreeze the lid pack in about 2.3 h [G7] and add 0.12 kg [O3]; or no lid pack and a 20 mm jacket holding 1.010 kg, all actively frozen [N1], with the body 10 mm longer and wider and 10 mm lower [N2].

The battery recharges in about 6.7 h at 12 W alongside the refreeze [G8], for a total input of 40.5 W [G9], inside the 45 W PD budget.

## H. Thermosiphon: diode ratio and tilt

The loop thermosiphon conducts about 2.50 W/K forward and 0.0058 W/K in reverse (the stainless wall sections), a ratio of 431 [H1]. For comparison, bolting the chosen module to the liner would raise the box conductance to 0.359 W/K [H2] and cut the passive hold at 43 °C to 3.6 h [H3]. The thermosiphon keeps its place (CPD-DDR-001 D2).

The condenser sits 75.0 mm above the evaporator loop [H4]. The whole loop stays below the condenser for tilts up to 18° with the cooling head down [H5] and 41° with the front or back down [H7]; with the cooling head down, part of the loop stays below the condenser up to 60° [H6]. Beyond those angles the part of the loop above the condenser dries out and cooling falls; the PCM carries the load meanwhile. Whether a motorbike carrier holds within 18° on average is an open question for a lab or field test after TRL 3.

## I. Freeze fault (R2)

In normal operation the coldest surface (the can, down to −2 °C during refreeze) is separated from the liner by the PCM, and the controller stops cooling at a liner reading of 3 °C, so R2 holds. With a stuck-on driver, the module draws about 3.6 A from the 14.4 V charge rail [I4] until the hardware cut-out on the cold block opens at −5 °C [I1]. Once the PCM is fully frozen, nothing stops the liner from following the can down to about −4 °C in a cool room [I2]. The liner and payload alarms would sound, but R2 asks that no payload-contact surface fall below 1 °C even in this fault. **R2 is not met.**

A second hardware cut-out on the liner, in series with the first, fixes it. A lumped estimate of the liner after the cut-out opens (the payload and liner sharing heat with the colder frozen jacket) gives 1.2 °C for a 2 °C setting and 2.0 °C for a 3 °C setting [I3]. A 3 °C liner cut-out is proposed, awaiting Amish.

## J. Logger (R9, R11)

Sixty days of one 16-byte record per minute take 1.38 MB of the 2.10 MB flash [J1]: R9 is met on storage, and on accuracy by sensor selection. The logger and standby loads come to about 0.78 mW [J2]; with a 5 mW design allowance [J3], the 15 % reserve lasts about 96 days [J4], far beyond the 14 days of R11: met.

## K. Mass (R12)

*Table 7. Empty mass [K1].*

| Part | kg | Part | kg |
| --- | --- | --- | --- |
| Shell (PETG, printed) | 0.740 | Loop tubes (copper) | 0.089 |
| Lid cap, gasket, latches | 0.357 | Cold block (aluminium) | 0.071 |
| Handle and strap | 0.200 | Peltier module | 0.025 |
| VIP set | 0.860 | Heat sink | 0.197 |
| PCM | 0.972 | Fan and guard | 0.060 |
| PCM pouches | 0.080 | End housings (PETG, printed) | 0.404 |
| Liner (aluminium) | 0.257 | LiFePO4 cells, 4 x 32700 | 0.560 |
| Rack (PETG) | 0.083 | BMS, fuse, holder | 0.080 |
| Evaporator can (aluminium) | 0.254 | Electronics | 0.160 |
| | | Wiring and hardware | 0.150 |

The total is **5.60 kg (12.3 lb)** empty [K2, K3] and 6.28 kg with 24 pens [K4], against the relaxed target of 5.5 kg: **R12 is not met** by 0.10 kg. The evaporator can (0.25 kg), which TRL 2 did not have, is most of the growth. Thinner printed parts (3 mm shell, 5 mm lid cap, 2 mm housings) would save 0.06, 0.04 and 0.11 kg [O1], for 5.39 kg [O2]; with the lid cold plate (0.12 kg, [O3]) the case would be about 5.51 kg.

## L. Cost and battery (R14, R15)

All 16 BOM lines are priced [L1]; the total is $295 [L2] against the $300 budget set by CPD-DDR-001 D10: met, with a $5 margin and no custom PCB. The battery is 76.8 Wh [L3], under the 100 Wh airline limit: R14 is met.

## P. Foam variant (CPD-DDR-001 D7)

The documented low-cost variant replaces the VIPs with 25 mm polyurethane foam (0.024 W/(m·K)). With the same shape factors and no VIP joints, the conductance is 0.160 W/K [P1] and the passive hold at 43 °C falls to about 7.4 h [P2], so the foam variant does not meet R4. TRL 2 estimated about 7 h.

## Checks against earlier figures

*Table 8. TRL 2 figures in CPD-PRC-001 v0.2 and the README, checked against this note. The docs are corrected in v0.3.*

| Quantity | TRL 2 | TRL 3 | Tag |
| --- | --- | --- | --- |
| Overall conductance | 0.11 W/K | 0.091 W/K | B9 |
| PCM | 1.06 kg, 191 kJ | 0.972 kg, 175 kJ | C2, C3 |
| Payload volume | about 1.2 L | 1.36 L | A2 |
| Passive hold 25 / 32 / 43 °C | 24 / 18 / 12.7 h | 24.7 / 18.3 / 13.0 h | D1 |
| Input power to hold 25 / 32 / 43 °C | 4.7 / 8.1 / 17.4 W | 4.2 / 7.5 / 18.4 W | E3 |
| Battery then PCM 25 / 32 / 43 °C | 38 / 26 / 16 h | 37.6 / 26.5 / 16.5 h | F2 |
| Refreeze | about 5 h (text), about 6 h (table) | 5.5 h, jacket only | G4 |
| Heat rejected 25 / 32 / 43 °C | 6 / 10 / 21 W | 5.2 / 8.9 / 19.7 W | E6 |
| Heat sink temperature at 43 °C | 55 to 65 °C | about 53 °C | E7 |
| Peltier off-state conductance | 0.3 to 0.5 W/K | 0.27 to 0.54 W/K | E1 |
| Peltier module | TEC1-12706 | TEC1-12703 class | E3 |
| PWM "for better COP" | stated | smooth DC; on/off PWM costs 61 % more | E10 |
| Battery recharge | about 3 h at 25 W | about 6.7 h at 12 W alongside refreeze | G8 |
| Logger reserve | weeks | about 96 days | J4 |
| Log storage, 60 days | about 1.4 MB | 1.38 MB | J1 |
| Size | 370 x 215 x 205 mm | 368 x 214 x 207 mm | A6 |
| Mass empty | 5.2 kg | 5.60 kg | K2 |
| Parts cost | $280 | $295 | L2 |
| Warm-payload pull-down | about 3.7 h | not recomputed; removed from the precis, which keeps the advice to load the payload pre-cooled | |

## Results

*Table 9. Requirements against this note. Status: met, at risk, not met, or not verifiable at TRL 3.*

| ID | Target (CPD-REQ-001 v0.3) | Value | Status |
| --- | --- | --- | --- |
| R2 | No payload-contact surface below 1 °C, including a stuck-on driver | Normal: met. Fault: liner near −4 °C with the −5 °C block cut-out [I2] | **Not met** |
| R8 | Refreeze a fully melted PCM in 8 h or less at 25 °C | Jacket 5.5 h [G4]; lid pack has no cold path [G6] | **Not met** |
| R12 | 5.5 kg or less empty (relaxed) | 5.60 kg [K2] | **Not met** |
| R1 | 2 to 8 °C at the payload probe | Can at 2 °C, liner 2 to 5 °C; lid path warms the top layer in long powered hold at 43 °C [F5] | At risk |
| R4 | 12 h or more at 43 °C, no power | 13.0 h; 10.0 h at +30 % leak [D2, D3] | At risk |
| R5 | 24 h or more at 32 °C, battery then PCM | 26.5 h; 20.1 h at +30 % leak [F2] | At risk |
| R6 | 16 h or more at 43 °C, battery then PCM (relaxed) | 16.5 h; 12.4 h at +30 % leak [F2] | At risk |
| R7 | Hold indefinitely up to 43 °C on 12 V or 45 W USB-C PD | 18.4 W input [E8]; lid pack melts after about 21 h [F4] | At risk |
| R3 | 1.0 L or more; 20 or more pens up to 170 mm | 1.36 L; 24 pens; up to 172 mm [A2 to A5] | Met |
| R9 | ±0.5 °C, log every 1 min, 60 days, CSV export | 1.38 MB of 2.10 MB [J1]; accuracy by selection | Met |
| R11 | Logger runs 14 days after cooling stops | About 96 days [J4] | Met |
| R13 | Fits 400 x 250 x 250 mm | 368 x 214 x 207 mm [A6] | Met |
| R14 | Battery 100 Wh or less | 76.8 Wh [L3] | Met |
| R15 | Parts $300 or less; no custom PCB | $295 [L2]; modules on perfboard | Met |
| R17 | "Research prototype, not a medical device" on box, start screen and logs | By design | Met |
| R10 | Alarm logic and thresholds | Design intent only; no firmware sketch exists at TRL 3 | Not verifiable at TRL 3 |
| R16 | IP54 bays; 0.5 m drop while loaded | Needs a test | Not verifiable at TRL 3 |

Counts: 7 met, 5 at risk, 3 not met, 2 not verifiable at TRL 3.

## Limits of this note

- All values are paper estimates. The heat leak (joint ψ, aged VIP conductivity), the thermosiphon resistance, the heat sink resistance and the PCM's usable latent heat inside 2 to 8 °C are the largest uncertainties, in that order.
- The Peltier model uses constant properties derived from datasheet maxima. Real modules vary by maker.
- The lid pack and payload temperatures in long powered holds come from a two-node estimate; stratification and contact with the rack are not modelled.
- No solar gain is included. A carrier in direct sun would see more heat than the 43 °C shaded case.
