---
doc_id: CPD-REQ-001
title: ColdPod requirements
project: ColdPod
doc_type: Requirements
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
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions (CPD-DDR-001); R6 redefined to 16 h, R12 relaxed to 5.5 kg, R15 set to $300; status from CPD-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R2 and R7 targets restated for the liner cut-out and buck-boost driver; status from CPD-CAL-001 v0.2
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish; R15 target $310, status met against CPD-CAL-001 v0.3
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status values from CPD-CAL-001 v0.4 for the constructable design (CPD-DDR-003, Draft); no target changed
- version: "0.7"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# ColdPod requirements

These are the requirements for the concept, checked by calculation at TRL 3 in CPD-CAL-001 v0.4 against the constructable design of CPD-DDR-003 (Draft, open for Amish's review). Amish decided the TRL 2 review items on 2026-09-25 (CPD-DDR-001): R6 is redefined from 24 h to 16 h at 43 °C (D5), R12 is relaxed from 5.0 kg to 5.5 kg (D6), R15 follows the $300 value-engineering target of D10 and the R10 alarm defaults are adopted (D9). He then accepted the TRL 3 recommendations (CPD-DDR-002): R2 now names the two hardware cut-outs in series and R7 names the buck-boost driver that serves the full 10 to 15 V vehicle range; no target was relaxed. The target is now $310 (CPD-DDR-002 N3), a hypothetical control target and not a limit, and R15 follows it. No target changed in v0.6; the values follow the constructable design. Against CPD-CAL-001 v0.4, ten requirements are met, three are at risk, two are **not met** by small margins (R8 and R12) and two cannot be verified at TRL 3 (R10 and R16). Before DDR-002 the count was seven met, five at risk and three not met (R2, R8, R12).

Table 1. Requirements.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (CPD-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Keep the payload in the safe range | 2 to 8 °C at a buffered probe anywhere in the payload space; control setpoint 5 °C | Heat-transfer calculation; later lab test in a climate chamber | Met on paper: liner held at 2 to 5 °C; the lid pack stays frozen near 2.8 °C on its cold plate in powered hold at 43 °C (was at risk) |
| R2 | Never freeze the payload | No payload-contact surface below 1 °C in normal operation or with a stuck-on Peltier driver; two hardware cut-outs in series in the Peltier supply, on the cold block (−5 °C) and on the liner (3 °C), independent of firmware (CPD-DDR-002) | Calculation of the cold path; fault analysis | Met on paper: with a stuck-on driver the liner settles near 2.0 °C after the liner cut-out opens (was not met, about −4 °C) |
| R3 | Carry a useful load | 1.0 L or more of usable payload; holds 20 or more insulin pens up to 170 mm long | Massing model | Met: 1.37 L, 24 pens, up to 172 mm |
| R4 | Hold with no power at all | 12 h or more at a constant +43 °C, starting with the PCM frozen | Heat-leak and PCM calculation | At risk: 13.3 h; 10.2 h with 30 % more heat leak |
| R5 | Hold off-grid on a full charge | 24 h or more at a constant +32 °C on the internal battery, then the PCM | Energy budget | At risk: 27.3 h; 21.4 h with 30 % more heat leak |
| R6 | Hold off-grid on a full charge in extreme heat | 16 h or more at a constant +43 °C on the internal battery, then the PCM; longer hot trips run from external power under R7 (redefined from 24 h, CPD-DDR-001 D5) | Energy budget | At risk: 16.7 h; 12.6 h with 30 % more heat leak |
| R7 | Hold indefinitely on external power | Keeps 2 to 8 °C up to +43 °C from 12 V DC (10 to 15 V, through a buck-boost Peltier driver, CPD-DDR-002) or USB-C PD (20 V, 45 W or more) | Peltier and heat sink calculation | Met on paper: 18.8 W input, well inside 45 W; the buck-boost stage covers a 10 V input; the lid pack stays frozen (was at risk) |
| R8 | Recharge the cold quickly | Refreeze a fully melted PCM in 8 h or less at 25 °C ambient, box empty, while charging the battery | PCM and Peltier calculation | **Not met: 8.0 h** (8.03 h) for all the PCM (jacket 6.8 h, lid pack 8.0 h), a few minutes over; 8.4 h before the constructable design, which holds slightly less PCM |
| R9 | Record the temperature | Payload probe accuracy ±0.5 °C; log every 1 min; 60 days or more on board; export as CSV over Bluetooth Low Energy or USB | Datasheet and storage calculation; later calibration | Met: 1.38 MB of 2.10 MB; accuracy by sensor selection |
| R10 | Raise alarms early | Local sound, light and display alarm, plus a phone notification when paired: warn after 10 min outside 2 to 8 °C; alarm at once at 0 °C or lower on the payload probe; early freeze warning at 1 °C on the liner probe; low battery, sensor fault and lid open for more than 2 min (defaults decided, CPD-DDR-001 D9; adjustable per product) | Design review of firmware sketch | Not verifiable at TRL 3: design intent only, no firmware sketch |
| R11 | Keep logging when the cooling stops | Logger runs 14 days or more after the Peltier is shut off for low battery | Power budget | Met: about 96 days |
| R12 | Be light enough to carry all day | 5.5 kg (12.1 lb) or less empty (relaxed from 5.0 kg, CPD-DDR-001 D6) | Mass estimate, later weighing | **Not met: 5.70 kg** (5.53 kg before the fixings and parts added to make the design buildable, CPD-DDR-003) |
| R13 | Be compact | Fits in 400 x 250 x 250 mm including handle | Massing model | Met: 366 x 220 x 207 mm |
| R14 | Travel by air | Battery 100 Wh or less, removable or with a shipping switch | Battery specification | Met: 76.8 Wh |
| R15 | Be affordable and buildable | Estimated parts cost within the $310 value-engineering target (hypothetical control target, CPD-DDR-002 N3); no custom PCB for the first build | Priced BOM | Within the value-engineering target: $308 against $310, with the construction parts of CPD-DDR-003 |
| R16 | Survive field use | Splash resistant (IP54 target for electronics bays); survives a 0.5 m drop onto a hard floor while loaded | Design review; later test | Not verifiable at TRL 3 |
| R17 | Be clearly labelled as a prototype | "Research prototype, not a medical device" on the box, the display start screen and every exported log | Design review | Met by design |

## Assumptions

- Ambient cases follow the WHO PQS test point of +43 °C for the hot zone ([WHO PQS E004/VC01](https://extranet.who.int/prequal/key-resources/documents/pqs-independent-type-testing-protocol-e004vc01-vp2-vaccine-carrier)), +32 °C for a typical hot day and 25 °C for a clinic.
- The 2 to 8 °C window and the no-freezing rule come from insulin and vaccine storage guidance ([US FDA](https://www.fda.gov/drugs/emergency-preparedness-drugs/information-regarding-insulin-storage-and-switching-between-products-emergency); [CDC Pink Book, chapter 5](https://www.cdc.gov/pinkbook/hcp/table-of-contents/chapter-5-vaccine-storage-and-handling.html)).
- Logging and alarm targets are stricter than a WHO 30-day recorder (−0.5 °C for 60 min, +8 °C for 10 h; [TechNet-21](https://www.technet-21.org/en/temperature-monitoring/finding-the-right-solution/finding-the-right-solution-30dtr)) because a carrier in transit can move out of range much faster than a refrigerator.
- R6 matches the WHO long-range carrier cold life only loosely: a WHO carrier is tested passive for 30 h at 43 °C. ColdPod does not claim WHO equivalence.
- The alarm thresholds in R10 were decided by Amish on 2026-09-25 (CPD-DDR-001 D9) and will be adjustable per product.
- Hold-time status uses a ±30 % band on the heat leak: met if the target holds at +30 %, at risk if it holds only at the nominal estimate (CPD-CAL-001).
- R15 counts ColdPod parts only; the payload is not costed.
