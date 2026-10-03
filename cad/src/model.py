"""ColdPod parametric model (build123d), TRL 3, constructable design (CPD-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks (contacts and clearances)

Exports:
    coldpod-assembly.step / .stl      whole case, lid closed, handle up
    shell.step, lid.step, vip-set.step, liner-rack.step, evaporator-thermosiphon.step,
    cooling-head.step (Peltier, sink, fan, cold block) and end-housings.step (and .stl)

Axes: X along the case length (battery and electronics bay at -X, cooling head at +X),
Y front (-Y) to back (+Y), Z up, table at Z = 0. Units mm.

Layers from the inside out: payload cavity in an aluminium liner standing on four printed
feet and centred by a printed collar; a phase-change material (PCM) jacket in sealed pouches
inside an aluminium evaporator can with a 5 mm inward rim flange; a lid PCM pack in an
aluminium cold plate tray that lands on that flange when the lid closes; seven 25 mm
vacuum-insulated panels (VIP) and a foam strip where the pipes cross; a printed shell (3 mm
walls, 5 mm lid cap, 2 mm end housings, CPD-DDR-002). The shell carries printed pads and
towers with heat-set inserts for every outside fixing, because no screw may pass through a
wall with a VIP behind it. A two-phase loop thermosiphon (evaporator loop bonded into the
bottom inside corner of the can, two bent risers through the foam strip) carries heat one
way, up and out, to an aluminium cold block on the Peltier module in the +X cooling head.

build_components() returns every component separately (the build plan draws from it);
build_parts() groups them into the 17 concept groups used by the concept media, the
appearance model and the calculation note. Not for fabrication: TRL 3 sizes only.
The same PARAMS feed docs/04-calcs/sizing.py (CPD-CAL-001).
"""
import math
import sys
from collections import namedtuple
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # payload cavity and liner (outside of the liner)
    "cav_l": 175.0, "cav_w": 110.0, "cav_h": 80.0, "liner_t": 1.5,
    "rack_t": 2.0,                            # rack floor and divider thickness
    # PCM jacket (includes the evaporator can wall) and lid pack
    "pcm_t": 15.0, "can_t": 1.0, "lid_pcm_t": 15.0,
    "can_flange": 5.0,                        # inward fold at the can rim: the landing for the lid tray (DDR-003)
    "lid_plate_t": 1.5,                       # aluminium lid cold plate, folded into a tray (DDR-003)
    "tray_clear": 0.5, "tray_lip": 6.0,       # tray clearance to the VIP opening; inward top lip bonded to the lid plug
    "foot": 12.0, "collar_h": 4.0,            # printed liner feet (on the can floor) and top collar (DDR-003)
    # insulation and shell (thinner printed parts, CPD-DDR-002)
    "vip_t": 25.0, "shell_t": 3.0, "lid_cap_t": 5.0,
    "foam_strip": 28.0, "foam_lo": 18.0,      # foam strip in the +X VIP wall where the pipes cross, from 18 below to 10 above the pipes
    "pad_t": 4.0, "pad_y": 89.0, "pad_z": (40.0, 145.0),   # printed pads with M3 inserts for the end housings
    "tower": 10.0, "tower_y": 44.0,           # printed towers for the cold block frame
    "slot_w": 10.0,                           # shell pipe slots, open to the rim (DDR-003)
    "handle_pad_z": 136.0, "latch_x": 72.0,
    # payload (not supplied): insulin pens in layers
    "pen_d": 16.0, "pen_l": 160.0, "pen_cols": 6, "pen_layers": 4,
    "probe": (10.0, 40.0),                    # buffered payload probe vial, dia x length, above the top layer (DDR-003)
    # thermosiphon (two-phase loop): 8 mm copper tube
    "pipe_d": 8.0, "pipe_y": 25.0, "loop_inset": 0.0, "pipe_exit_z": 114.0,
    "loop_r": 25.0, "riser_r": 17.5,          # bend radii of the loop corners and of the riser bends
    "socket": 5.0,                            # depth of the tube sockets in the cold block
    "cable_d": 5.0, "cable_y": -40.0,         # sensor cable out of the cavity
    # cold block, Peltier module, heat sink, fan
    "block": (10.0, 60.0, 44.0),              # aluminium, X, Y, Z; bottom at pipe_exit_z - 10
    "tec": (4.0, 40.0, 40.0),                 # 40 x 40 mm module
    "frame_t": 3.5,                           # printed block frame, thinner than the module
    "sink_base": 6.0, "sink_fin": 24.0, "sink_w": 80.0, "sink_h": 80.0, "fins": 9,
    "fan": (10.0, 70.0, 70.0),
    "tec_screw_y": 24.5,
    # end housings
    "head_l": 60.0, "bay_l": 45.0, "end_w": 160.0, "end_wall": 2.0,
    "duct": (8.0, 6.0, 18.0),                 # cable duct cover: depth, bottom, top (DDR-003)
    # battery: 4S1P 32700 LiFePO4 cells standing in the -X bay
    "cell_d": 32.0, "cell_h": 70.0, "cells": 4,
    # bail handle (up position)
    "handle_d": 16.0, "handle_top": 199.0, "handle_pivot_z": 128.0,
}

Comp = namedtuple("Comp", "name shape bom group kind")


def levels(P=PARAMS):
    """Derived half widths (X, Y) and Z levels of each layer."""
    d = {}
    d["cav_x"], d["cav_y"] = P["cav_l"] / 2, P["cav_w"] / 2
    d["pcm_x"], d["pcm_y"] = d["cav_x"] + P["pcm_t"], d["cav_y"] + P["pcm_t"]
    d["vip_x"], d["vip_y"] = d["pcm_x"] + P["vip_t"], d["pcm_y"] + P["vip_t"]
    d["sh_x"], d["sh_y"] = d["vip_x"] + P["shell_t"], d["vip_y"] + P["shell_t"]
    d["vip_z0"] = P["shell_t"]
    d["pcm_z0"] = d["vip_z0"] + P["vip_t"]
    d["cav_z0"] = d["pcm_z0"] + P["pcm_t"]
    d["cav_z1"] = d["cav_z0"] + P["cav_h"]
    d["plate_z1"] = d["cav_z1"] + P["lid_plate_t"]
    d["lidpcm_z1"] = d["plate_z1"] + P["lid_pcm_t"]
    d["rim"] = d["lidpcm_z1"] + P["vip_t"]
    d["lid_top"] = d["rim"] + P["lid_cap_t"]
    d["loop_z"] = d["pcm_z0"] + P["can_t"] + P["loop_inset"] + P["pipe_d"] / 2
    d["block_z0"] = P["pipe_exit_z"] - 10.0
    d["block_zc"] = d["block_z0"] + P["block"][2] / 2
    d["head_x1"] = d["sh_x"] + P["head_l"]
    d["bay_x0"] = -d["sh_x"] - P["bay_l"]
    d["loop_x"] = d["pcm_x"] - P["can_t"] - P["loop_inset"] - P["pipe_d"] / 2
    d["loop_y"] = d["pcm_y"] - P["can_t"] - P["loop_inset"] - P["pipe_d"] / 2
    d["tube_end_x"] = d["sh_x"] + P["socket"]
    return d


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _tube(p1, p2, r):
    from build123d import Solid, Plane, Vector
    v = Vector(*p2) - Vector(*p1)
    return Solid.make_cylinder(r, v.length, Plane(origin=p1, z_dir=v))


def _xcyl(x0, x1, y, z, r):
    return _tube((x0, y, z), (x1, y, z), r)


def _ycyl(x, y0, y1, z, r):
    return _tube((x, y0, z), (x, y1, z), r)


def _zcyl(x, y, z0, z1, r):
    return _tube((x, y, z0), (x, y, z1), r)


def _sweep(points, r, bend, close=False):
    """Round tube of radius r along a polyline with bends of radius `bend`."""
    import build123d as b
    path = b.FilletPolyline(*points, radius=bend, close=close)
    e0 = path.edges()[0]
    sec = b.Plane(origin=e0.position_at(0), z_dir=e0.tangent_at(0)) * b.Circle(r)
    return b.sweep(sec, path=path)


def _fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def loop_paths(P=PARAMS):
    """Centre lines of the loop thermosiphon: the closed evaporator ring and the two risers."""
    L = levels(P)
    lx, ly, lz, ez = L["loop_x"], L["loop_y"], L["loop_z"], P["pipe_exit_z"]
    ring = [(lx, -ly, lz), (lx, ly, lz), (-lx, ly, lz), (-lx, -ly, lz)]
    risers = [[(lx, y, lz), (lx, y, ez), (L["tube_end_x"], y, ez)] for y in (-P["pipe_y"], P["pipe_y"])]
    return ring, risers


def build_components(P=PARAMS):
    """Every component of the constructable design, in build order groups."""
    from build123d import Cylinder, Pos, Rot
    L = levels(P)
    B = _box
    C = {}

    def add(key, name, shape, bom, group, kind="made"):
        C[key] = Comp(name, shape, bom, group, kind)

    cx, cy, px, py = L["cav_x"], L["cav_y"], L["pcm_x"], L["pcm_y"]
    vx, vy, sx, sy = L["vip_x"], L["vip_y"], L["sh_x"], L["sh_y"]
    ez, r = P["pipe_exit_z"], P["pipe_d"] / 2
    ct, fl = P["can_t"], P["can_flange"]
    rim, top = L["rim"], L["lid_top"]
    pt = P["pad_t"]
    zc = L["block_zc"]
    ew, wt = P["end_w"] / 2, P["end_wall"]
    hx1, bx0 = L["head_x1"], L["bay_x0"]
    rc = P["cable_d"] / 2
    yc = P["cable_y"]
    pipes_y = (-P["pipe_y"], P["pipe_y"])

    # ---- loop thermosiphon centre lines (needed for holes in the can and the foam)
    ring, risers = loop_paths(P)

    def loop_solid(rr):
        s = _sweep(ring, rr, P["loop_r"], close=True)
        for pts in risers:
            s += _sweep(pts, rr, P["riser_r"])
        return s

    # ---- 1 Outer shell: open-topped tub, pipe and cable slots open to the rim, printed pads and towers
    shell = B(-sx, sx, -sy, sy, 0, rim) - B(-vx, vx, -vy, vy, P["shell_t"], rim + 1)
    sw = P["slot_w"] / 2
    slots = []
    for y, rs in ((pipes_y[0], sw), (pipes_y[1], sw), (yc, rc + 0.5)):
        slots.append((y, rs))
        shell -= _xcyl(vx - 1, sx + 1, y, ez, rs) + B(vx - 1, sx + 1, y - rs, y + rs, ez, rim + 1)
    for sgn in (1, -1):                                   # pads for the end housing ears
        for y in (P["pad_y"], -P["pad_y"]):
            for z in P["pad_z"]:
                x0, x1 = (sx, sx + pt) if sgn > 0 else (-sx - pt, -sx)
                shell += B(x0, x1, y - 7, y + 7, z - 8, z + 8)
    tw = P["tower"]
    for y in (P["tower_y"], -P["tower_y"]):                # towers for the cold block frame
        shell += B(sx, sx + tw, y - tw / 2, y + tw / 2, zc - tw / 2, zc + tw / 2)
    for ys in (-1, 1):                                      # handle pivot pads, front and back
        shell += _ycyl(0, ys * sy, ys * (sy + pt), P["handle_pad_z"], 10)
    for x in (-P["latch_x"], P["latch_x"]):                 # draw latch pads, front
        shell += B(x - 10, x + 10, -sy - pt, -sy, 142, 158)
    add("shell", "Outer shell", shell, 1, "shell")

    fillers = None
    for y, rs in slots:
        rt_ = (r if abs(y - yc) > 1e-6 else rc) + 0.5
        f = B(vx, sx, y - rs, y + rs, ez, rim) - _xcyl(vx - 1, sx + 1, y, ez, rt_)
        fillers = f if fillers is None else fillers + f
    add("fillers", "Slot fillers (3)", fillers, 17, "shell")

    # ---- 4 VIP set: seven panels bought to size, plus the cut foam strip
    z0v, z1v = L["vip_z0"], rim
    zp = L["pcm_z0"]
    f_lo, f_hi = ez - P["foam_lo"], ez - P["foam_lo"] + P["foam_strip"]
    add("vip_floor", "VIP floor panel", B(-vx, vx, -vy, vy, z0v, zp), 4, "vip", "bought")
    add("vip_front", "VIP front panel", B(-vx, vx, -vy, -py, zp, z1v), 4, "vip", "bought")
    add("vip_back", "VIP back panel", B(-vx, vx, py, vy, zp, z1v), 4, "vip", "bought")
    add("vip_endm", "VIP end panel, battery end", B(-vx, -px, -py, py, zp, z1v), 4, "vip", "bought")
    add("vip_endlo", "VIP end panel, cooling end, lower", B(px, vx, -py, py, zp, f_lo), 4, "vip", "bought")
    add("vip_endhi", "VIP end panel, cooling end, upper", B(px, vx, -py, py, f_hi, z1v), 4, "vip", "bought")
    c_ = P["tray_clear"]
    add("vip_lid", "VIP lid plug", B(-px + c_, px - c_, -py + c_, py - c_, L["lidpcm_z1"], rim), 4, "vip", "bought")
    loop8 = loop_solid(r)
    cable = _xcyl(cx - P["liner_t"], sx + 8, yc, ez, rc)
    foam = B(px, vx, -py, py, f_lo, f_hi) - loop8 - cable
    add("foam", "Foam strip (cut around the pipes and cable)", foam, 17, "vip")

    # ---- 7 Evaporator can with inward rim flange, the loop and the cold block
    can = B(-px, px, -py, py, zp, L["cav_z1"]) - B(-px + ct, px - ct, -py + ct, py - ct, zp + ct, L["cav_z1"] + 1)
    can += (B(-px + ct, px - ct, -py + ct, py - ct, L["cav_z1"] - ct, L["cav_z1"])
            - B(-px + ct + fl, px - ct - fl, -py + ct + fl, py - ct - fl, L["cav_z1"] - 2, L["cav_z1"] + 1))
    for y in pipes_y:                                       # riser slots, open at the rim
        can -= B(px - ct - 1, px + 1, y - r - 0.5, y + r + 0.5, ez - P["riser_r"] - 1, L["cav_z1"] + 1)
    can -= _xcyl(px - 3, px + 1, yc, ez, rc + 0.5)
    add("can", "Evaporator can", can, 7, "thermo")
    add("loop", "Loop thermosiphon (copper)", loop8, 7, "thermo")

    bx, by, bz = P["block"]
    bz0 = L["block_z0"]
    block = B(sx, sx + bx, -by / 2, by / 2, bz0, bz0 + bz)
    for y in pipes_y:                                       # tube sockets
        block -= _xcyl(sx - 1, sx + P["socket"], y, ez, r + 0.05)
    block -= _ycyl(sx + P["socket"], -P["pipe_y"] - 0.5, by / 2 + 1, ez, 3.0)   # condensing passage, open at +Y
    for y in (P["tec_screw_y"], -P["tec_screw_y"]):         # tapped holes for the module clamp screws
        block -= _xcyl(sx + bx - 8, sx + bx + 1, y, zc, 1.25)
    add("block", "Cold block", block, 7, "thermo")
    stub = _ycyl(sx + P["socket"], by / 2, by / 2 + 20, ez, 3.0)
    add("charge", "Charge stub (pinched and brazed shut)", stub, 7, "thermo")

    # ---- frame for the cold block, with the drip tray, on the shell towers
    ft = P["frame_t"]
    fx0, fx1 = sx + bx, sx + bx + ft
    frame = B(fx0, fx1, -(P["tower_y"] + 5), P["tower_y"] + 5, 100, 152) - B(fx0 - 1, fx1 + 1, -21, 21, 105, 147)
    for y in (P["tec_screw_y"], -P["tec_screw_y"]):
        frame -= _xcyl(fx0 - 1, fx1 + 1, y, zc, 1.75)
    for y in (P["tower_y"], -P["tower_y"]):
        frame -= _xcyl(fx0 - 1, fx1 + 1, y, zc, 1.75)
    tray = (B(sx, fx1, -34, 34, 100, 102) + B(sx, fx1, 32, 34, 102, 104) + B(sx, fx1, -34, -32, 102, 104))
    tray -= _zcyl(134, -30, 99, 103, 2.5)
    add("frame", "Block frame and drip tray", frame + tray, 17, "housings")
    drain = _zcyl(134, -30, 0, 100, 2.5)
    add("drain", "Drain tube", drain, 17, "housings", "bought")

    # ---- 8 Peltier module, 9 sink, fan, guard and screws
    tx, ty, tz = P["tec"]
    add("tec", "Peltier module", B(sx + bx, sx + bx + tx, -ty / 2, ty / 2, zc - tz / 2, zc + tz / 2), 8, "tec", "bought")
    h0 = sx + bx + tx
    swd, shh = P["sink_w"], P["sink_h"]
    sink = B(h0, h0 + P["sink_base"], -swd / 2, swd / 2, zc - shh / 2, zc + shh / 2)
    for i in range(P["fins"]):
        y = -swd / 2 + 1 + i * (swd - 2) / (P["fins"] - 1)
        sink += B(h0 + P["sink_base"], h0 + P["sink_base"] + P["sink_fin"], y - 1, y + 1, zc - shh / 2, zc + shh / 2)
    for y in (P["tec_screw_y"], -P["tec_screw_y"]):
        sink -= _xcyl(h0 - 1, h0 + P["sink_base"] + 1, y, zc, 1.7)
    add("sink", "Heat sink", sink, 9, "sink", "bought")
    fxx, fy, fz = P["fan"]
    f0 = h0 + P["sink_base"] + P["sink_fin"] + 1
    fan = B(f0, f0 + fxx, -fy / 2, fy / 2, zc - fz / 2, zc + fz / 2) - _xcyl(f0 - 1, f0 + fxx + 1, 0, zc, fy / 2 - 4)
    fan += _xcyl(f0, f0 + fxx, 0, zc, 10)
    fan += B(f0 - 1, f0, -fy / 2, -fy / 2 + 6, zc - fz / 2, zc + fz / 2) + B(f0 - 1, f0, fy / 2 - 6, fy / 2, zc - fz / 2, zc + fz / 2)
    add("fan", "Fan", fan, 9, "sink", "bought")
    guard = B(f0 + fxx, f0 + fxx + 1, -fy / 2, fy / 2, zc - fz / 2, zc + fz / 2) - _xcyl(f0 + fxx - 1, f0 + fxx + 2, 0, zc, fy / 2 - 3)
    guard += B(f0 + fxx, f0 + fxx + 1, -1, 1, zc - fz / 2, zc + fz / 2) + B(f0 + fxx, f0 + fxx + 1, -fy / 2, fy / 2, zc - 1, zc + 1)
    add("guard", "Finger guard", guard, 9, "sink", "bought")
    scr = None
    for y in (P["tec_screw_y"], -P["tec_screw_y"]):
        s = _xcyl(sx + bx - 8, h0 + P["sink_base"], y, zc, 1.25) + _xcyl(h0 + P["sink_base"], h0 + P["sink_base"] + 3, y, zc, 2.75)
        scr = s if scr is None else scr + s
    for y in (P["tower_y"], -P["tower_y"]):
        s = _xcyl(sx + 2, fx1, y, zc, 1.25) + _xcyl(fx1, fx1 + 0.4, y, zc, 2.75)
        scr += s
    add("screws", "Module clamp screws and frame screws", scr, 16, "sink", "bought")

    # ---- 10 End housings with ears; cooling head (+X) and battery bay (-X)
    dd, dz0, dz1 = P["duct"]
    head = B(sx, hx1, -ew, ew, 0, top) - B(sx - 1, hx1 - wt, -ew + wt, ew - wt, wt, top - wt)
    for i in range(7):                                   # exhaust grille on the +X face
        z = zc - 32 + i * 10
        head -= B(hx1 - wt - 1, hx1 + 1, -35, 35, z, z + 5)
    for i in range(5):                                   # intake slots on the front face, low down
        x = sx + 12 + i * 9
        head -= B(x, x + 5, -ew - 1, -ew + wt + 1, 30, 70)
    head -= _zcyl(134, -30, -1, wt + 1, 2.5)              # condensate drain
    head -= _xcyl(hx1 - wt - 1, hx1 + 1, 20, 40, 6.0)     # 12 V socket
    head -= B(hx1 - wt - 1, hx1 + 1, -24.5, -15.5, 37.5, 42.5)    # USB-C socket
    head -= B(sx - 1, sx + dd, ew - wt - 1, ew + 1, dz0, dz1)   # duct notch
    for y in (P["pad_y"], -P["pad_y"]):
        for z in P["pad_z"]:
            y0, y1 = (ew - wt, y + 7) if y > 0 else (y - 7, -ew + wt)
            ear = B(sx + pt, sx + pt + 3, y0, y1, z - 8, z + 8) - _xcyl(sx, sx + pt + 4, y, z, 1.7)
            head += ear
    add("head", "Cooling head housing", head, 10, "housings")
    bay = B(bx0, -sx, -ew, ew, 0, top) - B(bx0 + wt, -sx + 1, -ew + wt, ew - wt, wt, top - wt)
    for i in range(4):                                   # vents on the -X face
        z = 30 + i * 10
        bay -= B(bx0 - 1, bx0 + wt + 1, -30, 30, z, z + 4)
    bay -= B(bx0 + 9, bx0 + 35, -30, 30, top - wt - 1, top + 1)        # display window
    bay -= _zcyl(bx0 + 22, 50, top - wt - 1, top + 1, 5.2)              # alarm light and buzzer hole
    bay -= _zcyl(bx0 + 22, -50, top - wt - 1, top + 1, 5.2)             # second status light hole (mirrored)
    bay -= _zcyl(bx0 + 22, 64, top - wt - 1, top + 1, 5.2)              # battery shipping switch hole
    bay -= B(-sx - dd, -sx + 1, ew - wt - 1, ew + 1, dz0, dz1)          # duct notch
    for y in (P["pad_y"], -P["pad_y"]):
        for z in P["pad_z"]:
            y0, y1 = (ew - wt, y + 7) if y > 0 else (y - 7, -ew + wt)
            bay += B(-sx - pt - 3, -sx - pt, y0, y1, z - 8, z + 8) - _xcyl(-sx - pt - 4, -sx, y, z, 1.7)
    add("bay", "Battery bay housing", bay, 10, "housings")

    # ---- cable duct cover on the back face, turning onto both end faces into the housings
    ow = 1.5
    duct = B(-sx, sx, sy, sy + dd, dz0, dz1)
    chan = B(-sx - 1, sx + 1, sy - 1, sy + dd - ow, dz0 + ow, dz1 - ow)
    for sgn in (1, -1):
        xa, xb = (sx, sx + dd) if sgn > 0 else (-sx - dd, -sx)
        duct += B(xa, xb, ew, sy + dd, dz0, dz1)
        cxa, cxb = (sx - 1, sx + dd - ow) if sgn > 0 else (-sx - dd + ow, -sx + 1)
        chan += B(cxa, cxb, ew - 1, sy + dd - ow, dz0 + ow, dz1 - ow)
    add("duct", "Cable duct cover", duct - chan, 17, "shell")

    # ---- 2 Lid cap, latches; lid cold plate tray; lid PCM pack
    add("lid", "Lid cap", B(-sx, sx, -sy, sy, rim, top), 2, "lid")
    latches = None
    for x in (-P["latch_x"], P["latch_x"]):
        l_ = B(x - 9, x + 9, -sy - pt - 8, -sy - pt, 144, 160) + B(x - 8, x + 8, -sy, -sy + 10, top, top + 3)
        latches = l_ if latches is None else latches + l_
    add("latches", "Draw latches and keepers (2)", latches, 2, "lid", "bought")
    t_, lip = P["lid_plate_t"], P["tray_lip"]
    z_a, z_b = L["cav_z1"], L["lidpcm_z1"]
    ox, oy = px - c_, py - c_
    tray_l = (B(-ox, ox, -oy, oy, z_a, z_b) - B(-ox + t_, ox - t_, -oy + t_, oy - t_, z_a + t_, z_b - t_)
              - B(-ox + lip, ox - lip, -oy + lip, oy - lip, z_b - t_ - 1, z_b + 1))
    add("lidplate", "Lid cold plate tray", tray_l, 2, "lidplate")
    lid_pcm = (B(-ox + t_, ox - t_, -oy + t_, oy - t_, z_a + t_, z_b - t_)
               + B(-ox + lip, ox - lip, -oy + lip, oy - lip, z_b - t_, z_b))
    add("pcm_lid", "Lid PCM pack", lid_pcm, 5, "pcm", "bought")

    # ---- 6 Liner, feet, collar, rack
    lt, rt = P["liner_t"], P["rack_t"]
    liner = B(-cx, cx, -cy, cy, L["cav_z0"], L["cav_z1"]) - B(-cx + lt, cx - lt, -cy + lt, cy - lt, L["cav_z0"] + lt, L["cav_z1"] + 1)
    liner -= _xcyl(cx - lt - 1, cx + 1, yc, ez, rc + 0.5)
    add("liner", "Aluminium liner", liner, 6, "liner")
    fo = P["foot"] / 2
    feet = None
    for xs_ in (-1, 1):
        for ys_ in (-1, 1):
            f = B(xs_ * (cx - 8) - fo, xs_ * (cx - 8) + fo, ys_ * (cy - 8) - fo, ys_ * (cy - 8) + fo, zp + ct, L["cav_z0"])
            feet = f if feet is None else feet + f
    co_x, co_y = px - ct - fl - 0.5, py - ct - fl - 0.5
    collar = B(-co_x, co_x, -co_y, co_y, L["cav_z1"] - P["collar_h"], L["cav_z1"]) - B(-cx, cx, -cy, cy, 0, 500)
    add("feet", "Liner feet (4)", feet, 17, "liner")
    add("collar", "Liner collar", collar, 17, "liner")
    rz0 = L["cav_z0"] + lt
    rack = B(-cx + lt + 1, cx - lt - 1, -cy + lt + 1, cy - lt - 1, rz0, rz0 + rt)
    pd, nc = P["pen_d"], P["pen_cols"]
    pitch_pair = 2 * pd + rt
    y_pairs = [(i - (nc // 2 - 1) / 2) * pitch_pair for i in range(nc // 2)]
    for i in range(nc // 2 - 1):
        yd = (y_pairs[i] + y_pairs[i + 1]) / 2
        rack += B(-cx + lt + 1, cx - lt - 1, yd - rt / 2, yd + rt / 2, rz0 + rt, rz0 + rt + P["pen_layers"] * pd - 4)
    add("rack", "Payload rack", rack, 6, "liner")

    pens = None
    for k in range(P["pen_layers"]):
        z = rz0 + rt + pd / 2 + k * pd
        for yp in y_pairs:
            for s in (-1, 1):
                pen = Pos(-4, yp + s * pd / 2, z) * Rot(0, 90, 0) * Cylinder(pd / 2 - 0.5, P["pen_l"])
                pens = pen if pens is None else pens + pen
    add("pens", "Payload: insulin pens (not supplied)", pens, None, "pens", "payload")

    # ---- 5 PCM jacket pouches: the can space less liner, feet, collar, loop and cable
    jacket = (B(-px + ct, px - ct, -py + ct, py - ct, zp + ct, L["cav_z1"] - ct)
              - B(-cx, cx, -cy, cy, L["cav_z0"], L["cav_z1"] + 1) - feet - collar - loop8 - cable)
    add("pcm_jacket", "PCM jacket pouches", jacket, 5, "pcm", "bought")

    # ---- 14 sensors: payload probe above the top layer, liner probe, liner cut-out, ambient, cable
    pdia, plen = P["probe"]
    top_layer = rz0 + rt + P["pen_layers"] * pd
    pz = top_layer + 1 + pdia / 2
    probe = _ycyl(cx - lt - 3 - pdia / 2, -plen / 2, plen / 2, pz, pdia / 2)
    probe += B(cx - lt - 3, cx - lt, -4, 4, pz - 3, pz + 3)
    add("probe", "Payload probe and clip", probe, 14, "sensors", "bought")
    add("liner_probe", "Liner probe", B(cx - 20, cx - 8, cy - lt - 3, cy - lt, L["cav_z0"] + 30, L["cav_z0"] + 36), 14, "sensors", "bought")
    add("cutout", "Liner cut-out (3 °C)", B(cx - lt - 4, cx - lt, -8, 8, L["cav_z0"] + 50, L["cav_z0"] + 62), 14, "sensors", "bought")
    add("ambient", "Ambient sensor", B(sx + 14, sx + 30, -ew - 3, -ew, 80, 92), 14, "sensors", "bought")
    add("cable", "Sensor cable", cable, 16, "sensors", "bought")

    # ---- 12 power board on standoffs, inlets
    pb = B(sx + 8, hx1 - 8, -65, 65, 8, 14)
    so = None
    for x in (sx + 11, hx1 - 11):
        for y in (-62, 62):
            s = _zcyl(x, y, wt, 8, 2.5)
            so = s if so is None else so + s
    add("power", "Power board", pb, 12, "power", "bought")
    add("power_so", "Power board standoffs (4)", so, 16, "power", "bought")
    inl = _xcyl(hx1 - wt - 6, hx1, 20, 40, 6.0) + B(hx1 - wt - 6, hx1, -24.5, -15.5, 37.5, 42.5)
    add("inlets", "12 V and USB-C inlets", inl, 12, "power", "bought")

    # ---- 11 cells, BMS, cradle
    cd, ch, n = P["cell_d"], P["cell_h"], P["cells"]
    cells = None
    for i in range(n):
        y = (i - (n - 1) / 2) * (cd + 2)
        c = _zcyl(bx0 + wt + 2 + cd / 2, y, wt + 2, wt + 2 + ch, cd / 2)
        cells = c if cells is None else cells + c
    cells += B(bx0 + wt + 2, bx0 + wt + 2 + cd, -n * (cd + 2) / 2, n * (cd + 2) / 2, wt + 2 + ch, wt + 8 + ch)
    add("cells", "LiFePO4 cells and BMS", cells, 11, "cells", "bought")
    cradle = B(bx0 + wt, bx0 + wt + cd + 4, -70, 70, wt, wt + 12)
    for i in range(n):
        y = (i - (n - 1) / 2) * (cd + 2)
        cradle -= _zcyl(bx0 + wt + 2 + cd / 2, y, wt + 2, wt + 13, cd / 2 + 0.2)
    add("cradle", "Cell cradle", cradle, 17, "cells")

    # ---- 13 logger on the bay's back wall; 15 display behind the window
    yb = ew - wt
    add("logger", "Logger board", B(bx0 + wt + 2, -sx - 4, yb - 7.6, yb - 6, 95, 155), 13, "logger", "bought")
    lso = None
    for x in (bx0 + wt + 5, -sx - 7):
        for z in (100, 150):
            s = _ycyl(x, yb - 6, yb, z, 2.5)
            lso = s if lso is None else lso + s
    add("logger_so", "Logger standoffs (4)", lso, 16, "logger", "bought")
    disp = B(bx0 + 7, bx0 + 37, -33, 33, top - wt - 3, top - wt)
    led = _zcyl(bx0 + 22, 50, top - wt - 8, top, 5.0)
    add("display", "E-paper display", disp, 15, "display", "bought")
    add("alarm", "Alarm light and buzzer", led, 15, "display", "bought")
    led2 = _zcyl(bx0 + 22, -50, top - wt - 8, top, 5.0)
    add("alarm2", "Second status light (red), mirrored", led2, 15, "display", "bought")
    swt = _zcyl(bx0 + 22, 64, top - wt - 18, top, 5.0)
    add("shipswitch", "Battery shipping switch, flush panel isolator", swt, 18, "shipsw", "bought")

    # ---- 3 handle
    hd = P["handle_d"]
    ya = sy + pt
    handle = (_zcyl(0, -ya - hd / 4, P["handle_pivot_z"], P["handle_top"], hd / 4)       # round bail rod (CPD-DEC-001, 2026-10-02)
              + _zcyl(0, ya + hd / 4, P["handle_pivot_z"], P["handle_top"], hd / 4)
              + Pos(0, 0, P["handle_top"]) * Rot(90, 0, 0) * Cylinder(hd / 2, 2 * ya + hd))
    add("handle", "Bail handle", handle, 3, "handle", "bought")
    return C


GROUPS = [("shell", "Outer shell", 1), ("lid", "Lid cap with gasket", 2), ("lidplate", "lid cold plate tray, 1.5 mm aluminium", 2),
          ("handle", "Bail handle and shoulder strap", 3), ("vip", "Vacuum-insulated panels, 25 mm", 4),
          ("pcm", "PCM jacket and lid pack, 5 °C", 5), ("liner", "Aluminium liner, feet, collar and rack", 6),
          ("pens", "Payload: insulin pens (not supplied)", None),
          ("thermo", "Evaporator can, loop thermosiphon, cold block", 7), ("tec", "Peltier module, 40 x 40 mm", 8),
          ("sink", "Hot-side heat sink and fan", 9), ("housings", "End housings (cooling head, battery bay)", 10),
          ("cells", "LiFePO4 pack, 12.8 V 6 Ah, with BMS", 11), ("power", "Power board (USB-C PD, 12 V, drivers)", 12),
          ("logger", "Logger controller (nRF52840 class)", 13), ("sensors", "Temperature sensors and liner cut-out", 14),
          ("display", "E-paper display and two status lights", 15), ("shipsw", "Battery shipping switch", 18)]


def build_parts(P=PARAMS):
    """Return [(key, name, shape, bom_line)] grouped as in the concept (17 groups)."""
    C = build_components(P)
    out = []
    for key, name, bom in GROUPS:
        shapes = [c.shape for c in C.values() if c.group == key]
        out.append((key, name, _fuse(shapes), bom))
    return out


def build(P=PARAMS):
    """Whole assembly as one compound."""
    from build123d import Compound
    return Compound(children=[s for _, _, s, _ in build_parts(P)])


def volumes_cm3(P=PARAMS):
    """Solid volume of each concept group in cm³."""
    return {k: s.volume / 1000.0 for k, _, s, _ in build_parts(P)}


def component_volumes_cm3(P=PARAMS):
    """Solid volume of each component in cm³ (for the mass estimate in CPD-CAL-001)."""
    return {k: c.shape.volume / 1000.0 for k, c in build_components(P).items()}


# ---------------------------------------------------------------- constructability checks
def _vol(a, b_):
    bb1, bb2 = a.bounding_box(), b_.bounding_box()
    if (bb1.min.X > bb2.max.X or bb2.min.X > bb1.max.X or bb1.min.Y > bb2.max.Y or bb2.min.Y > bb1.max.Y
            or bb1.min.Z > bb2.max.Z or bb2.min.Z > bb1.max.Z):
        return 0.0
    try:
        r = a & b_
    except Exception:
        return -1.0
    return 0.0 if r is None else r.volume


def _gap(a, b_):
    return a.distance_to(b_)


# Pairs that must touch (a fixing or a seat). Every other pair must not overlap.
TOUCH = [
    ("vip_floor", "shell", "VIP floor panel on the shell floor"),
    ("vip_front", "vip_floor", "VIP front panel on the floor panel"), ("vip_back", "vip_floor", "VIP back panel on the floor panel"),
    ("vip_endm", "vip_floor", "VIP battery end panel on the floor panel"), ("vip_endlo", "vip_floor", "VIP cooling end lower panel on the floor panel"),
    ("vip_endhi", "foam", "VIP cooling end upper panel on the foam strip"), ("foam", "vip_endlo", "Foam strip on the lower end panel"),
    ("can", "vip_floor", "Evaporator can on the VIP floor"), ("loop", "can", "Loop bonded into the can's bottom corner"),
    ("loop", "block", "Tubes in the cold block sockets"), ("block", "shell", "Cold block against the shell end face"),
    ("frame", "block", "Block frame on the block rim"), ("frame", "shell", "Frame on the shell towers"),
    ("tec", "block", "Peltier on the block"), ("sink", "tec", "Heat sink on the Peltier"), ("fan", "sink", "Fan on the sink"),
    ("guard", "fan", "Guard on the fan"), ("screws", "sink", "Clamp screws through the sink"), ("screws", "block", "Clamp screws into the block"),
    ("feet", "can", "Liner feet on the can floor"), ("liner", "feet", "Liner on its feet"), ("collar", "liner", "Collar on the liner"),
    ("rack", "liner", "Rack on the liner floor"), ("pcm_jacket", "can", "Jacket pouches in the can"),
    ("lidplate", "can", "Lid tray on the can flange"), ("pcm_lid", "lidplate", "Lid pack in the tray"),
    ("vip_lid", "lidplate", "Lid plug on the tray lip"), ("vip_lid", "lid", "Lid plug under the lid cap"), ("lid", "shell", "Lid cap on the rim"),
    ("latches", "shell", "Latches on their pads"), ("latches", "lid", "Keepers on the lid cap"), ("handle", "shell", "Handle on its pivot pads"),
    ("head", "shell", "Cooling head against the shell end"), ("bay", "shell", "Battery bay against the shell end"),
    ("fillers", "shell", "Slot fillers in the slots"), ("duct", "shell", "Duct cover on the back face"),
    ("power_so", "head", "Power board standoffs on the head floor"), ("power", "power_so", "Power board on its standoffs"),
    ("inlets", "head", "Inlets in the head end wall"), ("drain", "frame", "Drain tube under the drip tray"), ("drain", "head", "Drain tube through the head floor"),
    ("cradle", "bay", "Cell cradle on the bay floor"), ("cells", "cradle", "Cells in the cradle"),
    ("logger_so", "bay", "Logger standoffs on the bay back wall"), ("logger", "logger_so", "Logger on its standoffs"),
    ("display", "bay", "Display under the bay top"),  ("probe", "liner", "Probe clip on the liner end wall"),
    ("liner_probe", "liner", "Liner probe on the liner"), ("cutout", "liner", "Liner cut-out on the liner"),
    ("ambient", "head", "Ambient sensor on the head front"), ("charge", "block", "Charge stub in the block"),
]
# Pairs allowed to overlap in the model because one passes through the other by design
PASS = {("cable", "liner"), ("cable", "can"), ("cable", "fillers"), ("cable", "shell"), ("cable", "foam"), ("cable", "pcm_jacket"),
        ("drain", "head"), ("screws", "block"), ("screws", "frame"), ("screws", "sink"), ("screws", "shell"),
        ("loop", "block"), ("loop", "fillers"), ("loop", "shell"), ("alarm", "bay"), ("alarm2", "bay"), ("shipswitch", "bay"), ("inlets", "head")}
CLEAR = [("loop", "vip_endlo", 1.0, "Riser bends clear of the lower VIP end panel"),
         ("lidplate", "vip_front", 0.4, "Lid tray clear of the VIP walls"),
         ("probe", "pens", 1.0, "Payload probe clear of the top layer of pens"),
         ("probe", "lidplate", 1.0, "Payload probe below the lid tray"),
         ("frame", "sink", 0.4, "Frame clear of the hot sink"),
         ("collar", "can", 0.4, "Collar clear of the can flange edge"),
         ("handle", "lid", 2.0, "Handle clear of the lid cap"),
         ("power", "drain", 1.0, "Power board clear of the drain tube"),
         ("power", "frame", 30.0, "Power board well below the drip tray"),
         ("guard", "head", 1.0, "Finger guard inside the grille wall"),
         ("logger", "cells", 5.0, "Logger clear of the cells and BMS"),
         ("shipswitch", "cells", 5.0, "Shipping switch body clear of the cells"),
         ("shipswitch", "display", 8.0, "Shipping switch clear of the display"),
         ("shipswitch", "logger", 1.0, "Shipping switch clear of the logger board"),
         ("shipswitch", "alarm", 2.0, "Shipping switch clear of the first status light"),
         ("alarm2", "display", 2.0, "Second status light clear of the display"),
         ("alarm2", "alarm", 60.0, "Status lights well apart (mirrored)")]


def checks(P=PARAMS):
    """Return rows (description, overlap mm3, gap mm, expectation, ok)."""
    C = build_components(P)
    S = {k: c.shape for k, c in C.items()}
    rows = []
    for a, b_, d in TOUCH:
        v = _vol(S[a], S[b_])
        g = 0.0 if v > 1e-3 else _gap(S[a], S[b_])
        ok = g < 0.06 and ((a, b_) in PASS or (b_, a) in PASS or v < 1e-3)
        rows.append((d, v, g, "touch", ok))
    for a, b_, c, d in CLEAR:
        v = _vol(S[a], S[b_])
        g = 0.0 if v > 1e-3 else _gap(S[a], S[b_])
        rows.append((d, v, g, f">= {c} mm", v < 1e-3 and g >= c - 1e-6))
    keys = [k for k in S if C[k].kind != "payload" or k == "pens"]
    bad = 0
    for i, a in enumerate(keys):
        for b_ in keys[i + 1:]:
            if (a, b_) in PASS or (b_, a) in PASS:
                continue
            v = _vol(S[a], S[b_])
            if v > 1e-2 or v < 0:
                rows.append((f"No overlap: {C[a].name} / {C[b_].name}", v, 0.0, "no overlap", False))
                bad += 1
    rows.append((f"No overlap between any other pair ({len(keys) * (len(keys) - 1) // 2} pairs)", 0.0, 0.0, "no overlap", bad == 0))
    return rows


def _export():
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    parts = {k: s for k, _, s, _ in build_parts()}
    groups = {"shell": ["shell"], "lid": ["lid", "lidplate"], "vip-set": ["vip"], "liner-rack": ["liner"],
              "evaporator-thermosiphon": ["thermo"], "cooling-head": ["tec", "sink"],
              "end-housings": ["housings"]}
    for name, keys in groups.items():  # export parts before they are adopted by a compound
        shape = parts[keys[0]] if len(keys) == 1 else Compound(children=[parts[k] for k in keys])
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
    asm = build()
    export_step(asm, str(out / "step" / "coldpod-assembly.step"))
    export_stl(asm, str(out / "stl" / "coldpod-assembly.stl"), tolerance=0.2, angular_tolerance=0.3)
    bb = asm.bounding_box()
    print(f"assembly {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm; exported STEP and STL to cad/step and cad/stl")


if __name__ == "__main__":
    if "--check" in sys.argv:
        rows = checks()
        for d, v, g, e, ok in rows:
            print(f"{'PASS' if ok else 'FAIL'}  {d}: overlap {v:.2f} mm3, gap {g:.2f} mm (expect {e})")
        n_ok = sum(r[4] for r in rows)
        print(f"{n_ok} of {len(rows)} checks pass")
        sys.exit(0 if n_ok == len(rows) else 1)
    _export()
