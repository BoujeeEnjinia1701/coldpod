"""ColdPod prototype build plan pictures (CPD-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|vips|sheets|joints|steps|wiring ...]
A sheet, joint or step can be drawn alone: sheets:104, joints:3, steps:12.
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    docs/05-build-plan/vip-panels.png      the seven bought VIP panels and the foam strip
    cad/drawings/CPD-DWG-101 to 115        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, levels  # noqa: E402
from build123d import Pos  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
L = levels(P)
C = build_components(P)

COL = {"shell": "#94A3B8", "fillers": "#475569", "duct": "#64748B", "vip": "#D6D3D1", "foam": "#FCD34D",
       "can": "#9CA3AF", "loop": "#B87333", "block": "#6B7280", "frame": "#0F766E", "drain": "#334155",
       "tec": "#7DD3FC", "sink": "#4B5563", "fan": "#1F2937", "screws": "#111827", "head": "#0E7490",
       "bay": "#0E7490", "lid": "#A1A1AA", "latches": "#111827", "lidplate": "#78716C", "pcm": "#60A5FA",
       "liner": "#A8A29E", "feet": "#7C3AED", "rack": "#F59E0B", "pens": "#F3F4F6", "sensors": "#D4A017",
       "power": "#15803D", "cells": "#C2410C", "cradle": "#7C2D12", "logger": "#1F2937", "display": "#38BDF8",
       "handle": "#374151"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def S(*ks):
    return _fuse([C[k].shape for k in ks])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


VIPS = ("vip_floor", "vip_front", "vip_back", "vip_endm", "vip_endlo")


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "shell": part("Outer shell and slot fillers", S("shell", "fillers"), COL["shell"]),
        "vips": part("VIP panels, body (6)", S(*VIPS, "vip_endhi"), COL["vip"]),
        "can": part("Evaporator can", C["can"].shape, COL["can"]),
        "loop": part("Loop thermosiphon", C["loop"].shape, COL["loop"]),
        "block": part("Cold block and charge stub", S("block", "charge"), COL["block"]),
        "foam": part("Foam strip", C["foam"].shape, COL["foam"]),
        "jacket": part("PCM jacket pouches", C["pcm_jacket"].shape, COL["pcm"]),
        "feet": part("Liner feet and collar", S("feet", "collar"), COL["feet"]),
        "liner": part("Liner, probes and liner cut-out", S("liner", "liner_probe", "cutout"), COL["liner"]),
        "rack": part("Payload rack and payload probe", S("rack", "probe"), COL["rack"]),
        "frame": part("Block frame and drip tray", S("frame", "drain"), COL["frame"]),
        "tec": part("Peltier module", C["tec"].shape, COL["tec"]),
        "sink": part("Heat sink, fan and guard", S("sink", "fan", "guard"), COL["sink"]),
        "power": part("Power board, inlets, ambient sensor", S("power", "power_so", "inlets", "ambient"), COL["power"]),
        "head": part("Cooling head housing", C["head"].shape, COL["head"]),
        "cells": part("Cell cradle, cells and BMS", S("cradle", "cells"), COL["cells"]),
        "logger": part("Logger, display, alarm light", S("logger", "logger_so", "display", "alarm"), COL["display"]),
        "bay": part("Battery bay housing", C["bay"].shape, COL["bay"]),
        "duct": part("Cable duct cover", C["duct"].shape, COL["duct"]),
        "handle": part("Handle and latches", S("handle", "latches"), COL["handle"]),
        "tray": part("Lid cold plate tray and lid pack", S("lidplate", "pcm_lid"), COL["lidplate"]),
        "plug": part("VIP lid plug", C["vip_lid"].shape, COL["vip"]),
        "lid": part("Lid cap", C["lid"].shape, COL["lid"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"shell": (0, 0, 0), "vips": (0, 0, 170), "can": (0, 0, 430), "loop": (0, 0, 310), "block": (0, 0, 310),
           "foam": (110, 0, 170), "jacket": (0, 0, 590), "feet": (0, 0, 690), "liner": (0, 0, 750), "rack": (0, 0, 870),
           "frame": (170, 0, 0), "tec": (240, 0, 0), "sink": (310, 0, 0), "power": (380, 0, -110), "head": (470, 0, 0),
           "cells": (-170, 0, 0), "logger": (-250, 0, 80), "bay": (-340, 0, 0), "duct": (0, 0, -120),
           "handle": (-360, 0, 470), "tray": (0, 0, 1010), "plug": (0, 0, 1110), "lid": (0, 0, 1200)}
    parts = []
    for k, p in M.items():
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "ColdPod prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; the cooling head is on the right",
                       elev=16, azim=-62, size=(11, 10), dpi=150, key=True)


def vips():
    parts = [part("Floor panel 255 x 190", C["vip_floor"].shape, "#D6D3D1", (0, 0, 0)),
             part("Front panel 255 x 136.5", C["vip_front"].shape, "#C7C2BD", (0, -90, 30)),
             part("Back panel 255 x 136.5", C["vip_back"].shape, "#C7C2BD", (0, 90, 30)),
             part("Battery end panel 140 x 136.5", C["vip_endm"].shape, "#E7E5E4", (-100, 0, 30)),
             part("Cooling end, lower 140 x 68", C["vip_endlo"].shape, "#E7E5E4", (100, 0, 30)),
             part("Foam strip, cut round the pipes", C["foam"].shape, COL["foam"], (100, 0, 70)),
             part("Cooling end, upper 140 x 40.5", C["vip_endhi"].shape, "#E7E5E4", (100, 0, 110)),
             part("Lid plug 204 x 139", C["vip_lid"].shape, "#D6D3D1", (0, 0, 170))]
    return bv.overview(parts, OUT / "vip-panels.png", "Vacuum-insulated panels: the seven bought panels and the foam strip",
                       subtitle="All 25 mm thick, sizes in mm. Ordered to size: never cut, drill or pierce a VIP",
                       elev=22, azim=-58, size=(10, 7), dpi=150)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    base = dict(project="ColdPod", date=DATE)
    M = made()
    g = lambda *ks: [part(C[k].name, C[k].shape, "#D1D5DB") for k in ks]  # noqa: E731
    specs = []
    sx, ez = L["sh_x"], P["pipe_exit_z"]

    specs.append((101, dict(
        part=part("Outer shell", C["shell"].shape, COL["shell"]), neighbours=g(*VIPS, "head", "bay", "lid"),
        title="ColdPod outer shell: making sketch", material="PETG or ASA, 3D printed, 4 perimeters, 25 % infill",
        inset_view=(22, -50),
        notes=["Print as one tub, open side up: 261 x 196 x 164.5 mm outside the walls",
               "  (275 x 204 over pads and towers), 3 mm walls and floor. Needs a",
               "  printer bed of at least 300 x 300 mm.",
               "Cooling end (right): two pipe slots 10 wide, 25 each side of the centre,",
               "  and a cable slot 6 wide, 40 toward the front, each open at the rim and",
               "  ending in a half-round at 114 up.",
               "Pads 14 x 16 x 4 proud on both end faces, 89 each side of centre,",
               "  centred 40 and 145 up; one M3 heat-set insert in each.",
               "Two towers 10 x 10 x 10 on the cooling end, 44 each side, 126 up; M3 insert.",
               "Handle pads 20 dia x 4 at the middle of front and back, 136 up; M5 insert.",
               "Latch pads 20 x 16 x 4 on the front, 72 each side, 142 to 158 up; 2 x M3.",
               "Set every insert with the soldering iron before any VIP goes in.",
               "No screw or drill may ever go through a wall: a VIP sits behind it.",
               "Check: the inside is 255 x 190, square, within 0.5 mm."])))
    specs.append((102, dict(
        part=part("Evaporator can", C["can"].shape, COL["can"]), neighbours=g("vip_floor", "loop"),
        title="ColdPod evaporator can: making sketch", material="Aluminium sheet 1.0 mm, 5052 or 3003",
        inset_view=(28, -50),
        notes=["Open box 205 x 140 x 95 mm outside, 1.0 mm sheet, folded from one",
               "  cross-shaped blank by a sheet metal shop; TIG weld the four corners.",
               "Fold a 5 mm flange inward all round the rim, last. It is the landing",
               "  for the lid cold plate tray and must be flat within 0.3 mm.",
               "Cooling end wall: two riser slots 9 wide, 25 each side of centre,",
               "  open at the rim and running down to 67.5 mm above the floor.",
               "Cable hole 6 mm, 40 toward the front, 86 up; fit a grommet.",
               "Deburr every edge: the pouches must not be cut.",
               "Fit: stands on the VIP floor panel; its walls touch the VIP walls.",
               "Check: the inside is 203 x 138 and square; the rim flange lies flat."])))
    specs.append((103, dict(
        part=part("Loop thermosiphon", C["loop"].shape, COL["loop"]), neighbours=g("block", "vip_floor"),
        title="ColdPod loop thermosiphon: bending sketch", material="Soft copper refrigeration tube 8 x 0.5 mm",
        inset_view=(28, -50),
        notes=["Evaporator ring: a closed rectangle 195 x 130 mm on the tube centre line,",
               "  corners bent to 25 mm radius, ends joined with a coupler, brazed.",
               "Two tees in the cooling-end run, 25 mm each side of the centre.",
               "Risers: from each tee straight up 63.5 mm, then a 90 degree bend of",
               "  17.5 mm radius (lever bender for 8 mm tube) toward the cooling end;",
               "  the tail ends 33 mm beyond the outside of the can.",
               "Braze with silver alloy, nitrogen purge; clean and cap the open ends.",
               "Fit: the ring lies in the bottom inside corner of the can, touching",
               "  floor and wall, bonded with thermally conductive epoxy; the risers",
               "  drop down the can's open slots; the tails go into the cold block.",
               "A refrigeration technician leak tests, evacuates and charges the loop.",
               "Check: the ring lies flat on a table within 1 mm."])))
    specs.append((104, dict(
        part=part("Cold block", S("block", "charge"), COL["block"]), neighbours=g("loop", "tec", "can"),
        title="ColdPod cold block: making sketch", material="Aluminium 6061, 10 x 60 x 44 mm",
        view_shape=C["block"].shape, inset_view=(20, -35),
        notes=["Mill a block 10 x 60 x 44 mm; lap the front face flat (Peltier side).",
               "Back face (against the shell): two tube sockets 8.1 mm, 5 deep, 25",
               "  each side of centre, 10 up from the bottom edge.",
               "Condensing passage: 6 mm, drilled from the back-side end face, 5 mm",
               "  in from the back face and 10 up, through both sockets.",
               "Front face: two M3 tapped holes 8 deep, 24.5 each side, 22 up.",
               "Join the loop tails into the sockets and a 6 mm copper charge stub",
               "  into the passage mouth with aluminium-to-copper brazing rod.",
               "After charging, the stub is pinched shut and brazed.",
               "Fit: back face flat on the shell end, over the slot fillers; held by",
               "  the block frame (CPD-DWG-109). Wrap its edges in foam tape.",
               "Check: front face flat within 0.05 mm."])))
    specs.append((105, dict(
        part=part("Slot fillers", C["fillers"].shape, COL["fillers"]), neighbours=g("shell", "loop", "block"),
        title="ColdPod slot fillers (make 3): making sketch", material="PETG, 3D printed, 100 % infill",
        view_shape=C["fillers"].shape, inset_view=(15, -30),
        notes=["Two pipe fillers 3 x 10 mm and one cable filler 3 x 6 mm, each 50.5",
               "  tall, with a half-round notch at the bottom: 9 mm across for the",
               "  pipes, 6 mm for the cable.",
               "Print lying flat.",
               "Fit: slide each filler down its shell slot onto the pipe or cable",
               "  after the foam strip and the upper VIP end panel are in. Glue the",
               "  sides with a bead of silicone; the outer face is flush with the shell.",
               "Check: flush within 0.3 mm, so the cold block sits flat on it."])))
    specs.append((106, dict(
        part=part("Liner", C["liner"].shape, COL["liner"]), neighbours=g("feet", "collar", "rack", "can"),
        title="ColdPod liner: making sketch", material="Aluminium sheet 1.5 mm, 5052",
        inset_view=(28, -50),
        notes=["Open box 175 x 110 x 80 mm outside, 1.5 mm sheet, folded from one",
               "  blank by a sheet metal shop; TIG weld the four corners.",
               "Cable hole 6 mm in the cooling-end wall, 40 toward the front, 71 up;",
               "  fit a grommet.",
               "Deburr all edges; round the top edge so it cannot cut a hand.",
               "Glue the four feet under it and the collar round its top",
               "  (CPD-DWG-107) with two-part epoxy.",
               "Clip the liner probe inside the back wall and the 3 degree cut-out",
               "  inside the cooling-end wall (thermal paste under each).",
               "Fit: stands on its feet on the can floor; the collar centres it",
               "  inside the can's rim flange with 0.5 mm all round.",
               "Check: inside 172 x 107 x 78.5; the top edge flat within 0.3 mm."])))
    specs.append((107, dict(
        part=part("Liner feet and collar", S("feet", "collar"), COL["feet"]), neighbours=g("liner", "can"),
        title="ColdPod liner feet (make 4) and collar: making sketch", material="PETG, 3D printed, 100 % infill",
        inset_view=(28, -50),
        notes=["Feet: four blocks 12 x 12 x 14 mm.",
               "Collar: a frame 192 x 127 mm outside, 175 x 110 inside, 4 mm tall.",
               "Print the collar flat. It insulates: never use metal here.",
               "Fit: glue a foot under each corner of the liner, 8 mm in from both",
               "  edges. Glue the collar round the liner with its top flush with the",
               "  liner's top edge.",
               "The feet stand on the can floor and keep the liner 14 mm above it;",
               "  the floor pouch has a relief at each foot.",
               "Check: the liner stands level on its feet within 0.5 mm."])))
    specs.append((108, dict(
        part=part("Payload rack", C["rack"].shape, COL["rack"]), neighbours=g("liner", "probe"),
        title="ColdPod payload rack: making sketch", material="PETG, 3D printed",
        inset_view=(28, -50),
        notes=["Floor 170 x 105 x 2 mm with two dividers 2 mm thick and 60 tall,",
               "  17 mm each side of the centre, running the full length.",
               "Holds 24 pens of 16 mm, three pairs across and four layers up.",
               "Print floor down.",
               "Fit: drops into the liner with 1 mm all round.",
               "The payload probe vial (10 x 40 mm) lies across the top layer at the",
               "  cooling end, held by its clip on the liner end wall.",
               "Check: a 16 mm rod slides freely between each divider and the wall."])))
    specs.append((109, dict(
        part=part("Block frame and drip tray", C["frame"].shape, COL["frame"]), neighbours=g("block", "tec", "can", "loop"),
        title="ColdPod block frame and drip tray: making sketch", material="PETG, 3D printed, 100 % infill",
        view_shape=C["frame"].shape, inset_view=(20, -35),
        notes=["Plate 98 x 52 x 3.5 mm with a 42 x 42 window for the Peltier module.",
               "Four 3.5 mm holes 26 up from the bottom edge: two at 24.5 each side",
               "  (module clamp screws pass) and two at 44 each side (frame screws).",
               "Drip tray along the bottom edge: floor 68 x 13.5 x 2 mm with 2 mm",
               "  lips at both ends, reaching back to the shell.",
               "Drain hole 5 mm, 3.5 mm from the shell end, 30 toward the front.",
               "The plate is thinner than the module (4 mm), so the clamp force goes",
               "  through the module, not the frame.",
               "Fit: plate on the block's front rim; M3 screws into the shell towers.",
               "Check: 0.5 mm gap between the plate and the heat sink."])))
    specs.append((110, dict(
        part=part("Cooling head housing", C["head"].shape, COL["head"]), neighbours=g("shell", "sink", "fan", "power"),
        title="ColdPod cooling head housing: making sketch", material="PETG or ASA, 3D printed, 2 mm walls",
        inset_view=(24, -40),
        notes=["Box 60 x 160 x 169.5 mm, 2 mm walls, open on the shell side.",
               "End wall: seven grille slots 70 x 5 at 10 mm pitch from 94 up; 12 V",
               "  socket hole 12 mm and USB-C slot 9 x 5, both 40 up, 20 each side.",
               "Front: five intake slots 5 x 40, from 30 up. Floor: 5 mm drain hole",
               "  3.5 from the shell end, 30 toward the front; four 3.4 mm holes for",
               "  the power board standoffs, 11 from each end, 62 each side.",
               "Back wall: notch 8 x 12 at the shell end, 6 up, for the cable duct.",
               "Four ears 3 mm thick on the side walls, 3.4 mm holes at 89 each side,",
               "  40 and 145 up.",
               "Fit: open edge against the shell end; four M3 screws through the",
               "  ears into the shell pads.",
               "Check: the ears sit flat on all four pads at once."])))
    specs.append((111, dict(
        part=part("Cell cradle", C["cradle"].shape, COL["cradle"]), neighbours=g("cells", "bay"),
        title="ColdPod cell cradle: making sketch", material="PETG, 3D printed",
        inset_view=(28, -50),
        notes=["Block 36 x 140 x 12 mm with four pockets 32.4 mm across and",
               "  10 deep on a 34 mm pitch; 2 mm floor under each pocket.",
               "Drill two 3.4 mm screw holes between the middle pockets for the bay floor.",
               "Fit: screwed to the bay floor against the end wall; the four cells",
               "  stand in the pockets, the BMS sits on top of them, and a hook and",
               "  loop strap holds the pack down.",
               "Check: each cell drops in without force and does not rattle."])))
    specs.append((112, dict(
        part=part("Battery bay housing", C["bay"].shape, COL["bay"]), neighbours=g("shell", "cells", "cradle", "logger"),
        title="ColdPod battery bay housing: making sketch", material="PETG or ASA, 3D printed, 2 mm walls",
        inset_view=(24, -130),
        notes=["Box 45 x 160 x 169.5 mm, 2 mm walls, open on the shell side.",
               "End wall: four vent slots 60 x 4 from 30 up.",
               "Top: display window 26 x 60, 9 mm from the end wall; 10.4 mm hole",
               "  for the alarm light, 22 from the end wall, 50 toward the back.",
               "Back wall: notch 8 x 12 at the shell end, 6 up, for the cable duct;",
               "  four 3.4 mm holes for the logger standoffs.",
               "Four ears like the cooling head's, mirrored.",
               "Fit: four M3 screws through the ears into the shell pads.",
               "Check: the display window lines up with the display's active area."])))
    specs.append((113, dict(
        part=part("Cable duct cover", C["duct"].shape, COL["duct"]), neighbours=g("shell", "head", "bay"),
        title="ColdPod cable duct cover: making sketch", material="PETG, 3D printed",
        inset_view=(20, 130),
        notes=["A U-channel 8 deep x 12 tall with 1.5 mm walls, open toward the",
               "  shell: 261 mm along the back face, turning 26 mm along each end face.",
               "Print in three pieces (back run and two corners) and glue them.",
               "Fit: lay the battery and sensor leads along the back face 6 to 18 mm",
               "  up, then glue the cover over them with silicone along both edges.",
               "  Each end turns into the notch in its housing's back wall.",
               "Check: no wire is pinched under an edge."])))
    specs.append((114, dict(
        part=part("Lid cold plate tray", C["lidplate"].shape, COL["lidplate"]), neighbours=g("vip_lid", "lid"),
        title="ColdPod lid cold plate tray: making sketch", material="Aluminium sheet 1.5 mm, 5052",
        inset_view=(-20, -50),
        notes=["A shallow tray 204 x 139 mm outside, 16.5 mm deep, folded from one",
               "  1.5 mm blank; the corners are notched and left open.",
               "Fold a 6 mm lip inward all round the top edge.",
               "Bottom flat within 0.3 mm: it lands on the can's rim flange.",
               "Fit: the lid PCM pack goes in through the lip opening; the lip is",
               "  bonded to the underside of the VIP lid plug with acrylic foam tape.",
               "  The bottom lands on the can's rim flange with 5.5 mm of overlap.",
               "Check: 0.5 mm all round between the tray and the VIP walls."])))
    specs.append((115, dict(
        part=part("Lid cap", C["lid"].shape, COL["lid"]), neighbours=g("shell", "latches", "vip_lid"),
        title="ColdPod lid cap: making sketch", material="PETG or ASA, 3D printed, 4 perimeters",
        inset_view=(24, -50),
        notes=["Slab 261 x 196 x 5 mm.",
               "Two M3 heat-set inserts per latch keeper on the top, 72 each side of",
               "  centre, 5 mm in from the front edge; insert depth 4 mm at most.",
               "6 mm magnet pocket in the cooling-end edge for the lid switch.",
               "Underside: bond a closed-cell EPDM strip 10 x 3 mm all round over the",
               "  shell rim, and the VIP lid plug in the middle (acrylic foam tape).",
               "Fit: sits on the shell rim; the two draw latches pull it down.",
               "Check: the gasket touches the rim all round before the latches close."])))

    out = []
    for n, kw in specs:
        if only and n not in only:
            continue
        out.append(bv.component_sheet(dwg_no=f"CPD-DWG-{n}", **kw, **base))
    return out


# ----------------------------------------------------------------- joints
def _win(shape, box_):
    import build123d as b
    x0, x1, y0, y1, z0, z1 = box_
    return shape & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def joints(only=None):
    out = []
    jobs = {
        1: ((84, 112, -10, 10, 20, 56), [("Evaporator can", "can", COL["can"]), ("Loop, bonded in the corner", "loop", COL["loop"]),
            ("VIP floor panel", "vip_floor", COL["vip"]), ("VIP end panel, lower", "vip_endlo", "#E7E5E4"),
            ("PCM pouches", "pcm_jacket", COL["pcm"]), ("Liner", "liner", COL["liner"])],
            "Joint 1: the loop in the bottom corner of the can (cut at the cooling end)",
            "Cut on the centre line, seen from the front. The tube touches the can floor and wall, bonded with thermal epoxy",
            dict(elev=4, azim=-90)),
        2: ((84, 142, 25, 40, 88, 132), [("Evaporator can", "can", COL["can"]), ("Riser and tail", "loop", COL["loop"]),
            ("Foam strip", "foam", COL["foam"]), ("VIP end panel, lower", "vip_endlo", "#E7E5E4"), ("VIP end panel, upper", "vip_endhi", "#D6D3D1"),
            ("Shell", "shell", COL["shell"]), ("Slot filler", "fillers", COL["fillers"]), ("Cold block", "block", COL["block"]),
            ("Liner and collar", ("liner", "collar"), COL["liner"])],
            "Joint 2: riser through the can slot, foam strip and shell slot into the block",
            "Cut through the riser, seen from the front. The bend lies in the foam strip, clear of the lower VIP panel",
            dict(elev=4, azim=-90)),
        3: ((128, 158, -52, 52, 98, 126), [("Shell and towers", "shell", COL["shell"]), ("Cold block", "block", COL["block"]),
            ("Block frame", "frame", COL["frame"]), ("Peltier module", "tec", COL["tec"]), ("Heat sink", "sink", COL["sink"]),
            ("M3 clamp and frame screws", "screws", COL["screws"])],
            "Joint 3: cold block, Peltier module, frame and heat sink",
            "Cut level with the screws, seen from above. The frame holds the block to the towers; two screws clamp the module",
            dict(elev=89, azim=-90)),
        4: ((60, 106, 47, 75, 26, 142), [("Evaporator can with rim flange", "can", COL["can"]), ("Liner", "liner", COL["liner"]),
            ("Liner foot", "feet", COL["feet"]), ("Collar", "collar", COL["feet"]), ("PCM jacket", "pcm_jacket", COL["pcm"]),
            ("Lid tray", "lidplate", COL["lidplate"]), ("Lid PCM pack", "pcm_lid", "#93C5FD"), ("VIP back panel", "vip_back", "#E7E5E4")],
            "Joint 4: liner on its foot, collar and the lid tray landing on the can flange",
            "Cut through a foot, seen from the front. The tray lands on the flange, the collar and the liner rim",
            dict(elev=6, azim=-90)),
        5: ((80, 135, -6, 6, 112, 172), [("Shell", "shell", COL["shell"]), ("VIP end panel", "vip_endhi", "#E7E5E4"),
            ("Evaporator can flange", "can", COL["can"]), ("Lid tray", "lidplate", COL["lidplate"]),
            ("Lid PCM pack", "pcm_lid", COL["pcm"]), ("VIP lid plug", "vip_lid", COL["vip"]), ("Lid cap", "lid", COL["lid"]),
            ("Liner and collar", ("liner", "collar"), COL["liner"])],
            "Joint 5: the lid stack at the cooling end",
            "Cut on the centre line, seen from the front. Cap, plug and tray come off as one; the tray lands on the can flange",
            dict(elev=5, azim=-90)),
        6: ((126, 145, 70, 100, 28, 52), [("Shell pad with M3 insert", "shell", COL["shell"]), ("Cooling head ear", "head", COL["head"])],
            "Joint 6: cooling head ear on a shell pad (back, lower)",
            "One M3 screw through the ear into the insert; the head's open edge sits flat on the shell end",
            dict(elev=20, azim=-30)),
        7: ((-100, 14, -165, -88, 120, 175), [("Shell front wall", "shell", COL["shell"]), ("Pads with inserts (pivot and latch)", "PADS", "#0F766E"),
            ("Handle arm, pulled forward", "HANDLE", COL["handle"]), ("Draw latch, pulled forward", "LATCH", COL["latches"]),
            ("Lid cap", "lid", COL["lid"])],
            "Joint 7: handle pivot and draw latch on their pads (front, left half)",
            "Arm and latch drawn pulled off their pads. Pivot: one M5 screw into the pad insert; latch: two M3 screws",
            dict(elev=18, azim=-35)),
        8: ((128, 146, -30, 40, 0, 108), [("Block frame and drip tray", "frame", COL["frame"]), ("Drain tube", "drain", COL["drain"]),
            ("Cold block", "block", COL["block"]), ("Head housing (floor and front)", "head", COL["head"]),
            ("Power board and standoffs", ("power", "power_so"), COL["power"]), ("Shell", "shell", COL["shell"])],
            "Joint 8: drip tray and drain tube, cut through the drain",
            "Water from the cold block runs into the tray and down the tube through the head floor, clear of the board",
            dict(elev=10, azim=-80)),
        9: ((118, 150, 66, 112, 0, 30), [("Shell", "shell", COL["shell"]), ("Cable duct cover", "duct", COL["duct"]),
            ("Cooling head housing", "head", COL["head"])],
            "Joint 9: cable duct cover turning into the cooling head",
            "The cover runs along the back face, turns onto the shell end and enters the notch in the head's back wall",
            dict(elev=25, azim=40)),
    }
    for n, (box_, items, title, sub, kw) in jobs.items():
        if only and n not in only:
            continue
        ps = []
        for name, k, col in items:
            if k == "PADS":
                sh = _win(C["shell"].shape, (-200, 200, -L["sh_y"] - P["pad_t"], -L["sh_y"], 0, 200))
            elif k == "HANDLE":
                sh = Pos(0, -40, 0) * C["handle"].shape
            elif k == "LATCH":
                sh = Pos(0, -20, 0) * _win(C["latches"].shape, (-200, 200, -200, -L["sh_y"] - 0.01, 0, 200))
            elif k == "shell" and n == 7:
                sh = _win(C["shell"].shape, (-200, 200, -L["sh_y"], 0, 0, 200))
            else:
                sh = S(*k) if isinstance(k, tuple) else C[k].shape
            ps.append(part(name, _win(sh, box_), col))
        if n == 2:      # cut through the riser centre line
            ps = [part(p.name, _win(p.shape, (84, 142, 25, 40, 88, 132)), p.color) for p in ps]
        out.append(bv.joint(ps, OUT / f"joint-{n:02d}.png", title, subtitle=sub, size=(8, 6), **kw))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        if only and n not in only:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    sh = M["shell"]
    shell_only = part("Outer shell", C["shell"].shape, COL["shell"])
    vip5 = [part("VIP floor", C["vip_floor"].shape, COL["vip"])]
    vipw = part("VIP walls: front, back, battery end, lower cooling end", S("vip_front", "vip_back", "vip_endm", "vip_endlo"), COL["vip"])
    st(1, [shell_only], [mv(vip5[0], (0, 0, 160)), mv(vipw, (0, 0, 260))], "VIP panels into the shell",
       "Inserts set first. Floor panel, then the four walls, on acrylic foam tape. Never cut or pierce a VIP",
       elev=24, azim=-58, label_done=False)
    can = part("Evaporator can", C["can"].shape, COL["can"])
    st(2, [can], [mv(part("Loop thermosiphon", C["loop"].shape, COL["loop"]), (0, 0, 120))], "loop into the can",
       "Lower the ring in, risers down the open slots; bond the ring into the bottom corner with thermal epoxy",
       elev=28, azim=-58, label_done=True)
    canloop = part("Can and loop", S("can", "loop"), COL["can"])
    st(3, [canloop], [mv(part("Cold block and charge stub", S("block", "charge"), COL["block"]), (60, 0, 0))],
       "cold block onto the tails, then charge",
       "Braze the tails into the sockets with aluminium-to-copper rod; leak test, evacuate, charge, pinch the stub",
       elev=20, azim=-50, label_done=True)
    box_done = [sh, part("VIP floor and walls", S(*VIPS), COL["vip"])]
    evap = part("Evaporator assembly (can, loop, block)", S("can", "loop", "block", "charge"), COL["can"])
    st(4, [shell_only, part("VIP floor and walls", S(*VIPS), COL["vip"])], [mv(evap, (0, 0, 200))], "evaporator assembly into the VIP box",
       "Lower it straight down: the tails drop down the shell's open slots and the block hangs outside the end",
       elev=24, azim=-50, label_done=False)
    after4 = [shell_only, part("VIP floor and walls", S(*VIPS), COL["vip"]), evap]
    st(5, after4, [mv(M["foam"], (0, 0, 90)), mv(part("VIP end panel, upper", C["vip_endhi"].shape, COL["vip"]), (0, 0, 160)),
                   mv(part("Slot fillers (3)", C["fillers"].shape, COL["fillers"]), (40, 0, 120))],
       "foam strip, upper end panel and slot fillers",
       "Foam pieces cut round the pipes; upper VIP panel on top; fillers slid down the slots and sealed with silicone",
       elev=26, azim=-40, label_done=False)
    vipall = part("VIP panels and foam", S(*VIPS, "vip_endhi", "foam"), COL["vip"])
    after5 = [sh, vipall, evap]
    st(6, after5, [mv(M["jacket"], (0, 0, 200))], "PCM pouches into the can",
       "Floor pouch first (reliefs at the liner feet), then sides and ends; three narrow pouches round the risers",
       elev=30, azim=-58, label_done=False)
    st(7, [part("Liner", C["liner"].shape, COL["liner"])],
       [mv(part("Feet (4)", C["feet"].shape, COL["feet"]), (0, 0, -60)), mv(part("Collar", C["collar"].shape, COL["feet"]), (0, 0, 70)),
        mv(part("Liner probe, cut-out and sensor cable", S("liner_probe", "cutout", "cable"), COL["sensors"]), (0, 0, 100))],
       "liner sub-assembly",
       "Glue the feet and collar on with epoxy; clip the liner probe and cut-out inside; cable through the grommet",
       elev=24, azim=-58, label_done=True)
    after6 = after5 + [part("PCM jacket", C["pcm_jacket"].shape, COL["pcm"])]
    liner_sa = part("Liner with feet, collar, probes and cable", S("liner", "feet", "collar", "liner_probe", "cutout", "cable"), COL["liner"])
    st(8, after6, [mv(liner_sa, (0, 0, 220))], "liner into the can",
       "Feed the cable through the can grommet and the cable slot first, then lower the liner onto its feet",
       elev=30, azim=-58, label_done=False)
    after8 = after6 + [liner_sa]
    st(9, after8, [mv(M["rack"], (0, 0, 200))], "rack and payload probe into the liner",
       "The rack drops in; clip the probe vial to the liner end wall above the top layer of pens",
       elev=34, azim=-58, label_done=False)
    after9 = after8 + [M["rack"]]
    st(10, after9, [mv(M["frame"], (80, 0, 0))], "block frame and drip tray onto the towers",
       "Two M3 screws into the tower inserts; push the drain tube into the tray's hole from below",
       elev=20, azim=-35, label_done=False)
    after10 = after9 + [M["frame"]]
    st(11, after10, [mv(M["tec"], (70, 0, 0)), mv(part("Heat sink and two clamp screws", S("sink", "screws"), COL["sink"]), (170, 0, 0))],
       "Peltier module and heat sink onto the block",
       "Thin paste on both faces, cold side to the block; two M3 screws through the sink, tightened evenly",
       elev=20, azim=-35, label_done=False)
    after11 = after10 + [M["tec"], part("Heat sink", S("sink", "screws"), COL["sink"])]
    st(12, after11, [mv(part("Fan and finger guard", S("fan", "guard"), COL["fan"]), (80, 0, 0))], "fan and guard onto the sink",
       "Airflow out through the grille; four fan screws into the gaps between the fins",
       elev=20, azim=-35, label_done=False)
    st(13, [part("Cooling head housing", C["head"].shape, COL["head"])],
       [mv(part("Standoffs and power board", S("power_so", "power"), COL["power"]), (0, 0, 80)),
        mv(part("12 V and USB-C inlets", C["inlets"].shape, COL["sensors"]), (60, 0, 0)),
        mv(part("Ambient sensor", C["ambient"].shape, COL["sensors"]), (0, -60, 0))],
       "build the cooling head",
       "Standoffs into the floor, board on them; inlets into the end wall; ambient sensor cap on the front",
       elev=30, azim=-130, label_done=True)
    after12 = after11 + [part("Fan and guard", S("fan", "guard"), COL["fan"])]
    head_sa = part("Cooling head with board and inlets", S("head", "power", "power_so", "inlets", "ambient"), COL["head"])
    st(14, after12, [mv(head_sa, (140, 0, 0))], "cooling head onto the shell",
       "Wire the board first (wiring diagram); then four M3 screws through the ears into the shell pads",
       elev=20, azim=-40, label_done=False)
    st(15, [part("Battery bay housing", C["bay"].shape, COL["bay"])],
       [mv(part("Cell cradle, cells and BMS", S("cradle", "cells"), COL["cells"]), (130, 0, 0)),
        mv(part("Logger on standoffs", S("logger", "logger_so"), COL["logger"]), (70, -40, 0)),
        mv(part("Display and alarm light", S("display", "alarm"), COL["display"]), (90, 0, -40))],
       "build the battery bay",
       "Cradle screwed to the floor, cells in, BMS on top, strap; logger on the back wall; display under its window",
       elev=28, azim=-50, label_done=True)
    after14 = after12 + [head_sa]
    bay_sa = part("Battery bay with cells, logger and display", S("bay", "cradle", "cells", "logger", "logger_so", "display", "alarm"), COL["bay"])
    st(16, after14, [mv(bay_sa, (-140, 0, 0))], "battery bay onto the shell",
       "Fuse out. Connect the duct leads, then four M3 screws through the ears into the shell pads",
       elev=20, azim=-130, label_done=False)
    after16 = after14 + [bay_sa]
    st(17, after16, [mv(M["duct"], (0, 90, 0))], "cable duct cover onto the back face",
       "Seen from the back. Leads laid 6 to 18 mm up; cover glued with silicone along both edges",
       elev=22, azim=120, label_done=False)
    after17 = after16 + [M["duct"]]
    st(18, after17, [mv(part("Bail handle", C["handle"].shape, COL["handle"]), (0, 0, 120)),
                     mv(part("Draw latches (2)", C["latches"].shape, COL["latches"]), (0, -80, 0))],
       "handle and latches",
       "Handle on two M5 pivot screws with the strap D-rings under the heads; latches on two M3 screws each",
       elev=20, azim=-58, label_done=False)
    st(19, [part("Lid cap", C["lid"].shape, COL["lid"])],
       [mv(part("VIP lid plug", C["vip_lid"].shape, COL["vip"]), (0, 0, -90)),
        mv(part("Lid tray with the lid PCM pack", S("lidplate", "pcm_lid"), COL["lidplate"]), (0, 0, -170))],
       "build the lid",
       "Shown right way up from below. Plug onto the cap with foam tape; pack into the tray; tray lip onto the plug",
       elev=-25, azim=-58, label_done=True)
    lid_sa = part("Lid with plug and tray", S("lid", "vip_lid", "lidplate", "pcm_lid"), COL["lid"])
    after18 = after17 + [part("Handle and latches", S("handle", "latches"), COL["handle"])]
    st(20, [p for p in after18 if p.name != "Handle and latches"] + [part("Latches", C["latches"].shape, COL["latches"])],
       [mv(lid_sa, (0, 0, 160))], "lid on",
       "Handle folded down to one side. Lower the lid straight down and close both latches",
       elev=24, azim=-58, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 76); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 74, "ColdPod prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 70.6, "Bought modules on perfboard, wired at block level; no circuit board is laid out. Stranded copper; ferrules on every screw terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/coldpod", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((44, 9), 74, 56, boxstyle="round,pad=0.4", fc="#F0FDFA", ec="#0E7490", lw=1, ls="--"))
    ax.text(45.5, 64, "In the cooling head (right end)", fontsize=8, color="#0E7490", va="top")
    ax.add_patch(FancyBboxPatch((2, 9), 32, 56, boxstyle="round,pad=0.4", fc="#FFF7ED", ec="#C2410C", lw=1, ls="--"))
    ax.text(3.5, 64, "In the battery bay (left end)", fontsize=8, color="#C2410C", va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.6, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.1, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk(48, 50, 16, 11, "Inlets", "USB-C PD 20 V\n12 V, 10 to 15 V", "#D4A017")
    blk(70, 50, 20, 11, "Input and charger", "reverse-polarity guard,\nLiFePO4 4S charger", "#16A34A")
    blk(70, 33, 20, 11, "Peltier driver", "buck-boost, LC filter,\nsmooth DC", "#16A34A")
    blk(96, 50, 20, 11, "Fan driver", "12 V fan, 70 mm", "#16A34A")
    blk(96, 33, 20, 11, "Cut-outs in series", "bimetal, no firmware:\nblock -5 °C, liner 3 °C", "#B91C1C")
    blk(96, 14, 20, 12, "Peltier module", "TEC1-12703 class\non the cold block", "#64748B")
    blk(48, 14, 18, 12, "Sensors", "payload, liner, block,\nambient; lid reed", "#D4A017")
    blk(5, 46, 26, 12, "LiFePO4 pack", "4S 12.8 V 6 Ah, BMS\nwith charge temp. stop", "#C2410C")
    blk(5, 28, 26, 12, "Logger", "nRF52840 class, RTC,\n2 MB flash, 3.3 V", "#0F766E")
    blk(5, 12, 26, 11, "Display and alarm", "e-paper, buzzer,\nred and green lights", "#38BDF8")
    wire([(64, 55.5), (70, 55.5)], RED); lab(67, 57.6, "1.0 mm²", RED, "center")
    wire([(80, 50), (80, 44)], RED); lab(80.6, 47, "1.0 mm²", RED)
    wire([(90, 55.5), (96, 55.5)], RED); lab(93, 57.6, "0.25 mm²", RED, "center")
    wire([(90, 38.5), (96, 38.5)], RED); lab(93, 40.6, "0.75 mm²", RED, "center")
    wire([(106, 33), (106, 26)], RED); lab(106.6, 29.5, "0.75 mm²", RED)
    wire([(31, 52), (40, 52), (40, 66.5), (80, 66.5), (80, 61)], RED); lab(52, 68.4, "battery, 1.0 mm², 5 A fuse at the pack, through the duct", RED)
    wire([(73, 50), (73, 47.5), (37, 47.5), (37, 38), (31, 38)], RED, 1.4); lab(42, 45.6, "3.3 V and ground, 0.25 mm², through the duct", RED)
    wire([(31, 34), (70, 34)], GRY, 1.2); lab(45, 32.2, "driver enable and set point, 0.14 mm²", GRY)
    wire([(48, 20), (37, 20), (37, 30), (31, 30)], BLU, 1.4); lab(38.3, 25, "8-core cable,\n0.14 mm²,\nvia the duct", BLU)
    wire([(18, 28), (18, 23)], BLU, 1.4); lab(18.6, 25.5, "SPI and GPIO", BLU)
    ax.text(36, 6.2, "Safety: battery fuse out until the stop points in section 6 of the plan are passed. Charge the pack only between 0 and 45 °C.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(36, 3.6, "Red: power. Blue: sensor bus. Grey: control. All circuits are 20 V DC or less; no mains wiring.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def _parse(arg):
    if ":" in arg:
        k, v = arg.split(":", 1)
        return k, {int(x) for x in v.split(",")}
    return arg, None


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "vips", "sheets", "joints", "steps", "wiring"]
    fns = {"overview": overview, "vips": vips, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        k, only = _parse(w)
        r = fns[k](only) if only else fns[k]()
        print(w, "->", r)
