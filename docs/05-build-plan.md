---
doc_id: CPD-BLD-001
title: ColdPod prototype build plan
project: ColdPod
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan; design made constructable (CPD-DDR-003, Draft, open for Amish's review)
---

# ColdPod prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

ColdPod is a research and educational prototype, not a medical device. Never use a prototype built to this plan to carry real vaccines or insulin.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The cooling head is at the right-hand end, the battery bay at the left.*

The prototype is one ColdPod carry case, 366 x 220 x 207 mm with the handle up. From the inside out it is a printed rack of 24 insulin pens in an aluminium liner; a jacket of sealed pouches of phase-change material (a paraffin that melts at 5 °C) inside an aluminium evaporator can; seven vacuum-insulated panels (VIPs); and a 3D-printed shell. A copper loop bonded to the bottom of the can carries heat out to an aluminium cold block, a Peltier module and a finned heat sink with a fan in a printed cooling head at the right-hand end; the battery, logger and display sit in a printed bay at the left-hand end. Figure 1 shows the 23 component groups in the order you make or fit them. Fifteen are made: the shell, the evaporator can, the copper loop, the cold block, three slot fillers, the liner, its feet and collar, the rack, the block frame, the two end housings, the cell cradle, the cable duct cover, the lid cold plate tray and the lid cap. Everything else is bought: the VIPs (to size), the PCM pouches, the Peltier module, heat sink and fan, the battery cells, the electronic modules, the handle and the latches. The work is 3D printing, simple sheet-metal work done by a local shop, tube bending, brazing and charging the loop (by a refrigeration technician), and wiring bought modules. The parts cost about $308, from the bill of materials.

> **Safety:** The prototype holds a 76.8 Wh lithium iron phosphate battery, about 0.94 kg of combustible paraffin in sealed pouches, a sealed refrigerant loop under pressure and a heat sink that reaches about 53 °C. Keep the battery fuse out until section 6 says otherwise. Brazing and charging the loop are done by a refrigeration technician before any plastic, VIP or PCM is near it. A punctured VIP loses its insulation without any visible sign: never cut, drill or press a sharp tool against one.

## 2. What changed to make it buildable

The concept showed what ColdPod does; many of its parts had no fixing or could not be put together as drawn. Each change below keeps what ColdPod does. All of them are recorded in decision record CPD-DDR-003, open for Amish's review. One rule drives most of them: there is a VIP behind every wall of the shell, so no screw, rivet or drill may pass through a shell wall, and every outside fixing lands on a printed pad or tower with a threaded insert.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Payload probe | A probe standing in a corner of the liner, overlapping the pens | A 10 x 40 mm vial lying across the top layer of pens at the cooling end (Figure 15) | Keeps all 24 pens |
| Copper loop | A ring floating in the PCM, touching nothing | The ring bonded into the bottom inside corner of the can (Figure 6) | The can becomes the evaporator it was meant to be |
| Risers and pass-throughs | A right-angle turn inside a 14 mm gap; round holes in the can and shell | Bends of 17.5 mm radius inside a taller foam strip; slots open at the rim, closed by printed fillers (Figure 8) | A one-piece sealed loop can be bent, charged and lowered in |
| Cold block | No passage and no joint to the tubes | Tube sockets, a drilled passage and a charge stub, joined by aluminium-to-copper brazing (Figure 9) | Makes a sealed condenser |
| Peltier stack | Hung on the copper tubes | A printed frame holds the block to two towers on the shell; two screws clamp the module (Figure 10) | The shell, not the tubes, carries the stack |
| End housings, handle, latches | No fixings | Printed pads with threaded inserts on the shell; ears on the housings (Figures 3 and 19) | No screw may pass through a VIP wall |
| Liner and lid plate | Liner resting on a pouch; a flat lid plate on a 1 mm can edge, not fixed to the lid | Liner on printed feet and a collar; a 5 mm rim flange on the can; a folded lid tray bonded to the lid plug (Figures 14 and 26) | Location, a real landing for the lid tray, and a lid that lifts off as one |
| VIPs | One solid box | Seven panels bought to size (Figure 4) | VIPs cannot be cut |
| Electronics | Floating in the housings | Standoffs, a cell cradle, a display window | Fixings for bought modules |
| Condensation | Would drip on the power board | A drip tray and drain tube (Figure 17) | The cooling head drains outward |
| Cables | No route out of the cavity or between the two ends | Grommets at the cooling end and a duct cover along the back (Figure 24) | Every lead has a path |

The case is 8 mm wider (the handle pivots stand on pads) and weighs about 5.70 kg empty, against 5.53 kg for the concept.

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Front" is the face with the latches; "left" and "right" are as seen from the front, so the cooling head is on the right. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Outer shell

![Figure 2. Making sketch of the outer shell](../cad/drawings/CPD-DWG-101.png)

*Figure 2. Outer shell making sketch (CPD-DWG-101).*

**What it is and what it is made from.** The open-topped tub that protects the VIPs and carries every outside fixing. PETG or ASA, 3D printed with four perimeters and 25 % infill, 261 x 196 x 164.5 mm outside the walls, 3 mm walls and floor.

**How to make it.**

1. Print the tub open side up on a printer with a bed of at least 300 x 300 mm and 180 mm of height. Let it cool on the bed.
2. Check that the right-hand end has two pipe slots 10 wide, 25 each side of the centre, and a cable slot 6 wide, 40 toward the front. Each is open at the rim and ends in a half-round 114 up from the bottom.
3. Check the printed pads: four on each end face (14 wide, 16 tall, 4 proud, 89 each side of centre, 40 and 145 up); two towers 10 x 10 x 10 on the right-hand end (44 each side of centre, 126 up); a round pad 20 across at the middle of the front and back (136 up) for the handle; two pads on the front (72 each side of centre, 142 to 158 up) for the latches.
4. Set the threaded inserts with a soldering iron and an insert tip: one M3 insert in each end pad and tower, one M5 insert in each handle pad, two M3 inserts in each latch pad. Do this now, before any VIP is near the shell.
5. Clean out any stringing inside; the inside faces must be smooth and flat for the VIPs.

**How it fits the parts next to it.** The VIPs fill it exactly (section 3.2). The cooling head and battery bay screw to the end pads (Figure 19), the block frame to the towers (Figure 10), the handle and latches to their pads:

![Figure 3. Joint 7: handle pivot and latch on their pads](05-build-plan/joint-07.png)

*Figure 3. The handle arm and the latch drawn pulled off their pads. The pivot is one M5 screw into the pad's insert; the latch takes two M3 screws.*

**Check before moving on.** The inside is 255 x 190, square, within 0.5 mm. Every insert sits flush and square, and no insert has pushed through the inside of a wall.

### 3.2 Vacuum-insulated panels (bought to size)

![Figure 4. The seven VIP panels and the foam strip](05-build-plan/vip-panels.png)

*Figure 4. The seven panels, all 25 mm thick, and the foam strip that fills the gap where the pipes cross.*

**What they are.** Fumed silica panels in metallized film, ordered to size from a VIP maker: floor 255 x 190; front and back 255 x 136.5 tall; left end 140 x 136.5; right end lower 140 x 68 and upper 140 x 40.5; lid plug 204 x 139. Order them to plus 0, minus 1 mm. Between the two right-end panels is a 28 mm strip of polyurethane foam, cut on the bench round the pipes and the cable (step 5).

**How they fit.** Butt jointed, edge to edge, on strips of acrylic foam tape: the floor on the shell floor, the front and back on the floor along the full length, the two ends between them. Store them flat in their packaging until step 1, away from tools.

**Check before moving on.** No panel has a soft spot or a wrinkled, puffy film (a sign it has lost its vacuum).

### 3.3 Evaporator can

![Figure 5. Making sketch of the evaporator can](../cad/drawings/CPD-DWG-102.png)

*Figure 5. Evaporator can making sketch (CPD-DWG-102).*

**What it is and what it is made from.** The aluminium box that holds the PCM pouches and spreads the cold from the loop over the whole jacket. Aluminium sheet 1.0 mm, 5052 or 3003, 205 x 140 x 95 mm outside.

**How to make it.** Have a sheet metal shop do steps 1 to 3.

1. Fold an open box from one cross-shaped blank and TIG weld the four vertical corners.
2. In the right-hand wall, cut two slots 9 wide, 25 each side of the centre, open at the rim and running down to 67.5 above the floor; drill a 6 mm hole 40 toward the front and 86 up for the sensor cable.
3. Fold a 5 mm flange inward all round the rim, last. It must be flat within 0.3 mm: the lid tray lands on it.
4. Deburr every edge and fit a grommet in the cable hole; a sharp edge would cut a pouch.

**How it fits the parts next to it.** It stands on the VIP floor with its walls against the VIP walls. The loop lies in its bottom corner:

![Figure 6. Joint 1: the loop in the corner of the can](05-build-plan/joint-01.png)

*Figure 6. Cut on the centre line at the right-hand end. The tube touches the can floor and wall and is bonded along its length.*

**Check before moving on.** Inside 203 x 138, square; the rim flange lies flat on a table.

### 3.4 Loop thermosiphon

![Figure 7. Bending sketch of the loop thermosiphon](../cad/drawings/CPD-DWG-103.png)

*Figure 7. Loop thermosiphon bending sketch (CPD-DWG-103).*

**What it is and what it is made from.** The one-way heat path: a sealed copper circuit in which a working fluid boils in the ring at the bottom of the can, rises as vapour, condenses in the cold block and runs back down as liquid. Soft copper refrigeration tube 8 x 0.5 mm.

**How to make it.** Bending is bench work; brazing, leak testing and charging are for a refrigeration technician (safety stops S1 and S2).

1. Bend the ring: a rectangle 195 x 130 on the tube centre line with 25 mm corner bends, the two ends joined with a coupler in the middle of the left-hand run.
2. Fit two tees in the right-hand run, 25 each side of the centre.
3. Bend two risers: straight up 63.5 from the tee, then a 90° bend of 17.5 mm radius (a lever bender for 8 mm tube) toward the right; the tail ends 33 beyond the outside of the can.
4. Braze the coupler, tees and risers with silver alloy under a nitrogen purge. Cap the open tails.
5. Lower the ring into the can (step 2) and bond it into the bottom corner with thermally conductive epoxy, touching floor and wall all round.

**How it fits the parts next to it.**

![Figure 8. Joint 2: riser through the can slot, foam strip and shell slot](05-build-plan/joint-02.png)

*Figure 8. Cut through a riser, seen from the front. The bend runs through the can's slot into the foam strip, clear of the lower VIP panel, and the tail enters the cold block's socket.*

The ring sits in the can's corner; each riser drops down its slot in the can and, later, its slot in the shell. The tails end in the cold block's sockets.

**Check before moving on.** The ring lies flat on a table within 1 mm; both tails are level, 50 apart, and stand 33 beyond the can.

### 3.5 Cold block

![Figure 9. Making sketch of the cold block](../cad/drawings/CPD-DWG-104.png)

*Figure 9. Cold block making sketch (CPD-DWG-104).*

**What it is and what it is made from.** The condenser of the loop and the cold face for the Peltier module. Aluminium 6061, 10 x 60 x 44 mm.

**How to make it.**

1. Mill the block square; lap the front face (the Peltier side) flat within 0.05 mm.
2. In the back face, drill two tube sockets 8.1 mm, 5 deep, 25 each side of the centre, 10 up from the bottom edge.
3. From the back-side end face, drill a 6 mm passage 5 mm in from the back face and 10 up, through both sockets.
4. In the front face, drill and tap two M3 holes 8 deep, 24.5 each side of the centre, 22 up.
5. The technician brazes the loop tails into the sockets and a 6 mm copper charge stub into the passage mouth with aluminium-to-copper brazing rod, leak tests the loop with dry nitrogen, evacuates and charges it, then pinches the stub shut and brazes the end (step 3).

**How it fits the parts next to it.**

![Figure 10. Joint 3: cold block, Peltier module, frame and heat sink](05-build-plan/joint-03.png)

*Figure 10. Cut level with the screws, seen from above. The frame holds the block to the shell towers; two screws through the heat sink clamp the module.*

The back face sits flat on the right-hand end of the shell, over the slot fillers. The printed block frame (section 3.10) holds it there. The Peltier module sits on the front face, cold side to the block, and the heat sink on the module. Wrap the block's edges and the tails in closed-cell foam tape after assembly, leaving the module face clear.

**Check before moving on.** The front face is flat; the charged loop holds its charge for 24 hours with no change in the technician's gauge reading.

### 3.6 Slot fillers (make 3)

![Figure 11. Making sketch of the slot fillers](../cad/drawings/CPD-DWG-105.png)

*Figure 11. Slot fillers making sketch (CPD-DWG-105).*

**What they are and what they are made from.** Strips that close the shell's three slots above the pipes and the cable. PETG, printed solid.

**How to make them.** Print two pipe fillers 3 x 10 and one cable filler 3 x 6, each 50.5 tall, lying flat. Each has a half-round notch at the bottom: 9 across for a pipe, 6 for the cable.

**How they fit.** After the foam strip and the upper VIP panel are in, each slides down its slot onto its pipe or cable, with a bead of silicone on both sides (Figure 8). The outer face is flush with the shell, because the cold block sits on it.

**Check before moving on.** Flush within 0.3 mm.

### 3.7 Liner

![Figure 12. Making sketch of the liner](../cad/drawings/CPD-DWG-106.png)

*Figure 12. Liner making sketch (CPD-DWG-106).*

**What it is and what it is made from.** The aluminium box the payload sits in; it spreads the cold evenly round the pens. Aluminium sheet 1.5 mm, 5052, 175 x 110 x 80 mm outside.

**How to make it.**

1. Have a sheet metal shop fold an open box from one blank and TIG weld the four corners.
2. Drill a 6 mm hole in the right-hand wall, 40 toward the front and 71 up, and fit a grommet.
3. Deburr all edges and round the top edge so it cannot cut a hand.
4. Clip the liner probe to the inside of the back wall and the 3 °C cut-out to the inside of the right-hand wall, each on a thin layer of thermal paste. Run their leads to the grommet and join them to the sensor cable.

**How it fits the parts next to it.** It stands on four printed feet on the can floor and is centred by a printed collar (section 3.8), never touching the can. The sensor cable leaves through the grommet, crosses the jacket and leaves the can through its own grommet.

**Check before moving on.** Inside 172 x 107 x 78.5; the top edge flat within 0.3 mm; both sensors and the cut-out read correctly on a meter.

### 3.8 Liner feet (make 4) and collar

![Figure 13. Making sketch of the liner feet and collar](../cad/drawings/CPD-DWG-107.png)

*Figure 13. Liner feet and collar making sketch (CPD-DWG-107).*

**What they are and what they are made from.** Plastic spacers that hold the liner in the middle of the can without a metal path between them. PETG, printed solid.

**How to make them.** Print four feet 12 x 12 x 14 and a collar frame 192 x 127 outside, 175 x 110 inside, 4 tall, lying flat.

**How they fit the parts next to them.**

![Figure 14. Joint 4: liner foot, collar and the lid tray landing](05-build-plan/joint-04.png)

*Figure 14. Cut through a foot, seen from the front. The foot keeps the liner 14 mm above the can floor; the collar centres it inside the can's rim flange; the lid tray lands on the flange.*

Glue a foot under each corner of the liner, 8 in from both edges, and the collar round the liner with its top flush with the liner's top edge, all with two-part epoxy. The collar clears the can's rim flange by 0.5 all round.

**Check before moving on.** The liner stands level on its feet within 0.5 mm.

### 3.9 Payload rack

![Figure 15. Making sketch of the payload rack](../cad/drawings/CPD-DWG-108.png)

*Figure 15. Payload rack making sketch (CPD-DWG-108). The inset shows the payload probe vial lying across the top at the right-hand end.*

**What it is and what it is made from.** A printed floor with two dividers that holds 24 pens of 16 mm, three pairs across and four layers up. PETG.

**How to make it.** Print floor down: a floor 170 x 105 x 2 with two dividers 2 thick and 60 tall, 17 each side of the centre, running the full length.

**How it fits the parts next to it.** It drops into the liner with 1 mm all round. The payload probe, a 10 x 40 mm glycol-buffered vial with a digital sensor, lies across the top layer of pens at the right-hand end, held by a printed clip on the liner's end wall, 1.8 mm above the pens and 1.5 mm below the lid tray.

**Check before moving on.** A 16 mm rod slides freely between each divider and the wall.

### 3.10 Block frame and drip tray

![Figure 16. Making sketch of the block frame and drip tray](../cad/drawings/CPD-DWG-109.png)

*Figure 16. Block frame and drip tray making sketch (CPD-DWG-109).*

**What it is and what it is made from.** A printed frame that holds the cold block against the shell and catches the water that condenses on it. PETG, printed solid.

**How to make it.** Print a plate 98 x 52 x 3.5 with a 42 x 42 window for the Peltier module, four 3.5 mm holes 26 up from its bottom edge (two at 24.5 each side of the centre for the clamp screws to pass, two at 44 each side for the frame screws) and, along the bottom edge, a drip tray 68 wide reaching back 13.5 to the shell, with 2 mm lips at both ends and a 5 mm drain hole near the shell, 30 toward the front.

**How it fits the parts next to it.** The plate rests on the block's front face round the module and is screwed to the shell's two towers with M3 screws. It is 0.5 thinner than the module, so the clamp force goes through the module, and it stays 0.5 clear of the hot heat sink. A 4 mm drain tube runs from the tray's hole down through the floor of the cooling head:

![Figure 17. Joint 8: drip tray and drain tube](05-build-plan/joint-08.png)

*Figure 17. Cut through the drain. Water from the block runs down the tube and out through the head floor, clear of the power board.*

**Check before moving on.** Water poured into the tray runs out of the tube.

### 3.11 Cooling head housing

![Figure 18. Making sketch of the cooling head housing](../cad/drawings/CPD-DWG-110.png)

*Figure 18. Cooling head housing making sketch (CPD-DWG-110).*

**What it is and what it is made from.** The vented printed cover over the Peltier stack, the fan and the power board. PETG or ASA, 60 x 160 x 169.5 mm, 2 mm walls, open on the shell side.

**How to make it.**

1. Print it open side down.
2. Check the end wall: seven grille slots 70 x 5 at 10 pitch from 94 up; a 12 mm hole for the 12 V socket, 20 toward the back, and a 9 x 5 slot for the USB-C socket, 20 toward the front, both 40 up.
3. Check the front wall: five intake slots 5 x 40 from 30 up.
4. Check the floor: a 5 mm drain hole 3.5 from the shell end, 30 toward the front; four 3.4 mm holes for the power board standoffs, 11 from each end, 62 each side.
5. Check the back wall: a notch 8 x 12 at the shell end, 6 up, for the cable duct; and the four ears with 3.4 mm holes, 89 each side of the centre, 40 and 145 up.

**How it fits the parts next to it.**

![Figure 19. Joint 6: a cooling head ear on a shell pad](05-build-plan/joint-06.png)

*Figure 19. One M3 screw through each ear into the pad's insert; the open edge of the housing sits flat on the shell end.*

Inside, the power board stands on four M3 standoffs, the inlets fit the end wall, and the ambient sensor's vented cap sits on the outside of the front wall above the intake slots. A reed switch taped inside the housing's top, 5 from the shell end, faces a magnet in the lid cap's edge to sense an open lid.

**Check before moving on.** The four ears sit flat on the four pads at once.

### 3.12 Wiring

![Figure 20. Block-level wiring](05-build-plan/wiring.png)

*Figure 20. Block-level wiring with wire sizes. No circuit board is laid out; bought modules on perfboard stand in for the power board.*

*Table 2. Modules.*

| Module | What to buy |
| --- | --- |
| Input stage | USB-C PD sink module set to 20 V, 45 W or more; 12 V input with reverse-polarity protection, 10 to 15 V |
| Charger | Four-cell lithium iron phosphate charger, about 12 W, charge stop at 14.4 V |
| Peltier driver | Buck-boost converter that can feed the module from 10 to 20 V input, with an LC output filter for smooth DC and an enable and set point input |
| Fan driver | Switched 12 V output for the 70 mm fan |
| Cut-outs | Two normally closed bimetal thermostats: one on the cold block opening at -5 °C, one on the liner opening at 3 °C |
| Logger | nRF52840-class module with a real-time clock and 2 MB of flash, 3.3 V |
| Sensors | Glycol-buffered payload probe, liner probe, cold-block probe and ambient sensor, digital, ±0.5 °C or better |
| Display and alarm | 2.13 in e-paper, buzzer, red and green lights |

Wire it like this, with stranded copper and a ferrule on every screw terminal:

1. Inlets to the input stage: 1.0 mm² (18 AWG).
2. Input stage to the Peltier driver: 1.0 mm².
3. Peltier driver through the cold-block cut-out and then the liner cut-out to the module: 0.75 mm² (20 AWG). The two cut-outs are in series in the module supply and work without any firmware.
4. Fan driver to the fan: 0.25 mm² (24 AWG).
5. Battery pack to the charger, through the 5 A fuse at the pack: 1.0 mm², along the cable duct.
6. 3.3 V and ground from the power board to the logger: 0.25 mm², along the duct.
7. Sensor cable (eight cores, 0.14 mm²) from the cavity to the logger, along the duct; the driver enable and set point from the logger back to the driver in the same run.
8. Logger to the display and alarm: the display's own ribbon, and 0.25 mm² for the buzzer and lights.

Conformal-coat the power board after the wiring checks pass: water condenses in the cooling head.

**Check before moving on.** Every wire continues end to end and is labelled; with the battery fuse out, no rail reads short to ground; each cut-out reads closed at room temperature and open when chilled in a bag of ice water (it opens at 3 °C; the block's at -5 °C needs a freezer).

### 3.13 Cell cradle

![Figure 21. Making sketch of the cell cradle](../cad/drawings/CPD-DWG-111.png)

*Figure 21. Cell cradle making sketch (CPD-DWG-111).*

**What it is and what it is made from.** A printed block that holds the four 32700 cells upright in the battery bay. PETG.

**How to make it.** Print a block 36 x 140 x 12 with four pockets 32.4 across and 10 deep on a 34 pitch, 2 mm floor under each. Drill two 3.4 mm screw holes between the middle pockets.

**How it fits the parts next to it.** Screwed to the bay floor against its end wall. The cells stand in the pockets, the battery management board sits on top of them, and a hook-and-loop strap holds the pack down.

**Check before moving on.** Each cell drops in without force and does not rattle.

### 3.14 Battery bay housing

![Figure 22. Making sketch of the battery bay housing](../cad/drawings/CPD-DWG-112.png)

*Figure 22. Battery bay housing making sketch (CPD-DWG-112).*

**What it is and what it is made from.** The vented printed box for the battery, logger and display. PETG or ASA, 45 x 160 x 169.5 mm, 2 mm walls, open on the shell side.

**How to make it.** Print it open side down. Check four vent slots 60 x 4 from 30 up in the end wall; a display window 26 x 60 in the top, 9 from the end wall; a 10.4 mm hole for the alarm light, 22 from the end wall and 50 toward the back; the duct notch in the back wall; four 3.4 mm holes in the back wall for the logger standoffs; and four ears like the cooling head's.

**How it fits the parts next to it.** Four M3 screws through the ears into the shell's left-hand pads, as Figure 19. The logger stands on four M3 standoffs on the back wall, the display sits under its window, and the alarm light is pushed into its hole from inside.

**Check before moving on.** The display window lines up with the display's active area.

### 3.15 Cable duct cover

![Figure 23. Making sketch of the cable duct cover](../cad/drawings/CPD-DWG-113.png)

*Figure 23. Cable duct cover making sketch (CPD-DWG-113).*

**What it is and what it is made from.** A printed U-channel that carries the battery and sensor leads along the back of the shell from one housing to the other. PETG.

**How to make it.** Print a channel 8 deep and 12 tall with 1.5 mm walls, open on one side: a back run 261 long and a return 26 long at each end. Print it in three pieces and glue them.

**How it fits the parts next to it.**

![Figure 24. Joint 9: the duct cover turning into the cooling head](05-build-plan/joint-09.png)

*Figure 24. The cover runs along the back face, 6 to 18 up, turns onto the shell end and enters the notch in the housing's back wall.*

The leads lie along the back face; the cover is glued over them with silicone along both edges.

**Check before moving on.** No wire is pinched under an edge.

### 3.16 Lid cold plate tray

![Figure 25. Making sketch of the lid cold plate tray](../cad/drawings/CPD-DWG-114.png)

*Figure 25. Lid cold plate tray making sketch (CPD-DWG-114).*

**What it is and what it is made from.** A shallow aluminium tray that holds the lid PCM pack and, when the lid is closed, lands on the can's rim flange so the Peltier can freeze the lid pack too. Aluminium sheet 1.5 mm, 5052.

**How to make it.** Have a sheet metal shop fold a tray 204 x 139 outside and 16.5 deep from one blank, corners notched and left open, then fold a 6 mm lip inward all round the top edge. The bottom must be flat within 0.3 mm.

**How it fits the parts next to it.**

![Figure 26. Joint 5: the lid stack](05-build-plan/joint-05.png)

*Figure 26. Cut on the centre line at the right-hand end. Cap, VIP plug and tray come off as one; the tray lands on the can's rim flange.*

The lid PCM pack goes in through the lip opening. The lip is bonded to the underside of the VIP lid plug with acrylic foam tape. With the lid closed, the tray's bottom lands on the can's rim flange with 5.5 of overlap and 0.5 clear of the VIP walls all round.

**Check before moving on.** The tray drops into the opening without touching the VIP walls.

### 3.17 Lid cap

![Figure 27. Making sketch of the lid cap](../cad/drawings/CPD-DWG-115.png)

*Figure 27. Lid cap making sketch (CPD-DWG-115).*

**What it is and what it is made from.** The printed top of the case. PETG or ASA, 261 x 196 x 5 mm, four perimeters.

**How to make it.**

1. Print it flat.
2. Set two short M3 inserts for each latch keeper in the top, 72 each side of the centre and 5 in from the front edge, no deeper than 4 mm.
3. Glue a 6 mm magnet into a pocket in the right-hand edge for the lid switch.
4. Bond a closed-cell EPDM strip 10 x 3 all round the underside over the shell rim, and the VIP lid plug in the middle with acrylic foam tape.

**How it fits the parts next to it.** It sits on the shell rim on its gasket; the two draw latches pull it down.

**Check before moving on.** The gasket touches the rim all round before the latches close.

### 3.18 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **VIPs (line 4).** As section 3.2.
- **PCM pouches (line 5).** About 0.94 kg of organic PCM melting at 5 °C (RT 5 HC class) in sealed HDPE pouches: a floor pouch with a relief at each liner foot, two long side pouches, two left-end pouches and three narrow right-end pouches (one between the risers and one outside each), about 0.67 kg in all; and a lid pack about 0.27 kg that fits the tray.
- **Peltier module (line 8).** 40 x 40 mm, 127 couples, about 3 A maximum (TEC1-12703 class).
- **Heat sink and fan (line 9).** Finned aluminium sink 80 x 80 x 30 mm, 0.50 K/W or better with the fan; 70 mm 12 V fan; wire finger guard.
- **Battery (line 11).** Four 32700 lithium iron phosphate cells, 3.2 V, 6 Ah, from a maker that publishes a datasheet; four-cell battery management board with a charge temperature stop; 5 A fuse.
- **Power board modules (line 12), logger (line 13), sensors and cut-outs (line 14), display and alarm (line 15).** As Table 2.
- **Handle and latches (lines 2 and 3).** Folding bail handle rated 10 kg or more with pivot eyes for M5 screws; padded 38 mm strap with two D-rings; two draw latches with keepers.
- **Construction parts (line 17).** 22 M3 and 2 M5 brass heat-set inserts, foam strip, 4 mm drain tube, acrylic foam tape.
- **Fixings and consumables (line 16).** M3 and M5 stainless screws, M3 standoffs, grommets, silicone sealant, two-part epoxy, thermally conductive epoxy, thermal paste, closed-cell foam tape, conformal coating, eight-core sensor cable, wire, ferrules and labels.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: VIP panels into the shell

![Step 1](05-build-plan/step-01.png)

Inserts are already set (section 3.1). Floor panel first, then the front, back, left end and lower right end, each on strips of acrylic foam tape, edges butted tight. **Hold point:** safety stop S3.

### Step 2: loop into the can

![Step 2](05-build-plan/step-02.png)

Lower the ring into the can with the risers dropping down the can's slots. Bond the ring into the bottom corner with thermally conductive epoxy and let it cure.

### Step 3: cold block onto the tails, then charge

![Step 3](05-build-plan/step-03.png)

The technician brazes the tails and charge stub into the block, leak tests with dry nitrogen, evacuates, charges and pinches the stub. **Hold point:** safety stops S1 and S2; the loop holds its charge for 24 hours.

### Step 4: evaporator assembly into the VIP box

![Step 4](05-build-plan/step-04.png)

Lower the can, loop and block straight down into the VIP box. The tails drop down the shell's open slots and the block hangs outside the right-hand end.

### Step 5: foam strip, upper end panel and slot fillers

![Step 5](05-build-plan/step-05.png)

Cut the foam strip into an upper and a lower piece round the pipes and fit it; feed the sensor cable through its slot as you do. Lay the upper right-end VIP on the foam. Slide the three fillers down their slots onto the pipes and cable and seal them with silicone.

### Step 6: PCM pouches into the can

![Step 6](05-build-plan/step-06.png)

Floor pouch first, its reliefs at the four feet positions; then the side, left-end and the three narrow right-end pouches round the risers. **Hold point:** safety stop S8; no brazing or hot work from here on.

### Step 7: liner sub-assembly

![Step 7](05-build-plan/step-07.png)

On the bench: feet and collar glued on, liner probe and cut-out clipped inside, sensor cable through the liner grommet (section 3.7).

### Step 8: liner into the can

![Step 8](05-build-plan/step-08.png)

Feed the sensor cable through the can's grommet first, then lower the liner onto its feet. The collar centres it inside the rim flange.

### Step 9: rack and payload probe into the liner

![Step 9](05-build-plan/step-09.png)

Drop the rack in and clip the probe vial to the liner's right-hand wall above where the top layer of pens will lie.

### Step 10: block frame and drip tray onto the towers

![Step 10](05-build-plan/step-10.png)

Two M3 screws through the frame into the tower inserts, snug. Push the drain tube up into the tray's hole from below.

### Step 11: Peltier module and heat sink onto the block

![Step 11](05-build-plan/step-11.png)

A thin even layer of thermal paste on both module faces, cold side to the block (check the maker's marking). Heat sink on the module, two M3 screws through the sink into the block, tightened a little at a time in turn. Wrap the block's exposed edges and the tails in closed-cell foam tape.

### Step 12: fan and guard onto the sink

![Step 12](05-build-plan/step-12.png)

Fan blowing out through the grille, finger guard on its outer face, four fan screws into the gaps between the fins.

### Step 13: build the cooling head

![Step 13](05-build-plan/step-13.png)

On the bench: standoffs into the floor, power board on them, inlets into the end wall, ambient sensor cap on the front, reed switch inside the top. Wire as section 3.12. **Hold point:** the wiring checks of section 3.12 pass.

### Step 14: cooling head onto the shell

![Step 14](05-build-plan/step-14.png)

Connect the module, fan, cut-out and drain; slide the housing over the stack; four M3 screws through the ears into the shell pads.

### Step 15: build the battery bay

![Step 15](05-build-plan/step-15.png)

On the bench: cradle screwed to the floor, cells in, battery management board on top, strap; logger on its standoffs on the back wall; display under its window and the alarm light in its hole. **Hold point:** safety stop S4; fuse out.

### Step 16: battery bay onto the shell

![Step 16](05-build-plan/step-16.png)

Fuse still out. Connect the duct leads, then four M3 screws through the ears into the left-hand pads.

### Step 17: cable duct cover onto the back face

![Step 17](05-build-plan/step-17.png)

Seen from the back. Lay the battery, 3.3 V and sensor leads along the back face 6 to 18 up and glue the cover over them.

### Step 18: handle and latches

![Step 18](05-build-plan/step-18.png)

Handle on two M5 pivot screws, the strap's D-rings under the screw heads; latches on two M3 screws each, keepers on the lid cap.

### Step 19: build the lid

![Step 19](05-build-plan/step-19.png)

Seen from below. VIP plug onto the cap with acrylic foam tape; lid pack into the tray; the tray's lip onto the plug with foam tape.

### Step 20: lid on

![Step 20](05-build-plan/step-20.png)

Fold the handle down to one side, lower the lid straight down and close both latches. **Hold point:** safety stops S5 to S7 before any power.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of CPD-REQ-001.

*Table 3. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Payload fits | R3 | Load 24 rods 16 mm across and 160 mm long, and one 172 mm long | All fit; the lid closes; the probe vial clears the top layer |
| Lid seal and tray landing | R1, R16 | Close the lid on a strip of thin paper at several points round the gasket, then on a strip on the can flange | The paper is gripped at every point on both |
| Loop sealed | R7 | The technician's 24 hour charge check | No change in the gauge reading |
| Cut-outs | R2 | Chill each cut-out (ice water for the liner one, a freezer for the block one) with the module supply on a bench supply at low current | The supply opens at each cut-out without any firmware running |
| First cooling on a bench supply | R7 | 12 V, current limit 3 A, box empty; watch the block probe and the sink | The block cools within a minute; the fan runs; the sink stays below 60 °C |
| Input range | R7 | Bench supply at 10 V and at 15 V; then a USB-C PD charger | The driver runs the module at its set point on all three |
| Charge stops | R14 | Battery charging from the bench supply; substitute the board's temperature sensor with resistors for -1 °C and 46 °C | No charge current in either case |
| Logger and probes | R9 | Read all four probes in a room and in an ice-water bath | Each within ±0.5 °C of a reference thermometer |
| Alarms | R10 | Open the lid; unplug a probe; warm the payload probe by hand past 8 °C | Lid-open, sensor-fault and out-of-range alarms sound and show |
| Drain | R16 | Pour 20 ml of water into the drip tray | It leaves through the head floor; the power board stays dry |
| Size and mass | R12, R13 | Measure over the handle; weigh empty | Within 400 x 250 x 250 mm; mass recorded (5.70 kg estimated) |
| Battery removal | R14 | Remove the battery bay and unplug the duct leads | The pack comes out with a screwdriver |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before any brazing.** The can, loop and block are on a steel bench with no plastic, VIP, PCM or paper within 1 m. Work in a ventilated space with a fire extinguisher at hand. Brazing is done by a technician trained in it, with eye protection and a nitrogen purge.
- **S2. Before the loop is charged.** The technician is qualified to handle refrigerants where you live and chooses the working fluid and charge. The loop has passed a dry nitrogen leak test at the technician's test pressure. Eye protection and gloves; never heat a charged loop.
- **S3. Before the VIPs come out of their packaging.** No knives, drills or sharp tools on the bench. Handle panels by their faces, never by a corner.
- **S4. Before the cells come into the workshop.** Each cell reads about 2.8 to 3.4 V, with no swelling, dents or leaks and a datasheet from its maker. The fuse is out. A charging spot is ready on a non-combustible surface with a fire extinguisher for electrical fires.
- **S5. Before first power to the Peltier module.** The heat sink is clamped and the fan connected: a module run without its heat sink overheats in seconds. Both cut-outs are in series in the module supply and pass their check. The bench supply current limit is 3 A or less.
- **S6. Before the battery fuse goes in.** Polarity checked with a meter at the battery board, not by wire colour; with the fuse out, no rail reads short to ground; the charger stops at 14.4 V on a bench check.
- **S7. First charge.** Attended the whole time, lid open, case on the charging spot; cell temperature checked every 15 minutes. Stop if a cell passes 45 °C or 3.65 V.
- **S8. Once the PCM is in.** The paraffin is combustible: no brazing, soldering or hot work on the case from here on, and any leaking pouch is replaced at once.
- **S9. Before the case leaves the workshop.** It is labelled "Research prototype, not a medical device"; it carries no real vaccines or medicines.

## 7. Tools, skills and workspace

**Tools.** 3D printer with a bed of at least 300 x 300 mm and 180 mm of height, enclosed for ASA; soldering iron with heat-set insert tips for M3 and M5; lever tube bender for 8 mm tube and a tube cutter; drill press, drills 2.5 to 12 mm, M3 tap; files and deburring tool; steel rule, calipers, square and a surface plate or flat glass for checking flatness; utility knife for foam only; ferrule crimper and wire strippers; soldering iron for wiring; multimeter; bench power supply 0 to 20 V, 0 to 5 A with a current limit; USB-C PD charger of 45 W or more; two reference thermometers; scale to 10 kg. The sheet metal parts (can, liner, tray) and the brazing, leak testing and charging need a sheet metal shop and a refrigeration technician with their own tools.

**Skills.** Printing large parts in PETG or ASA; setting threaded inserts; simple tube bending; soldering and crimping; safe use of a bench supply and care with lithium cells. All circuits are 20 V DC or less; no mains wiring is part of this build. Brazing, refrigerant handling and charging are trades: use a qualified technician.

**Workspace.** A bench about 1.5 x 0.75 m kept clean and free of sharp tools for the VIP work; a separate steel bench or outside space for brazing; a ventilated place for the printer; the charging spot of S4.

**Personal protective equipment.** Safety glasses for drilling, brazing and charging; gloves for sheet metal edges and refrigerant work; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 63 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/CPD-DWG-101` to `CPD-DWG-115`.
- General arrangement: `cad/drawings/CPD-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (CPD-CAL-001 v0.4) and `docs/04-calcs/sizing.py`; size [A6], heat leak [B9], PCM [C2], hold times [D2, F2], refreeze [G4], thermosiphon [H4, H5], mass [K2], cost [L2].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (CPD-DDR-003), with CPD-DDR-001 and CPD-DDR-002.
- Requirements: `docs/03-requirements.md` (CPD-REQ-001 v0.6).
