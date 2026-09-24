# ColdPod

**Area:** BioMedical · **Status:** Concept · **Prototype budget:** about $250 USD · **Difficulty:** 3 of 5

Portable Peltier cooler with a phase-change buffer and a temperature logger that raises alerts on excursions.

## Problem

Insulin and vaccines spoil in field transport without a reliable cold chain.

## Concept

Portable Peltier cooler with a phase-change buffer and a temperature logger that raises alerts on excursions.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Peltier module
- Heat sink and fan
- Phase-change material packs
- Vacuum-insulated panels
- Temperature sensors
- LiFePO4 pack
- Data logger

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> This is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose, treat or monitor any person.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
