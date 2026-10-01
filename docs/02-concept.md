---
doc_id: CPD-PRC-001
title: ColdPod design precis
project: ColdPod
doc_type: Design precis
version: "0.7"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, first-order numbers, design choices, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions (CPD-DDR-001); numbers replaced by CPD-CAL-001; evaporator can, loop thermosiphon and TEC1-12703 class sized; smooth DC drive
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Lid cold plate, liner cut-out at 3 °C, thinner printed parts and buck-boost driver; numbers from CPD-CAL-001 v0.2
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish; budget $310, R15 met
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Constructable design (CPD-DDR-003, Draft, open for Amish's review); numbers from CPD-CAL-001 v0.4; build plan CPD-BLD-001 and decisions register CPD-DEC-001 added
- version: "0.7"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# ColdPod design precis

ColdPod is a carry case about the size of a lunch cooler (366 x 220 x 207 mm) that holds 1.37 L of insulin or vaccines (24 pens) at 2 to 8 °C. The payload sits in an aluminium liner wrapped in a phase-change material (PCM) that melts at 5 °C, inside 25 mm vacuum-insulated panels. A Peltier module freezes the PCM from a 12 V socket, a solar panel or a USB-C charger, and a small LiFePO4 battery keeps it running on the road. A two-phase loop thermosiphon connects the two and carries heat in one direction only, so a stopped Peltier does not leak heat back in. A logger records the payload temperature every minute and raises alarms. An aluminium cold plate tray holding the lid PCM pack lands on the evaporator can's rim flange when the lid closes, so the Peltier freezes all the PCM, and a second hardware cut-out on the liner stops a stuck-on driver from freezing the payload. Version 0.6 describes the constructable design of CPD-DDR-003 (Draft, open for Amish's review), in which every part can be made and fixed; the prototype build plan is CPD-BLD-001 and open decisions are in the register CPD-DEC-001. The TRL 3 calculations (CPD-CAL-001 v0.4) give about 13.3 h with no power at 43 °C, 27.3 h off-grid at 32 °C and 16.7 h off-grid at 43 °C, for $308 in parts and 5.70 kg empty. The hold times meet their targets with thin margins. The design misses two targets: refreezing all the PCM takes 8.0 h, a few minutes over 8 h (R8), and the mass is 0.20 kg over (R12). Options for these are awaiting Amish. The parts cost is within the $310 budget that Amish approved on 2026-09-26 (R15 met).

![Hero render](../media/hero.png)

*Figure 1. ColdPod on a table, with a phone for scale. Cooling head on the right end, battery and electronics bay with the e-paper display on the left end. Rendered from the parametric model `cad/src/model.py`.*

## How it works

1. **Charge the cold.** At a clinic, in a vehicle or under a solar panel, the Peltier module runs at up to 25 W and freezes the PCM jacket through the thermosiphon and the aluminium evaporator can around it. The lid PCM pack sits in a 1.5 mm aluminium cold plate tray that lands on the can's rim flange when the lid closes, so it freezes through the can too. The same input charges the battery at about 12 W. A fully melted charge refreezes in about 8.0 h (the jacket in 6.8 h). The case works best if the payload goes in already cold from a refrigerator.
2. **Carry.** On the road, the controller runs the Peltier from the battery only as hard as needed to hold the evaporator can at about 2 °C, so the PCM stays frozen, and turns it off when the battery reaches 15 % so that the logger always has a reserve. A buck-boost driver feeds the module smooth DC from any input between 10 and 20 V; on/off PWM would cost about 60 % more power at 43 °C. The lid pack stays frozen on its plate.
3. **Hold passively.** When the battery is flat or the user switches cooling off, the PCM absorbs the heat that leaks through the walls; the plate lets the jacket and lid pack share the load. Because it melts at 5 °C, it cannot pull the payload below freezing the way water ice can.
4. **Watch.** A buffered probe among the payload, a liner probe, a cold-block probe and an ambient sensor are read every minute. The payload probe is logged with a timestamp on the controller's flash memory for 60 days or more.
5. **Alarm.** The display shows current, minimum and maximum temperature and time left. A buzzer, an LED and a phone notification warn after 10 min outside 2 to 8 °C, alarm at once at 0 °C or lower, and flag low battery, a failed sensor or a lid left open. The owner exports the log as a CSV file over Bluetooth Low Energy or USB. Nothing goes to the cloud.

![Heat flow](../media/flow.png)

*Figure 2. Heat flow in powered hold at 32 °C ambient, can at 2 °C. All values are estimates from CPD-CAL-001: 0.092 W/K overall heat leak, TEC1-12703 class module at a coefficient of performance (COP) of 0.45, fan 0.6 W.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 4.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Outer shell | 3D-printed PETG or ASA tub, 3 mm walls, 261 x 196 x 164.5 mm, with printed pads and towers carrying threaded inserts for every outside fixing, and pipe and cable slots closed by printed fillers | Protects the VIPs from knocks and punctures; no fixing passes through a wall (CPD-DDR-003) |
| 2 | Lid and lid cold plate | Printed 5 mm cap with EPDM gasket and a 25 mm VIP plug; 1.5 mm aluminium cold plate tray, 204 x 139 x 16.5 mm, holding the lid PCM pack and bonded to the plug | Two front draw latches; lid switch for the lid-open alarm; the tray lands on the can's rim flange so the lid pack freezes and stays frozen |
| 3 | Bail handle and strap | Folding bail handle, padded shoulder strap | Rated 10 kg or more |
| 4 | Vacuum-insulated panels | Seven panels, 25 mm, fumed silica core, ordered to size, and a 28 mm foam strip | VIPs cannot be cut or pierced; the heat-pipe crossing is a foam-filled gap between panels |
| 5 | PCM packs | About 0.94 kg of organic PCM melting at 5 °C (Rubitherm RT 5 HC class) in sealed HDPE pouches: a 0.67 kg jacket on four sides and the floor inside the evaporator can, and a 0.27 kg pack in the lid tray | Organic paraffins are stable for thousands of cycles ([PATH PCM study](https://media.path.org/documents/DT_pcm_summary_rpt1.pdf)) |
| 6 | Liner and rack | 1.5 mm aluminium can, 175 x 110 x 80 mm outside (172 x 107 x 78.5 mm inside), with a removable printed rack for 24 pens in four layers of six; stands on printed feet with a printed collar, never touching the can | Spreads cold evenly around the payload |
| 7 | Evaporator can and thermosiphon | 1.0 mm aluminium can lining the outer face of the PCM jacket (four sides and floor); two-phase loop thermosiphon: 8 mm copper evaporator loop bonded into the bottom corner of the can, vapour riser and liquid return at the +X end, stainless sections through the wall, aluminium cold block 81 mm above the loop, held to the shell by a printed frame | One-way thermal link (design choices 2 and 3); sized in CPD-CAL-001, section G |
| 8 | Peltier module | 40 x 40 mm, 127 couples, Imax about 3 A (TEC1-12703 class) | The TEC1-12706 cannot hold at 43 °C: its off-state conduction is too high (CPD-CAL-001, section E) |
| 9 | Heat sink and fan | Finned aluminium sink, 80 x 80 x 30 mm, 0.50 K/W or better with a 70 mm, 12 V fan and a finger guard | Rejects about 8.9 W at 32 °C and 19.7 W at 43 °C |
| 10 | End housings | Printed cooling head (+X end) and battery and electronics bay (−X end), 2 mm walls, vented | Keep the heat source and the battery outside the insulation |
| 11 | Battery | LiFePO4, 4S1P 32700 cells, 12.8 V 6 Ah (76.8 Wh), BMS and fuse | Below the 100 Wh airline limit |
| 12 | Power board | USB-C PD sink (20 V), 12 V input (10 to 15 V) with reverse-polarity protection, LiFePO4 charger, buck-boost Peltier driver with an LC filter, fan driver; the cold-block and liner cut-outs wired in series in the Peltier supply | Off-the-shelf modules on perfboard; no custom PCB |
| 13 | Logger controller | nRF52840 module with real-time clock and 2 MB flash | Bluetooth Low Energy link to a phone |
| 14 | Temperature sensors and liner cut-out | Glycol-buffered payload probe, liner probe, cold-block probe, ambient sensor; bimetal cut-out on the liner opening at 3 °C | Digital sensors with ±0.5 °C or better accuracy; the cut-out works without firmware |
| 15 | Display and alarm | 2.13 in e-paper, buzzer, red and green LED | E-paper keeps the last reading visible with no power |

Item 16 (wiring, fasteners, latches and consumables) is in the BOM but not modelled.

![Cutaway](../media/cutaway.png)

*Figure 3. Section looking from the front. From the inside out: payload (white pens) in the rack and liner (6), PCM jacket and lid pack (5, blue) with the evaporator can and its loop (7, copper; the loop shows as two circles at the base), the lid cold plate (2) under the lid pack, VIPs (4, light grey) and shell (1). The pipes (7) cross the right wall to the cold block, Peltier (8) and heat sink (9) in the cooling head. The battery (11) and logger (13) are in the left bay.*

## Numbers at TRL 3

All values come from the calculation note CPD-CAL-001 (`docs/04-calcs/01-sizing.md`), which states every assumption; the tags in brackets point to lines of its script, `docs/04-calcs/sizing.py`. They are paper estimates. The main inputs are an aged VIP conductivity of 0.007 W/(m·K) with explicit joint and edge losses, 180 kJ/kg of usable latent heat inside 2 to 8 °C for the PCM ([Rubitherm RT range](https://www.rubitherm.eu/en/productcategory/organische-pcm-rt)), a Peltier model derived from datasheet maxima (single-stage modules typically reach a COP of 0.3 to 0.7, [ThermalLM](https://thermallm.com/cop-of-a-thermoelectric-cooler-tec/)), and 65.3 Wh of the 76.8 Wh battery available for cooling.

Table 2. Hold times, charging, size, mass and cost.

| Quantity | Value | Basis | Requirement |
| --- | --- | --- | --- |
| Payload | 1.37 L; 24 insulin pens in four layers of six, up to 172 mm long | Liner less rack and probe [A2, A3] | R3 met |
| Heat leak | 0.093 W/K: 1.86 W at 25 °C, 2.50 W at 32 °C, 3.53 W at 43 °C | Langmuir shape factor, joints, foam strip, pipes, wires [B9, B10] | |
| PCM | 0.935 kg, 168 kJ (46.8 Wh) usable | Jacket 0.670 kg, lid pack 0.265 kg, measured on the model [C2, C3] | |
| Passive hold, PCM only | 25.2 h at 25 °C, 18.7 h at 32 °C, **13.3 h at 43 °C** | Jacket and lid pack pooled through the lid cold plate [D1, D2] | R4 at risk (10.2 h at +30 % leak) |
| Input power to hold | 4.2 W at 25 °C, 7.6 W at 32 °C, 18.8 W at 43 °C | TEC1-12703 class, can at 2 °C, buck-boost driver [E3] | R7 met |
| Battery hold, then PCM | 15.4 + 25.2 = 40.6 h at 25 °C; 8.6 + 18.7 = **27.3 h at 32 °C**; 3.5 + 13.3 = **16.7 h at 43 °C** | 65.3 Wh, then the PCM [F2] | R5 and R6 at risk |
| PCM refreeze from melted | **8.0 h** (8.03 h) for all the PCM at 25 °C (jacket 6.8 h, lid pack 8.0 h) | Time-stepped model, 25 W to the module [G4] | R8 **not met** (8 h) |
| Battery recharge | about 6.7 h at 12 W alongside the refreeze | 45 W USB-C PD budget [G8] | |
| Heat rejected at the heat sink | 5.3 W at 25 °C, 9.0 W at 32 °C, 20.1 W at 43 °C; sink base about 53 °C at 43 °C | Heat lifted plus module input [E6, E7] | Fan needed |
| Thermosiphon | Forward 2.50 W/K, reverse 0.0058 W/K; full function to 19° of tilt with the cooling head down | [H1, H5] | |
| Freeze fault | Liner settles near 2.0 °C after a stuck-on driver, with the 3 °C liner cut-out | Lumped estimate [I5] | R2 met |
| Logger reserve | about 96 days | 15 % of 76.8 Wh at a 5 mW allowance [J4] | R11 met |
| Log storage | 1.38 MB for 60 days | 1 record per minute, 16 bytes [J1] | R9 met on 2 MB flash |
| Size | 366 x 220 x 207 mm (14.4 x 8.7 x 8.1 in) overall | Handle up [A6] | R13 met |
| Mass, empty | **5.70 kg (12.6 lb)** | Model volumes and densities [K2]; the fixings and parts that make the design buildable add about 0.17 kg (CPD-DDR-003) | R12 **not met** (5.5 kg) |
| Parts cost | **$308** | `bom/bom.csv` [L2] | R15 within the value-engineering target ($310) |

## Key design choices

Amish decided choices 1 to 9 on 2026-09-25, going with the recommendation in each case (CPD-DDR-001). The options are kept here for the record.

1. **PCM at 5 °C instead of water ice (decided, D1).** Water ice stores about 334 kJ/kg, nearly twice as much, but a frozen ice pack sits at 0 °C or below and is a known cause of vaccine freezing ([Hanson et al., 2017](https://www.sciencedirect.com/science/article/pii/S0264410X16309471)). A 5 °C PCM keeps the whole payload space inside the window. Options were (a) 5 °C organic PCM; (b) water with a conditioning step; (c) a 3 °C PCM. Decision: (a).
2. **A thermosiphon between the Peltier and the PCM (decided, D2).** A Peltier module that is switched off conducts heat well: 0.27 W/K for the chosen module, about three times the whole box's heat leak. Bolted straight to the liner, it would cut the passive hold at 43 °C to about 3.6 h. A gravity thermosiphon, with its condenser above its evaporator, only carries heat upward and out, so it acts as a thermal diode (forward to reverse ratio about 430). Options were (a) thermosiphon; (b) a mechanical disconnect that lifts the cold block away when power is lost; (c) direct mounting. Decision: (a), with (b) as the fallback if the thermosiphon cannot be made reliable at this size. TRL 3 sizes it as a two-phase loop.
3. **Evaporator on the outer face of the PCM, not on the liner (decided, D3).** Keeps the coldest surface (down to −2 °C during refreezing) separated from the payload by the PCM, which supports R2. At TRL 3 this is sized as an aluminium can lining the outer face of the jacket, because a small plate cannot freeze a paraffin jacket that wraps the liner.
4. **LiFePO4, 76.8 Wh (decided, D4).** LiFePO4 tolerates heat better than other lithium-ion chemistries and 76.8 Wh stays under the 100 Wh airline limit. The rejected 4S2P option (153.6 Wh, about $30 more and 0.6 kg heavier) would give about 18.6 h at 43 °C off-grid.
5. **R6 redefined (decided, D5).** Accept about 16 h at 43 °C off-grid and run from a vehicle 12 V socket or a solar panel on long hot trips, rather than a larger battery or 35 mm VIPs with 1.6 kg of PCM (about 400 mm long and over 6 kg). Revisit after field data on real trip temperatures.
6. **Vacuum-insulated panels instead of foam (decided, D7).** Polyurethane foam of the same thickness (about 0.024 W/(m·K)) gives 0.161 W/K rather than 0.092 W/K, so the passive hold at 43 °C would drop from 13.3 h to about 7.6 h (CPD-CAL-001, P1 and P2), but it would save about $45 and some mass. VIPs are used, with a foam version documented as a low-cost variant.
7. **Local alarms and Bluetooth Low Energy only (decided, D8).** No cellular or LoRa radio in the first build (either would add $20 to $40 and more power).
8. **Alarm thresholds (decided, D9).** Warn after 10 min outside 2 to 8 °C; alarm at once at 0 °C or lower on the payload probe; alarm if the liner probe reaches 1 °C (an early freeze warning); adjustable per product.
9. **Value-engineering target (decided, D10).** The target is $310 (a hypothetical control target, not a limit; $300 at D10, $310 after CPD-DDR-002 item 16); the estimated parts cost of the constructable design is $308, $2 under the target.

Amish decided the TRL 3 review items on 2026-09-25, again going with the recommendation in each case (CPD-DDR-002):

10. **Lid cold plate (decided, DDR-002 item 2).** A 1.5 mm aluminium plate under the lid PCM pack, whose rim seats on the evaporator can rim when the lid closes (about $5 and 0.12 kg). It gives the lid pack a cold path, so the Peltier refreezes all the PCM and the lid pack stays frozen in long powered holds. The other options were no lid pack with a 20 mm jacket, or conditioning the lid pack in a refrigerator. The gasket must still seal with the plate in place; that is a check for a built lid.
11. **Liner cut-out at 3 °C (decided, DDR-002 item 3).** A bimetal cut-out on the liner, in series with the −5 °C cold-block cut-out in the Peltier supply (about $3). After a stuck-on driver fault the liner settles near 2.0 °C.
12. **Thinner printed parts (decided, DDR-002 item 4).** Shell 3 mm (was 4 mm), lid cap 5 mm (was 8 mm), end housings 2 mm (was 3 mm), saving about 0.21 kg. Confirming the mass by weighing is TRL 4 work, on hold.
13. **Evaporator can and loop thermosiphon confirmed (decided, DDR-002 item 5).** As sized in CPD-CAL-001: a 1.0 mm aluminium can around the jacket fed by an 8 mm copper loop. The mechanical disconnect (choice 2b) stays ready as the fallback if a maker cannot charge the loop.
14. **Peltier class and drive confirmed (decided, DDR-002 item 6).** TEC1-12703 class module, smooth DC through an LC filter, heat sink of 0.50 K/W or better with the fan.
15. **Buck-boost driver (decided, DDR-002 item 7).** The Peltier driver can raise the module voltage above a low vehicle input (10 V), rather than narrowing the 12 V input range to 11 to 15 V (about $4 more).
16. **Value-engineering target of $310 (decided by Amish, DDR-002 item 8 and N3).** A VIP quote is to come before any purchase decision; purchasing is TRL 4 work, on hold.

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with BOM numbers, from the parametric model. The payload pens rise with the liner (6); the evaporator can, loop and cold block (7) sit between the VIPs (4) and the PCM (5).*

## Safety

> **Safety:** ColdPod is a research and educational prototype. It is not a medical device, is not WHO-prequalified and has not been cleared or approved by any regulator. Do not use it as the only protection for vaccines, insulin or other medicines. Follow national immunization program and manufacturer storage instructions, and use a qualified carrier and a calibrated logger for real products.

> **Safety:** The LiFePO4 pack stores 76.8 Wh. Use it only with its BMS and fuse, charge it only between 0 and 45 °C (the controller must block charging outside that range), and never charge a damaged, swollen or wet pack. The battery sits in its own vented bay outside the insulation, away from the Peltier's hot side.

> **Safety:** The PCM is a paraffin, which is combustible. It stays sealed in HDPE pouches, separated from the battery bay by the VIPs and the shell. Replace any leaking pouch; paraffin can also soften some plastics ([PATH PCM study](https://media.path.org/documents/DT_pcm_summary_rpt1.pdf)).

- **Hot surfaces.** At 43 °C ambient the heat sink base reaches about 53 °C (estimate, CPD-CAL-001, E7). It is enclosed by the vented cooling head, and the vents must not be blocked, covered or placed against skin or a bag.
- **Moving parts.** The fan has a finger guard inside the cooling head grille.
- **Electrical.** All voltages are 20 V DC or less. There are no mains-voltage parts in the box. Inputs are fused and protected against reverse polarity.
- **Freezing fault.** A stuck-on Peltier driver is the main way to freeze the payload. Two hardware thermostats in series cut power to the Peltier independent of the firmware: one on the cold block at −5 °C and one on the liner at 3 °C. CPD-CAL-001 (section I) shows that the cold-block cut-out alone would let the liner follow the can down to about −4 °C; with the liner cut-out the liner settles near 2.0 °C. The liner and payload probes also raise alarms. The lid cold plate reaches −2 °C only while refreezing, which is done with the box empty; it touches no payload.
- **Condensation.** Water condenses on the cold block and pipes. The cooling head drains outward and the electronics are conformal-coated.
- **VIP damage.** A punctured VIP loses most of its insulation value without any visible change. The shell protects the panels, and a rising Peltier duty cycle should trigger a service warning.
- **Lifting.** About 6.2 kg when loaded; carry with the strap across the body.

## Open questions after TRL 3

Open decisions and items to confirm are kept in the design decisions register, [CPD-DEC-001](06-design-decisions.md). In short:

- Accepting the design-for-construction changes (CPD-DDR-003), the larger mass miss (R12, 5.70 kg against 5.5 kg) and the refreeze miss (R8, 8.0 h against 8 h) are awaiting Amish.
- Does the lid gasket still seal with the tray landed on the can flange, and does the tray seat give about 0.5 K/W?
- Can the loop thermosiphon be made and charged reliably at this size, with which working fluid, and does a motorbike carrier stay within about 19° of tilt with the cooling head down? If not, the mechanical disconnect (choice 2b) is the fallback.
- Confirm the off-state conductance and real COP of the chosen module with the chosen heat sink, and the sink's resistance with the fan.
- Confirm the VIP supplier, panel sizes, aged conductivity and edge losses; joints and edges are about 45 % of the heat leak.
- Confirm the usable latent heat of the PCM between 2 and 8 °C, its supercooling and its behavior over many cycles.
- Where to place the payload probe so that it represents the warmest pen, not the average; the build places it across the top layer at the cooling end.
- Validate trip profiles, loads, alarm behavior and price with users through a partner (partner choice open, awaiting Amish).

Drawings and media: [prototype build plan CPD-BLD-001](05-build-plan.md), [general arrangement CPD-DWG-001](../cad/drawings/CPD-DWG-001.pdf), [concept blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
