---
doc_id: CPD-REQ-001
title: ColdPod requirements
project: ColdPod
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
  change: First measurable requirements for TRL 2, with status against the concept estimates
---

# ColdPod requirements

These are first-pass requirements for the concept. Targets are proposals for review, awaiting Amish, and will be checked by calculation at TRL 3. The status column compares each target with the first-order estimates in CPD-PRC-001; three requirements are **not met** by the current concept (R6, R12 and R15) and two are met with thin margins (R4 and R5).

Table 1. Requirements.

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status (estimate) |
| --- | --- | --- | --- | --- |
| R1 | Keep the payload in the safe range | 2 to 8 °C at a buffered probe anywhere in the payload space; control setpoint 5 °C | Heat-transfer calculation; later lab test in a climate chamber | Met by design |
| R2 | Never freeze the payload | No payload-contact surface below 1 °C in normal operation or with a stuck-on Peltier driver | Calculation of the cold path; fault analysis | Met by design (5 °C PCM between cold path and liner; hardware cut-out) |
| R3 | Carry a useful load | 1.0 L or more of usable payload; holds 20 or more insulin pens up to 170 mm long | Massing model | Met: about 1.2 L, about 24 pens |
| R4 | Hold with no power at all | 12 h or more at a constant +43 °C, starting with the PCM frozen | Heat-leak and PCM calculation | Met, thin margin: about 12.7 h |
| R5 | Hold off-grid on a full charge | 24 h or more at a constant +32 °C on the internal battery, then the PCM | Energy budget | Met, thin margin: about 26 h |
| R6 | Hold off-grid on a full charge in extreme heat | 24 h or more at a constant +43 °C on the internal battery, then the PCM | Energy budget | **Not met: about 16 h** |
| R7 | Hold indefinitely on external power | Keeps 2 to 8 °C up to +43 °C from 12 V DC (10 to 15 V) or USB-C PD (20 V, 45 W or more) | Peltier and heat sink calculation | Met on estimate (about 17 W needed at 43 °C) |
| R8 | Recharge the cold quickly | Refreeze a fully melted PCM in 8 h or less at 25 °C ambient, box empty, while charging the battery | PCM and Peltier calculation | Met: about 6 h |
| R9 | Record the temperature | Payload probe accuracy ±0.5 °C; log every 1 min; 60 days or more on board; export as CSV over Bluetooth Low Energy or USB | Datasheet and storage calculation; later calibration | Met by design |
| R10 | Raise alarms early | Local sound, light and display alarm, plus a phone notification when paired: warn after 10 min outside 2 to 8 °C; alarm at once at 0 °C or lower; low battery, sensor fault and lid open for more than 2 min | Design review of firmware sketch | Met by design |
| R11 | Keep logging when the cooling stops | Logger runs 14 days or more after the Peltier is shut off for low battery | Power budget | Met: reserve lasts weeks |
| R12 | Be light enough to carry all day | 5.0 kg (11 lb) or less empty | Mass estimate, later weighing | **Not met: about 5.2 kg** |
| R13 | Be compact | Fits in 400 x 250 x 250 mm including handle | Massing model | Met: about 370 x 215 x 205 mm |
| R14 | Travel by air | Battery 100 Wh or less, removable or with a shipping switch | Battery specification | Met: 76.8 Wh |
| R15 | Be affordable and buildable | Parts cost $250 or less; no custom PCB for the first build | Priced BOM | **Not met: about $280** |
| R16 | Survive field use | Splash resistant (IP54 target for electronics bays); survives a 0.5 m drop onto a hard floor while loaded | Design review; later test | Unverified |
| R17 | Be clearly labelled as a prototype | "Research prototype, not a medical device" on the box, the display start screen and every exported log | Design review | Met by design |

## Assumptions

- Ambient cases follow the WHO PQS test point of +43 °C for the hot zone ([WHO PQS E004/VC01](https://extranet.who.int/prequal/key-resources/documents/pqs-independent-type-testing-protocol-e004vc01-vp2-vaccine-carrier)), +32 °C for a typical hot day and 25 °C for a clinic.
- The 2 to 8 °C window and the no-freezing rule come from insulin and vaccine storage guidance ([US FDA](https://www.fda.gov/drugs/emergency-preparedness-drugs/information-regarding-insulin-storage-and-switching-between-products-emergency); [CDC Pink Book, chapter 5](https://www.cdc.gov/pinkbook/hcp/table-of-contents/chapter-5-vaccine-storage-and-handling.html)).
- Logging and alarm targets are stricter than a WHO 30-day recorder (−0.5 °C for 60 min, +8 °C for 10 h; [TechNet-21](https://www.technet-21.org/en/temperature-monitoring/finding-the-right-solution/finding-the-right-solution-30dtr)) because a carrier in transit can move out of range much faster than a refrigerator.
- R6 matches the WHO long-range carrier cold life only loosely: a WHO carrier is tested passive for 30 h at 43 °C. ColdPod does not claim WHO equivalence.
- The alarm thresholds in R10 are proposed defaults, awaiting Amish, and will be adjustable per product.
