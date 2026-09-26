"""ColdPod parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    coldpod-assembly.step / .stl      whole case, lid closed, handle up
    shell.step, lid.step, vip-set.step, liner-rack.step, evaporator-thermosiphon.step,
    cooling-head.step (Peltier, sink, fan, cold block) and end-housings.step (and .stl)

Axes: X along the case length (battery and electronics bay at -X, cooling head at +X),
Y front (-Y) to back (+Y), Z up, table at Z = 0. Units mm.

Layers from the inside out: payload cavity in an aluminium liner, a phase-change material
(PCM) jacket on four sides and the floor held in an aluminium evaporator can, a PCM pack in
the lid on a 1.5 mm aluminium cold plate that seats on the can rim when the lid closes,
25 mm vacuum-insulated panels (VIP), a printed shell (3 mm walls, 5 mm lid cap, 2 mm end
housings, CPD-DDR-002). A hardware cut-out on the liner (3 °C) backs up the one on the
cold block. A two-phase loop thermosiphon
(evaporator loop low around the can, vapour riser and liquid return at the +X end) carries
heat one way, up and out, to a cold block on the Peltier module in the +X cooling head.

Main dimensions and interfaces only; not fabrication detail; not for fabrication.
The same PARAMS feed docs/04-calcs/sizing.py (CPD-CAL-001).
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # payload cavity and liner (outside of the liner)
    "cav_l": 175.0, "cav_w": 110.0, "cav_h": 80.0, "liner_t": 1.5,
    "rack_t": 2.0,                            # rack floor and divider thickness
    # PCM jacket (includes the evaporator can wall) and lid pack
    "pcm_t": 15.0, "can_t": 1.0, "lid_pcm_t": 15.0,
    "lid_plate_t": 1.5,                       # aluminium cold plate under the lid pack, seats on the can rim
    # insulation and shell (thinner printed parts, CPD-DDR-002)
    "vip_t": 25.0, "shell_t": 3.0, "lid_cap_t": 5.0,
    "foam_strip": 20.0,                       # foam-filled strip in the +X VIP wall where the pipes cross
    # payload (not supplied): insulin pens in layers
    "pen_d": 16.0, "pen_l": 160.0, "pen_cols": 6, "pen_layers": 4,
    # thermosiphon (two-phase loop): 8 mm copper tube, stainless adiabatic section through the wall
    "pipe_d": 8.0, "pipe_y": 25.0, "loop_inset": 5.0, "pipe_exit_z": 114.0,
    # cold block, Peltier module, heat sink, fan
    "block": (10.0, 60.0, 44.0),              # aluminium, X, Y, Z; bottom at pipe_exit_z - 10
    "tec": (4.0, 40.0, 40.0),                 # 40 x 40 mm module
    "sink_base": 6.0, "sink_fin": 24.0, "sink_w": 80.0, "sink_h": 80.0, "fins": 9,
    "fan": (10.0, 70.0, 70.0),
    # end housings
    "head_l": 60.0, "bay_l": 45.0, "end_w": 160.0, "end_wall": 2.0,
    # battery: 4S1P 32700 LiFePO4 cells standing in the -X bay
    "cell_d": 32.0, "cell_h": 70.0, "cells": 4,
    # bail handle (up position)
    "handle_d": 16.0, "handle_top": 199.0, "handle_pivot_z": 128.0,
}


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
    d["head_x1"] = d["sh_x"] + P["head_l"]
    d["bay_x0"] = -d["sh_x"] - P["bay_l"]
    return d


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _tube(p1, p2, r):
    from build123d import Solid, Plane, Vector
    v = Vector(*p2) - Vector(*p1)
    return Solid.make_cylinder(r, v.length, Plane(origin=p1, z_dir=v))


def build_parts(P=PARAMS):
    """Return [(key, name, shape, bom_line)] for the whole case."""
    from build123d import Cylinder, Pos, Rot
    L = levels(P)
    B = _box
    cx, cy, px, py = L["cav_x"], L["cav_y"], L["pcm_x"], L["pcm_y"]
    vx, vy, sx, sy = L["vip_x"], L["vip_y"], L["sh_x"], L["sh_y"]
    ez, r = P["pipe_exit_z"], P["pipe_d"] / 2

    # 1 Outer shell: open-topped tub with two pipe pass-throughs at +X
    shell = B(-sx, sx, -sy, sy, 0, L["rim"]) - B(-vx, vx, -vy, vy, P["shell_t"], L["rim"] + 1)
    for y in (-P["pipe_y"], P["pipe_y"]):
        shell -= Pos(sx - 2, y, ez) * Rot(0, 90, 0) * Cylinder(r + 1, 8)

    # 2 Lid: printed cap over the rim, VIP plug and the lid PCM pack hang below it
    lid = B(-sx, sx, -sy, sy, L["rim"], L["lid_top"])
    lid_vip = B(-px, px, -py, py, L["lidpcm_z1"], L["rim"])

    # 3 Bail handle, pivots on the front and back faces
    hd = P["handle_d"]
    handle = (B(-hd / 2, hd / 2, -sy - hd / 2, -sy, P["handle_pivot_z"], P["handle_top"])
              + B(-hd / 2, hd / 2, sy, sy + hd / 2, P["handle_pivot_z"], P["handle_top"])
              + Pos(0, 0, P["handle_top"]) * Rot(90, 0, 0) * Cylinder(hd / 2, 2 * sy + hd))

    # 4 VIP set: five body panels plus the lid plug; foam strip where the pipes cross at +X
    vip = B(-vx, vx, -vy, vy, L["vip_z0"], L["rim"]) - B(-px, px, -py, py, L["pcm_z0"], L["rim"] + 1)
    fs = P["foam_strip"] / 2
    foam = B(px, vx, -py, py, ez - fs, ez + fs)
    vip = vip - foam + lid_vip

    # 5 PCM: jacket inside the evaporator can (sides and floor) plus the lid pack
    ct = P["can_t"]
    jacket = B(-px + ct, px - ct, -py + ct, py - ct, L["pcm_z0"] + ct, L["cav_z1"]) - B(-cx, cx, -cy, cy, L["cav_z0"], L["cav_z1"] + 1)
    lid_pcm = B(-px, px, -py, py, L["plate_z1"], L["lidpcm_z1"])
    # Lid cold plate (BOM line 2): under the lid pack, its rim lands on the evaporator can rim
    lid_plate = B(-px, px, -py, py, L["cav_z1"], L["plate_z1"])

    # 6 Liner and payload rack
    lt, rt = P["liner_t"], P["rack_t"]
    liner = B(-cx, cx, -cy, cy, L["cav_z0"], L["cav_z1"]) - B(-cx + lt, cx - lt, -cy + lt, cy - lt, L["cav_z0"] + lt, L["cav_z1"] + 1)
    rz0 = L["cav_z0"] + lt
    rack = B(-cx + lt + 1, cx - lt - 1, -cy + lt + 1, cy - lt - 1, rz0, rz0 + rt)
    pd, nc = P["pen_d"], P["pen_cols"]
    # dividers between column pairs: pens in three pairs across Y
    pitch_pair = 2 * pd + rt
    y_pairs = [(i - (nc // 2 - 1) / 2) * pitch_pair for i in range(nc // 2)]
    for i in range(nc // 2 - 1):
        yd = (y_pairs[i] + y_pairs[i + 1]) / 2
        rack += B(-cx + lt + 1, cx - lt - 1, yd - rt / 2, yd + rt / 2, rz0 + rt, rz0 + rt + P["pen_layers"] * pd - 4)
    liner = liner + rack

    # Payload (not supplied): pens, pen_layers x pen_cols
    pens = None
    for k in range(P["pen_layers"]):
        z = rz0 + rt + pd / 2 + k * pd
        for yp in y_pairs:
            for s in (-1, 1):
                pen = Pos(-4, yp + s * pd / 2, z) * Rot(0, 90, 0) * Cylinder(pd / 2 - 0.5, P["pen_l"])
                pens = pen if pens is None else pens + pen

    # 7 Evaporator can and loop thermosiphon, cold block (condenser)
    can = B(-px, px, -py, py, L["pcm_z0"], L["cav_z1"]) - B(-px + ct, px - ct, -py + ct, py - ct, L["pcm_z0"] + ct, L["cav_z1"] + 1)
    lz, li = L["loop_z"], ct + P["loop_inset"] + r
    lxa, lya = px - li, py - li
    loop = (_tube((-lxa, -lya, lz), (lxa, -lya, lz), r) + _tube((lxa, -lya, lz), (lxa, lya, lz), r)
            + _tube((lxa, lya, lz), (-lxa, lya, lz), r) + _tube((-lxa, lya, lz), (-lxa, -lya, lz), r))
    bx, by, bz = P["block"]
    for y in (-P["pipe_y"], P["pipe_y"]):
        loop += _tube((lxa, y, lz), (lxa, y, ez), r)                  # riser (vapour) and return (liquid)
        loop += _tube((lxa, y, ez), (sx + 1, y, ez), r)               # out through the foam strip and shell
    block = B(sx, sx + bx, -by / 2, by / 2, L["block_z0"], L["block_z0"] + bz)
    thermo = can + loop + block
    pcm = (jacket - loop) + lid_pcm                                   # pouches are formed around the tubes

    # 8 Peltier module, cold face on the block
    tx, ty, tz = P["tec"]
    zc = L["block_z0"] + bz / 2
    tec = B(sx + bx, sx + bx + tx, -ty / 2, ty / 2, zc - tz / 2, zc + tz / 2)

    # 9 Hot-side heat sink and fan
    h0 = sx + bx + tx
    sw, sh = P["sink_w"], P["sink_h"]
    sink = B(h0, h0 + P["sink_base"], -sw / 2, sw / 2, zc - sh / 2, zc + sh / 2)
    for i in range(P["fins"]):
        y = -sw / 2 + 1 + i * (sw - 2) / (P["fins"] - 1)
        sink += B(h0 + P["sink_base"], h0 + P["sink_base"] + P["sink_fin"], y - 1, y + 1, zc - sh / 2, zc + sh / 2)
    fx, fy, fz = P["fan"]
    f0 = h0 + P["sink_base"] + P["sink_fin"] + 1
    fan = B(f0, f0 + fx, -fy / 2, fy / 2, zc - fz / 2, zc + fz / 2) - Pos(f0 + fx / 2, 0, zc) * Rot(0, 90, 0) * Cylinder(fy / 2 - 4, fx + 2)
    fan += Pos(f0 + fx / 2, 0, zc) * Rot(0, 90, 0) * Cylinder(10, fx)
    sinkfan = sink + fan

    # 10 End housings: cooling head (+X) and battery and electronics bay (-X)
    ew, wt, top = P["end_w"] / 2, P["end_wall"], L["lid_top"]
    hx1 = L["head_x1"]
    head = B(sx, hx1, -ew, ew, 0, top) - B(sx, hx1 - wt, -ew + wt, ew - wt, wt, top - wt)
    for i in range(7):                                   # exhaust grille on the +X face
        z = zc - 32 + i * 10
        head -= B(hx1 - wt - 1, hx1 + 1, -35, 35, z, z + 5)
    for i in range(5):                                   # intake slots on the front face, low down
        x = sx + 12 + i * 9
        head -= B(x, x + 5, -ew - 1, -ew + wt + 1, 30, 70)
    bx0 = L["bay_x0"]
    bay = B(bx0, -sx, -ew, ew, 0, top) - B(bx0 + wt, -sx, -ew + wt, ew - wt, wt, top - wt)
    for i in range(4):                                   # vents on the -X face
        z = 30 + i * 10
        bay -= B(bx0 - 1, bx0 + wt + 1, -30, 30, z, z + 4)
    housings = head + bay

    # 11 LiFePO4 pack: 4S1P cells standing in the -X bay, BMS on top
    cd, ch, n = P["cell_d"], P["cell_h"], P["cells"]
    cells = None
    for i in range(n):
        y = (i - (n - 1) / 2) * (cd + 2)
        c = Pos(bx0 + wt + 2 + cd / 2, y, wt + 2 + ch / 2) * Cylinder(cd / 2, ch)
        cells = c if cells is None else cells + c
    cells += B(bx0 + wt + 2, bx0 + wt + 2 + cd, -n * (cd + 2) / 2, n * (cd + 2) / 2, wt + 4 + ch, wt + 10 + ch)

    # 12 Power board on the floor of the cooling head
    power = B(sx + 8, hx1 - 8, -65, 65, 8, 14)

    # 13 Logger controller board, standing in the -X bay
    logger = B(-sx - 6, -sx - 3, -50, 50, 95, 155)

    # 14 Temperature sensors: buffered payload probe in the cavity, liner probe, ambient at the intake
    sensors = (Pos(cx - 12, -cy + 12, rz0 + rt + 18) * Cylinder(7, 36)
               + B(cx - 20, cx - 8, cy - lt - 3, cy - lt, L["cav_z0"] + 30, L["cav_z0"] + 36)
               + B(sx + 14, sx + 30, -ew - 3, -ew, 80, 92)
               # liner cut-out thermostat (opens at 3 °C), clipped to the inside of the +X liner wall
               + B(cx - lt - 4, cx - lt, -8, 8, L["cav_z0"] + 50, L["cav_z0"] + 62))

    # 15 E-paper display and alarm on top of the bay
    display = B(bx0 + 7, bx0 + 37, -33, 33, top, top + 3) + Pos(bx0 + 22, 50, top + 2) * Cylinder(5, 4)

    return [
        ("shell", "Outer shell", shell, 1),
        ("lid", "Lid cap with gasket", lid, 2),
        ("lidplate", "Lid cold plate, 1.5 mm aluminium", lid_plate, 2),
        ("handle", "Bail handle and shoulder strap", handle, 3),
        ("vip", "Vacuum-insulated panels, 25 mm", vip, 4),
        ("pcm", "PCM jacket and lid pack, 5 °C", pcm, 5),
        ("liner", "Aluminium liner and payload rack", liner, 6),
        ("pens", "Payload: insulin pens (not supplied)", pens, None),
        ("thermo", "Evaporator can, loop thermosiphon, cold block", thermo, 7),
        ("tec", "Peltier module, 40 x 40 mm", tec, 8),
        ("sink", "Hot-side heat sink and fan", sinkfan, 9),
        ("housings", "End housings (cooling head, battery bay)", housings, 10),
        ("cells", "LiFePO4 pack, 12.8 V 6 Ah, with BMS", cells, 11),
        ("power", "Power board (USB-C PD, 12 V, drivers)", power, 12),
        ("logger", "Logger controller (nRF52840 class)", logger, 13),
        ("sensors", "Temperature sensors and liner cut-out", sensors, 14),
        ("display", "E-paper display and alarm", display, 15),
    ]


def build(P=PARAMS):
    """Whole assembly as one compound."""
    from build123d import Compound
    return Compound(children=[s for _, _, s, _ in build_parts(P)])


def volumes_cm3(P=PARAMS):
    """Solid volume of each part in cm³ (for the mass estimate in CPD-CAL-001)."""
    return {k: s.volume / 1000.0 for k, _, s, _ in build_parts(P)}


if __name__ == "__main__":
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
        export_stl(shape, str(out / "stl" / f"{name}.stl"))
    asm = build()
    export_step(asm, str(out / "step" / "coldpod-assembly.step"))
    export_stl(asm, str(out / "stl" / "coldpod-assembly.stl"))
    bb = asm.bounding_box()
    print(f"assembly {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm; exported STEP and STL to cad/step and cad/stl")
