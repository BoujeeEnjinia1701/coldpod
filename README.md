# ColdPod

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** BioMedical · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $300 USD · **Difficulty:** 3 of 5

Portable Peltier cooler with a phase-change buffer and a temperature logger that raises alerts on excursions.

![ColdPod concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement CPD-DWG-001 (PDF)](cad/drawings/CPD-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Insulin and vaccines spoil in field transport without a reliable cold chain. They must stay between 2 and 8 °C: ice packs run out in the heat, freeze vials when they are too cold, and usually nothing records what happened. Studies of the vaccine cold chain find freezing exposure in roughly a fifth to a third of storage and shipping studies. Design with, not for: requirements must come from co-design with health workers and people who carry insulin, through a local partner.

Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

A carry case 368 x 214 x 207 mm holds 1.36 L of insulin or vaccines (24 insulin pens) in an aluminium liner wrapped in a phase-change material that melts at 5 °C, inside 25 mm vacuum-insulated panels. A Peltier module refreezes the phase-change material from a 12 V socket, a solar panel or a USB-C charger, through a loop thermosiphon that carries heat one way only. A 76.8 Wh LiFePO4 battery keeps it cooling on the road, and a logger records the payload temperature every minute and raises alarms on excursions.

TRL 3 calculations ([CPD-CAL-001](docs/04-calcs/01-sizing.md)): about 13.0 h with no power at 43 °C, 26.5 h off-grid at 32 °C and 16.5 h off-grid at 43 °C, all with thin margins; 5.60 kg empty (over the 5.5 kg target) and $295 in parts (budget $300). Two design gaps remain: the lid phase-change pack cannot be refrozen by the Peltier, and a stuck-on driver could freeze the liner. Fixes are proposed, awaiting Amish. TRL 4 (lab testing) is on hold.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Vacuum-insulated panels, 25 mm, in a printed shell
- Phase-change material packs, 5 °C, around an aluminium liner
- Aluminium evaporator can and loop thermosiphon (one-way) to a 40 mm Peltier module (TEC1-12703 class)
- Heat sink and fan in a vented cooling head
- LiFePO4 battery, 12.8 V 6 Ah (76.8 Wh), with BMS
- USB-C PD and 12 V power board
- nRF52840 logger with buffered payload probe, e-paper display and alarm

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> This is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, is not WHO-prequalified, and must not be used to diagnose, treat or monitor any person or as the only protection for real vaccines or insulin.

It contains a lithium (LiFePO4) battery, a combustible paraffin phase-change material and a heat sink that can get hot. See the safety section of the [design precis](docs/02-concept.md#safety).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations (`04-calcs/`) and design decisions (`decisions/`) |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (CPD-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `CPD-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
