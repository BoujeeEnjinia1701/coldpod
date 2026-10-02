---
doc_id: CPD-PRB-001
title: ColdPod problem statement
project: ColdPod
doc_type: Problem statement
version: "0.6"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (problem, users and context, constraints, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions (CPD-DDR-001), outreach vaccinators first and budget $300; partner stays open
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); budget kept at $300; origin of the idea (vaccine vial monitor) added
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish; budget $310
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Partner type decided and first candidate to approach (CPD-DEC-001, 2026-10-02)"
---

# ColdPod problem statement

Insulin and vaccines must stay between 2 and 8 °C in transport, but the last leg of the cold chain (a health worker on foot or on a motorbike, or a person with diabetes travelling in a hot place without steady power) relies on ice packs and luck: loads get too warm when the ice runs out, freeze when the ice is too cold, and nobody knows either happened because nothing records the temperature.

## The problem

**Both heat and cold spoil the load.** Unopened insulin keeps its potency until the printed expiry date only when stored at about 2 to 8 °C (36 to 46 °F); it can be kept at 15 to 30 °C (59 to 86 °F) for up to 28 days, loses potency faster above that, and must be thrown away if it has frozen ([US FDA, insulin storage in emergencies](https://www.fda.gov/drugs/emergency-preparedness-drugs/information-regarding-insulin-storage-and-switching-between-products-emergency)). Most routine vaccines have the same 2 to 8 °C window, and several (for example those with an aluminium adjuvant) are damaged by freezing.

**Freezing is common, not rare.** A systematic review found that vaccines were exposed to temperatures below the recommended range in about 33 % of storage studies in wealthier countries and 37 % in lower-income countries, and during shipment in 38 % and 19 % of studies respectively ([Hanson et al., *Vaccine*, 2017](https://www.sciencedirect.com/science/article/pii/S0264410X16309471); an earlier review reached a similar conclusion: [Matthias et al., *Vaccine*, 2007](https://pubmed.ncbi.nlm.nih.gov/17382434/)). Frozen water ice packs placed against vials are a well-known cause, which is why WHO now prequalifies "freeze-free" cold boxes and carriers ([WHO PQS E004/CB05.3](https://extranet.who.int/pqweb/key-resources/documents/pqs-performance-specification-e004cb053-vaccine-cold-box-freeze-prevention)).

**Passive carriers have a fixed clock.** A WHO-prequalified vaccine carrier must keep its load cold for at least 15 h (short range) or 30 h (long range) at a constant +43 °C, and then it needs freshly frozen or conditioned ice packs ([WHO PQS E004/VC01 test protocol](https://extranet.who.int/prequal/key-resources/documents/pqs-independent-type-testing-protocol-e004vc01-vp2-vaccine-carrier)). Where freezers are scarce or power is intermittent, the ice packs are the weak link.

**Monitoring is separate and often missing.** Good practice is a digital data logger with a buffered probe, ±0.5 °C accuracy, logging at least every 30 min and an out-of-range alarm ([CDC Pink Book, chapter 5](https://www.cdc.gov/pinkbook/hcp/table-of-contents/chapter-5-vaccine-storage-and-handling.html)). WHO's 30-day temperature recorders alarm at −0.5 °C or lower for 60 min and at +8 °C or higher for 10 h ([TechNet-21, 30DTR](https://www.technet-21.org/en/temperature-monitoring/finding-the-right-solution/finding-the-right-solution-30dtr)). In a carrier, these are extra devices that are easy to leave behind, and they record a problem rather than prevent it.

**Existing active coolers are closed or costly.** Battery-powered cold chain boxes with built-in monitoring exist, for example the Ember Cube shipping box ([Fast Company](https://www.fastcompany.com/90717041/ember-known-for-keeping-coffee-hot-builds-a-shipping-box-to-keep-vaccines-cold)), and small USB-powered insulin coolers are sold to travellers ([4AllFamily Voyager](https://4allfamily.com/products/portable-medical-fridge-usb-insulin-medicines)). None is an open, inspectable design that a clinic, university group or maker space can build, repair and adapt.

**Indicators record heat, not cold.** The vaccine vial monitor, a heat-sensitive label that WHO and PATH brought into use on oral polio vaccine in 1996 ([PATH](https://www.path.org/our-impact/articles/vaccine-vial-monitor-worlds-smartest-sticker/)), showed how much a cheap indicator travelling with each vial can do, but it does "not measure exposure to freezing temperatures" ([OpenLearn Create, Immunization module](https://www.open.edu/openlearncreate/mod/oucontent/view.php?id=53354&section=1.5.1)). That gap between heat monitoring and freeze protection is the starting point for ColdPod.

The gap ColdPod addresses: an open, repairable carrier that combines passive storage (so it works with no power), active cooling (so it can be topped up from a vehicle, a solar panel or a USB-C charger instead of a freezer) and an integrated logger that raises alarms before a load is lost.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Outreach vaccinator or community health worker | Carry a day's vaccines to villages and back without freezing or overheating them; know that the load stayed in range | On foot, bicycle or motorbike; 25 to 43 °C; clinic power intermittent; 8 to 12 h trips |
| Person with diabetes | Keep a month's insulin cold while travelling or during power cuts | Hot climates, long journeys, displacement, homes without a refrigerator |
| Pharmacy or clinic running home deliveries | Deliver temperature-sensitive medicines with a record of the trip | Van or motorbike with a 12 V socket |
| Humanitarian or disaster response team | Carry insulin and vaccines where the grid is down | Solar panels, vehicles, generator hours |
| Open hardware and global health researchers | A reproducible, auditable reference design | University labs, maker spaces |

## Constraints

- Garage-buildable prototype, $310 USD or less in parts (raised from $250 to $300 by Amish, 2026-09-25, CPD-DDR-001 D10, and to $310 by Amish, 2026-09-26, CPD-DDR-002 N3; the TRL 3 BOM is $303), using off-the-shelf modules, 3D-printed or hand-made parts, and bought vacuum-insulated panels.
- Carried by one person, by hand or on a shoulder strap.
- Chargeable from a vehicle 12 V socket, a small solar panel or a USB-C Power Delivery (PD) charger; no mains-voltage parts inside the box.
- Battery small enough to carry on a passenger aircraft without airline approval (100 Wh or less per the [FAA PackSafe rules](https://www.faa.gov/hazmat/packsafe/lithium-batteries)).
- Research and educational prototype only. ColdPod is not a medical device, is not WHO-prequalified, and must not be the only protection for real vaccines or insulin.

## Out of scope

- Frozen and ultra-cold products (for example −20 °C or −70 °C vaccines).
- Clinic refrigerators and bulk storage.
- Regulatory prequalification, which would follow only after lab and field validation well beyond TRL 3.
- Cloud services. Data stays on the device and the owner's phone.

## Open questions

- Which user comes first? Decided by Amish, 2026-09-25 (CPD-DDR-001 D11): the outreach vaccinator first, since that user sets the 43 °C design case; the traveller with insulin second.
- Which partner should help shape the requirements? Decided by Amish, 2026-10-02 (CPD-DEC-001): an immunization program, consistent with outreach vaccinators first. First candidate to approach: PATH, or a national immunization program's outreach team reached through it. Nothing is agreed yet.
- How hot does it really get inside a carrier strapped to a motorbike in direct sun? The 43 °C WHO test point is used until field data exists.
