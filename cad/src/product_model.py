"""ColdPod product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a filleted off-white tub with a black rubber base
bumper, a lid cap with an EPDM gasket line and two teal draw latches, a steel bail handle with a
ribbed rubber grip on pivot bosses, graphite end housings with rounded exhaust and intake slots,
a smoked window over the heat sink in the cooling head, USB-C and 12 V inlets, a lit e-paper
logger display with a green status light, a raised wordmark and a 2 to 8 degC label, and the
full internal stack for the exploded view (VIP set, evaporator can and loop thermosiphon, PCM
jacket and lid pack, liner and rack with pens, Peltier module, heat sink and fan, cells, boards).
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, levels() and build_parts() in model.py.
Axes as model.py: X along the case length (battery and electronics bay at -X, cooling head at
+X), Y front (-Y) to back (+Y), Z up, table at Z = 0. Units mm.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))

from build123d import (Axis, Box, BuildLine, Circle, Cylinder, FilletPolyline, Plane, Pos,
                       RectangleRounded, RegularPolygon, Rot, SlotOverall, Text, extrude, fillet, sweep)
from model import PARAMS, levels, build_parts, _box, _tube

derived = levels  # the brief's name for the derived levels

TITLE = "ColdPod: portable medicine cooler with a temperature logger"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); cooling head "
             "with heat sink window and exhaust grille at right, logger display at far left"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): handle, lid, gasket, "
             "lid VIP and PCM pack, cold plate, liner with pens, PCM jacket, evaporator can and "
             "thermosiphon, VIP set, tub; Peltier, heat sink and fan at right; cells and logger at left"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 34, "az": -140,
     "note": "Detail view from the front left and above (about 34 deg elevation): battery and "
             "electronics bay with the lit e-paper logger display, status lights and vents"},
]

# Colours (restrained product palette; kit accent for the latches and wordmark)
C_TUB = "#E6E8EB"
C_LID = "#F1F2F4"
C_HOUSING = "#2F343B"
C_RUBBER = "#1E2227"
C_ACCENT = "#0F766E"
C_STEEL = "#A9B0B8"
C_ALU = "#C6CBD1"
C_COPPER = "#B87333"
C_VIP = "#CBD0D6"
C_PCM = "#CFDDE9"
C_RACK = "#3A3F47"
C_PEN = "#F4F5F7"
C_TEC = "#EEF0F2"
C_SINK = "#B5BBC2"
C_FAN = "#1C1F24"
C_PCB = "#166534"
C_PCB_DARK = "#1A1D21"
C_CHIP = "#111827"
C_CELL = "#1E3A8A"
C_SCREEN = "#E4ECE6"
C_INK = "#1F2937"
C_GREEN = "#22C55E"
C_RED = "#7F1D1D"
C_WINDOW = "#B9C8D2"
C_WHITE = "#F7F7F5"
C_FABRIC = "#2A3038"

FONT = str(HERE.parents[2] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")

# Appearance-only detail sizes (mm)
R_PLAN = 12.0          # tub and lid plan corner radius
GASKET_H = 1.6         # visible gasket band under the lid
BUMPER_H = 12.0        # rubber base bumper height
BUMPER_PROUD = 1.0
PIVOT_Z = 136.0        # handle pivot centre (arm bottom in model.py is 128)
LATCH_X = (-72.0, 72.0)


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _prism(L, W, r, z0, h, x=0.0, y=0.0):
    """Rounded-rectangle prism in plan, from z0 up by h."""
    r = max(min(r, min(L, W) / 2 - 0.01), 0.01)
    return Pos(x, y, z0) * extrude(RectangleRounded(L, W, r), amount=h)


def _top_edges(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom_edges(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _slot_x(x0, depth, y, z, w, h):
    """Stadium slot (w across Y, h in Z) extruded along +X from x0."""
    return Pos(x0, y, z) * extrude(Plane.YZ * SlotOverall(w, h), amount=depth)


def _slot_y(y0, depth, x, z, w, h):
    """Stadium slot (w along X, h in Z) extruded along +Y from y0 (vertical slots use w < h)."""
    if h > w:
        return Pos(x, y0, z) * extrude(Plane.XZ * Rot(0, 0, 90) * SlotOverall(h, w), amount=-depth)
    return Pos(x, y0, z) * extrude(Plane.XZ * SlotOverall(w, h), amount=-depth)


def _text(txt, size, font=FONT):
    return Text(txt, font_size=size, font_path=font)


def _tub(P, L):
    """Outer shell (BOM 1): filleted tub, gasket groove, base bumper recess, pipe pass-throughs."""
    sx, sy, vx, vy = L["sh_x"], L["sh_y"], L["vip_x"], L["vip_y"]
    rim = L["rim"]
    tub = _prism(2 * sx, 2 * sy, R_PLAN, 0.0, rim)
    tub = _fillet_try(tub, _bottom_edges(tub), [3.0, 2.0, 1.0])
    tub -= _box(-vx, vx, -vy, vy, P["shell_t"], rim + 1)
    # gasket groove around the top outer edge (the gasket fills it)
    tub -= _prism(2 * sx + 4, 2 * sy + 4, R_PLAN + 2, rim - GASKET_H, GASKET_H + 1) - \
        _prism(2 * sx - 2.4, 2 * sy - 2.4, R_PLAN - 1.2, rim - GASKET_H - 1, GASKET_H + 3)
    ez, r = P["pipe_exit_z"], P["pipe_d"] / 2
    for y in (-P["pipe_y"], P["pipe_y"]):
        tub -= Pos(sx - 2, y, ez) * Rot(0, 90, 0) * Cylinder(r + 1, 8)
    gasket = _prism(2 * sx - 0.6, 2 * sy - 0.6, R_PLAN - 0.3, rim - GASKET_H, GASKET_H) - \
        _prism(2 * sx - 5.0, 2 * sy - 5.0, R_PLAN - 2.5, rim - GASKET_H - 1, GASKET_H + 2)
    bumper = _prism(2 * sx + 2 * BUMPER_PROUD, 2 * sy + 2 * BUMPER_PROUD, R_PLAN + BUMPER_PROUD, 0.0, BUMPER_H)
    bumper = _fillet_try(bumper, _top_edges(bumper), [0.9, 0.6])
    bumper = _fillet_try(bumper, _bottom_edges(bumper), [0.9, 0.6])
    bumper -= _prism(2 * sx - 4, 2 * sy - 4, R_PLAN - 2, -1, BUMPER_H + 2)
    return tub, gasket, bumper


def _lid(P, L):
    """Lid cap (BOM 2): 5 mm printed cap, filleted top edge, raised wordmark and window marking."""
    sx, sy = L["sh_x"], L["sh_y"]
    lid = _prism(2 * sx, 2 * sy, R_PLAN, L["rim"], P["lid_cap_t"])
    lid = _fillet_try(lid, _top_edges(lid), [2.0, 1.5, 1.0])
    top = L["lid_top"]
    word = Pos(-72.0, -62.0, top) * extrude(_text("ColdPod", 16.0), amount=0.5)
    mark = Pos(62.0, -64.0, top) * extrude(_text("2 to 8 °C", 7.0, str(HERE.parents[2] / ".kit" / "fonts" / "IBMPlexSans-Medium.ttf")), amount=0.4)
    return lid, word, mark


def _latches(P, L):
    """Two draw latches on the front (BOM 2): base plate on the tub, lever, keeper hook on the lid."""
    sy, rim = L["sh_y"], L["rim"]
    bases, levers, keepers = None, None, None
    for x in LATCH_X:
        base = Pos(x, -sy - 1.5, rim - 21) * Rot(90, 0, 0) * extrude(RectangleRounded(24.0, 18.0, 3.0), amount=1.5, both=True)
        lever = Pos(x, -sy - 5.5, rim - 12) * Rot(90, 0, 0) * extrude(RectangleRounded(20.0, 26.0, 4.0), amount=2.5, both=True)
        lever = _fillet_try(lever, lever.faces().sort_by(Axis.Y)[0].edges(), [1.2, 0.8])
        lever -= Pos(x, -sy - 8.5, rim - 4) * Box(12.0, 2.0, 3.0)
        keeper = Pos(x, -sy - 1.5, rim + 2.5) * Rot(90, 0, 0) * extrude(RectangleRounded(16.0, 5.0, 1.5), amount=1.5, both=True)
        keeper += Pos(x, -sy - 4.0, rim + 3.5) * Box(12.0, 4.0, 3.0)
        bases = base if bases is None else bases + base
        levers = lever if levers is None else levers + lever
        keepers = keeper if keepers is None else keepers + keeper
    return bases + keepers, levers


def _handle(P, L):
    """Bail handle (BOM 3): steel bail swept round the lid, ribbed rubber grip, pivot bosses, screws."""
    sy = L["sh_y"]
    top = P["handle_top"]
    a = sy + 5.0
    pts = [(0, -a, PIVOT_Z), (0, -a, top), (0, a, top), (0, a, PIVOT_Z)]
    with BuildLine() as bl:
        FilletPolyline(*pts, radius=22.0)
    path = bl.wire()
    prof = Plane(origin=pts[0], z_dir=(0, 0, 1)) * Circle(5.0)
    bail = sweep(prof, path)
    eyes = None
    for s in (-1, 1):
        eye = Pos(0, s * (sy + 7.0), PIVOT_Z) * Rot(90, 0, 0) * Cylinder(8.0, 6.0)
        eyes = eye if eyes is None else eyes + eye
    bail = bail + eyes
    hd = P["handle_d"]
    gl = 2 * sy - 2 * 22.0 - 6.0
    grip = Pos(0, 0, top) * Rot(90, 0, 0) * Cylinder(hd / 2, gl)
    grip = _fillet_try(grip, grip.edges(), [3.0, 2.0, 1.0])
    for i in range(-5, 6):
        grip -= Pos(0, i * 9.0, top) * Rot(90, 0, 0) * (Cylinder(hd / 2 + 1, 1.6) - Cylinder(hd / 2 - 0.7, 2.0))
    bosses, screws = None, None
    for s in (-1, 1):
        b = Pos(0, s * (sy + 2.0), PIVOT_Z) * Rot(90, 0, 0) * Cylinder(12.0, 4.0)
        b = _fillet_try(b, b.faces().sort_by(Axis.Y)[0 if s < 0 else -1].edges(), [1.2, 0.8])
        bosses = b if bosses is None else bosses + b
        sc = Pos(0, s * (sy + 10.75), PIVOT_Z) * Rot(90, 0, 0) * Cylinder(4.5, 1.5)
        screws = sc if screws is None else screws + sc
    return bail, grip, bosses, screws


def _housings(P, L):
    """End housings (BOM 10): cooling head at +X with window, grille, intake slots and inlets; bay at -X."""
    sx, top, wt = L["sh_x"], L["lid_top"], P["end_wall"]
    ew, hx1, bx0 = P["end_w"] / 2, L["head_x1"], L["bay_x0"]
    zc = L["block_z0"] + P["block"][2] / 2

    def shell(x0, x1, outer_x):
        s = _box(x0, x1, -ew, ew, 0, top)
        vert = [e for e in s.edges().filter_by(Axis.Z) if abs(e.center().X - outer_x) < 1]
        s = _fillet_try(s, vert, [10.0, 6.0, 3.0])
        inner_x = x0 if outer_x == x1 else x1
        keep = lambda es: [e for e in es if not (abs(e.center().X - inner_x) < 1 and e.length > 100)]
        s = _fillet_try(s, keep(_top_edges(s)), [3.0, 2.0, 1.0])
        s = _fillet_try(s, keep(_bottom_edges(s)), [1.5, 1.0])
        return s

    head = shell(sx, hx1, hx1) - _box(sx - 1, hx1 - wt, -ew + wt, ew - wt, wt, top - wt)
    for i in range(7):                                   # exhaust grille on the +X face (as model.py)
        z = zc - 32 + i * 10
        head -= _slot_x(hx1 - wt - 1, wt + 3, 0, z + 2.5, 70.0, 5.0)
    for i in range(5):                                   # intake slots on the front face (as model.py)
        x = sx + 12 + i * 9
        head -= _slot_y(-ew - 1, wt + 3, x + 2.5, 50.0, 5.0, 40.0)
    # window over the heat sink in the top of the cooling head (appearance proposal)
    win_l, win_w = hx1 - sx - 18.0, 88.0
    win_x = (sx + hx1) / 2 - 1.0
    head -= _prism(win_l + 3, win_w + 3, 5.0, top - 0.8, 2.0, x=win_x)
    head -= _prism(win_l, win_w, 4.0, top - wt - 1, wt + 2, x=win_x)
    window = _prism(win_l + 2.6, win_w + 2.6, 4.8, top - 0.8, 0.8, x=win_x)
    # USB-C and 12 V inlets low on the +X face (appearance proposal)
    head -= _slot_x(hx1 - wt - 1, wt + 3, -28.0, 36.0, 9.4, 3.8)
    head -= Pos(hx1 - wt / 2, 22.0, 36.0) * Rot(0, 90, 0) * Cylinder(8.0, wt + 2)
    bay = shell(bx0, -sx, bx0) - _box(bx0 + wt, -sx + 1, -ew + wt, ew - wt, wt, top - wt)
    for i in range(4):                                   # vents on the -X face (as model.py)
        z = 30 + i * 10
        bay -= _slot_x(bx0 - 1, wt + 2, 0, z + 2, 60.0, 4.0)
    # display pocket: the module sits in a shallow recess (top face stays at lid_top)
    return head, bay, window, zc


def _inlets(P, L):
    hx1, wt = L["head_x1"], P["end_wall"]
    usb = _slot_x(hx1 - 4.0, 4.0, -28.0, 36.0, 9.0, 3.4) - _slot_x(hx1 - 0.8, 1.0, -28.0, 36.0, 8.0, 2.4)
    usb += Pos(hx1 - 1.6, -28.0, 36.0) * Box(1.2, 6.6, 0.7)
    dc = Pos(hx1 - 3.0, 22.0, 36.0) * Rot(0, 90, 0) * (Cylinder(7.6, 6.0) - Pos(0, 0, 2.0) * Cylinder(5.5, 4.0))
    dc += Pos(hx1 - 3.0, 22.0, 36.0) * Rot(0, 90, 0) * Cylinder(1.2, 5.0)
    flange = Pos(hx1 + 0.4, 22.0, 36.0) * Rot(0, 90, 0) * (Cylinder(10.5, 0.8) - Cylinder(7.6, 1.0))
    return usb, dc, flange


def _housing_screws(P, L):
    hx1, bx0 = L["head_x1"], L["bay_x0"]
    out = []
    for x, s in ((hx1, 1), (bx0, -1)):
        heads = None
        for y in (-66.0, 66.0):
            for z in (12.0, 156.0):
                h = Pos(x + s * 0.75, y, z) * Rot(0, 90, 0) * Cylinder(3.0, 1.5)
                h -= Pos(x + s * 1.3, y, z) * Rot(0, 90, 0) * extrude(RegularPolygon(1.3, 6), amount=1.0, both=True)
                heads = h if heads is None else heads + h
        out.append(heads)
    return out


def _display(P, L):
    """E-paper display and alarm (BOM 15): bezel, lit screen, readout, status lights, buzzer holes."""
    bx0, top = L["bay_x0"], L["lid_top"]
    cxd = bx0 + 22.0
    bezel = _prism(30.0, 66.0, 4.0, top, 3.0, x=cxd)
    bezel = _fillet_try(bezel, _top_edges(bezel), [1.2, 0.8])
    bezel -= _prism(22.0, 54.0, 1.5, top + 2.4, 2.0, x=cxd)
    screen = _prism(22.0, 54.0, 1.5, top + 2.4, 0.4, x=cxd)
    ink_z = top + 2.8
    big = Pos(cxd + 1.0, 2.0, ink_z) * Rot(0, 0, -90) * extrude(_text("4.8°C", 12.0), amount=0.12)
    small = Pos(cxd - 7.0, 0.0, ink_z) * Rot(0, 0, -90) * extrude(
        _text("MIN 3.9   MAX 6.1   OK", 3.2, str(HERE.parents[2] / ".kit" / "fonts" / "IBMPlexSans-Medium.ttf")), amount=0.12)
    bar = Pos(cxd + 8.5, 0.0, ink_z + 0.06) * Box(1.2, 46.0, 0.12)
    ink = big + small + bar
    ring_g = Pos(cxd, 50.0, top + 1.0) * (Cylinder(6.5, 2.0) - Cylinder(5.0, 3.0))
    ring_r = Pos(cxd, -50.0, top + 1.0) * (Cylinder(6.5, 2.0) - Cylinder(3.6, 3.0))
    green = Pos(cxd, 50.0, top + 2.0) * Cylinder(5.0, 4.0)
    green = _fillet_try(green, _top_edges(green), [1.5, 1.0])
    red = Pos(cxd, -50.0, top + 1.5) * Cylinder(3.6, 3.0)
    red = _fillet_try(red, _top_edges(red), [1.2, 0.8])
    return bezel + ring_g + ring_r, screen, ink, green, red


def _label(P, L):
    """Front label: dark plate with white wordmark and range marking on the tub front."""
    sy = L["sh_y"]
    y0 = -sy
    plate = Pos(0, y0 - 0.3, 58.0) * Rot(90, 0, 0) * extrude(RectangleRounded(96.0, 34.0, 4.0), amount=0.3, both=True)
    t1 = Pos(0.0, y0 - 0.6, 62.0) * Rot(90, 0, 0) * extrude(_text("ColdPod", 11.0), amount=0.15, both=True)
    t2 = Pos(0.0, y0 - 0.6, 48.0) * Rot(90, 0, 0) * extrude(
        _text("MEDICINE COOLER  2 to 8 °C", 3.6, str(HERE.parents[2] / ".kit" / "fonts" / "IBMPlexSans-Medium.ttf")), amount=0.15, both=True)
    return plate, t1 + t2


def _fan(P, L, zc):
    fx, fy, fz = P["fan"]
    sx, bx, tx = L["sh_x"], P["block"][0], P["tec"][0]
    f0 = sx + bx + tx + P["sink_base"] + P["sink_fin"] + 1
    frame = _box(f0, f0 + fx, -fy / 2, fy / 2, zc - fz / 2, zc + fz / 2) - Pos(f0 + fx / 2, 0, zc) * Rot(0, 90, 0) * Cylinder(fy / 2 - 4, fx + 2)
    frame = _fillet_try(frame, frame.edges().filter_by(Axis.X), [3.0, 2.0])
    hub = Pos(f0 + fx / 2, 0, zc) * Rot(0, 90, 0) * Cylinder(10, fx)
    for k in range(7):
        blade = Pos(f0 + fx / 2, 0, zc) * Rot(360.0 * k / 7, 0, 0) * Rot(0, 0, 30) * Pos(0, 0, 20.0) * Box(1.2, 13.0, 22.0)
        hub += blade
    return frame, hub


def product_parts(P=PARAMS):
    L = levels(P)
    m = {k: s for k, _, s, _ in build_parts(P)}
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    sx, sy = L["sh_x"], L["sh_y"]
    cx, cy, px, py = L["cav_x"], L["cav_y"], L["pcm_x"], L["pcm_y"]
    vx, vy = L["vip_x"], L["vip_y"]

    # ---- exploded stack offsets (mm)
    E_TUB = (0, 0, -200)
    E_VIP = (0, 0, 0)
    E_THERMO = (0, 0, 170)
    E_JACKET = (0, 0, 290)
    E_LINER = (0, 0, 400)
    E_LIDPLATE = (0, 0, 430)
    E_LIDPCM = (0, 0, 465)
    E_LIDVIP = (0, 0, 500)
    E_GASKET = (0, 0, 535)
    E_LID = (0, 0, 555)
    E_HANDLE = (0, 0, 670)
    E_HEAD = (420, 0, 0)
    E_BAY = (-220, 0, 0)

    # ---- outer shell, bumper, gasket, lid, latches, handle (shell group)
    tub, gasket, bumper = _tub(P, L)
    add("Outer shell (tub)", tub, C_TUB, "plastic", 1, "shell", E_TUB)
    add("Base bumper (TPE)", bumper, C_RUBBER, "rubber", 1, "shell", E_TUB)
    add("Lid gasket (EPDM)", gasket, C_RUBBER, "rubber", 2, "shell", E_GASKET)
    lid, word, mark = _lid(P, L)
    add("Lid cap", lid, C_LID, "plastic", 2, "shell", E_LID)
    add("Lid wordmark", word, C_ACCENT, "painted", 2, "shell", E_LID)
    add("Lid range marking", mark, "#6B7280", "painted", 2, "shell", E_LID)
    lbases, levers = _latches(P, L)
    add("Draw latch bases and keepers", lbases, C_STEEL, "metal", 2, "shell", E_TUB)
    add("Draw latch levers", levers, C_ACCENT, "plastic", 2, "shell", E_TUB)
    plate, ltext = _label(P, L)
    add("Front label plate", plate, "#2B2F36", "painted", 16, "shell", E_TUB)
    add("Front label text", ltext, C_WHITE, "painted", 16, "shell", E_TUB)
    bail, grip, bosses, pscrews = _handle(P, L)
    add("Bail handle (steel)", bail, C_STEEL, "metal", 3, "shell", E_HANDLE)
    add("Handle grip (ribbed rubber)", grip, C_RUBBER, "rubber", 3, "shell", E_HANDLE)
    add("Handle pivot bosses", bosses, C_HOUSING, "plastic", 3, "shell", E_TUB)
    add("Handle pivot screws", pscrews, C_ALU, "metal", 16, "shell", E_HANDLE)

    # ---- end housings (shell group)
    head, bay, window, zc = _housings(P, L)
    add("Cooling head housing", head, C_HOUSING, "plastic", 10, "shell", E_HEAD)
    add("Cooling head window (smoked)", window, C_WINDOW, "clear", 10, "shell", (E_HEAD[0], 0, 60))
    add("Battery and electronics bay housing", bay, C_HOUSING, "plastic", 10, "shell", E_BAY)
    hs_head, hs_bay = _housing_screws(P, L)
    add("Cooling head screws", hs_head, C_ALU, "metal", 16, "shell", E_HEAD)
    add("Battery bay screws", hs_bay, C_ALU, "metal", 16, "shell", E_BAY)
    usb, dc, flange = _inlets(P, L)
    add("USB-C PD inlet", usb, C_CHIP, "plastic", 12, "shell", E_HEAD)
    add("12 V inlet", dc, C_CHIP, "plastic", 12, "shell", E_HEAD)
    add("12 V inlet trim ring", flange, C_ALU, "metal", 12, "shell", E_HEAD)

    # ---- display and alarm (BOM 15)
    bezel, screen, ink, green, red = _display(P, L)
    E_DISP = (E_BAY[0], 0, 80)
    add("Display bezel and light rings", bezel, C_FAN, "plastic", 15, "shell", E_DISP)
    add("E-paper display (lit)", screen, C_SCREEN, "emissive", 15, "shell", E_DISP)
    add("Display readout", ink, C_INK, "paper", 15, "shell", E_DISP)
    add("Status light, green (lit)", green, C_GREEN, "emissive", 15, "shell", E_DISP)
    add("Alarm light, red", red, C_RED, "plastic", 15, "shell", E_DISP)

    # ---- insulation, PCM, liner and payload (internal group)
    lid_vip = _box(-px, px, -py, py, L["lidpcm_z1"], L["rim"])
    body_vip = m["vip"] - _box(-px - 1, px + 1, -py - 1, py + 1, L["lidpcm_z1"] - 0.01, L["rim"] + 1)
    add("VIP set, body panels", body_vip, C_VIP, "metal", 4, "internal", E_VIP)
    add("VIP lid plug", lid_vip, C_VIP, "metal", 4, "internal", E_LIDVIP)
    lid_pcm = _box(-px, px, -py, py, L["plate_z1"], L["lidpcm_z1"])
    jacket = m["pcm"] - _box(-px - 1, px + 1, -py - 1, py + 1, L["plate_z1"] - 0.01, L["lidpcm_z1"] + 1)
    add("PCM jacket pouches", jacket, C_PCM, "plastic", 5, "internal", E_JACKET)
    lid_pcm = _fillet_try(lid_pcm, lid_pcm.edges().filter_by(Axis.Z), [6.0, 3.0])
    add("PCM lid pack", lid_pcm, C_PCM, "plastic", 5, "internal", E_LIDPCM)
    add("Lid cold plate", m["lidplate"], C_ALU, "metal", 2, "internal", E_LIDPLATE)
    lt, rt = P["liner_t"], P["rack_t"]
    liner = _box(-cx, cx, -cy, cy, L["cav_z0"], L["cav_z1"]) - _box(-cx + lt, cx - lt, -cy + lt, cy - lt, L["cav_z0"] + lt, L["cav_z1"] + 1)
    add("Aluminium liner", liner, C_ALU, "metal", 6, "internal", E_LINER)
    rack = m["liner"] - liner
    add("Payload rack (PETG)", rack, C_RACK, "plastic", 6, "internal", E_LINER)
    add("Payload: insulin pens (not supplied)", m["pens"], C_PEN, "plastic", None, "internal", (0, 0, 470))
    # sensors as model.py: payload probe, liner probe and liner cut-out inside; ambient sensor at the intake
    rz0 = L["cav_z0"] + lt
    ew = P["end_w"] / 2
    probes = (Pos(cx - 12, -cy + 12, rz0 + rt + 18) * Cylinder(7, 36)
              + _box(cx - 20, cx - 8, cy - lt - 3, cy - lt, L["cav_z0"] + 30, L["cav_z0"] + 36)
              + _box(cx - lt - 4, cx - lt, -8, 8, L["cav_z0"] + 50, L["cav_z0"] + 62))
    add("Temperature probes and liner cut-out", probes, "#C9A227", "metal", 14, "internal", (0, -200, 400))
    amb = _box(sx + 14, sx + 30, -ew - 3, -ew, 80, 92)
    amb = _fillet_try(amb, amb.edges().filter_by(Axis.Y), [1.5, 1.0])
    for i in range(3):
        amb -= _box(sx + 17 + i * 4, sx + 19 + i * 4, -ew - 4, -ew - 2.2, 83, 89)
    add("Ambient sensor cap", amb, "#4B5563", "plastic", 14, "shell", E_HEAD)

    # ---- evaporator can, loop thermosiphon, cold block (BOM 7)
    ct = P["can_t"]
    can = _box(-px, px, -py, py, L["pcm_z0"], L["cav_z1"]) - _box(-px + ct, px - ct, -py + ct, py - ct, L["pcm_z0"] + ct, L["cav_z1"] + 1)
    bxb, byb, bzb = P["block"]
    block = _box(sx, sx + bxb, -byb / 2, byb / 2, L["block_z0"], L["block_z0"] + bzb)
    loop = m["thermo"] - can - block
    add("Evaporator can", can, C_ALU, "metal", 7, "internal", E_THERMO)
    add("Loop thermosiphon (copper)", loop, C_COPPER, "metal", 7, "internal", E_THERMO)
    add("Cold block", block, "#9EA6AE", "metal", 7, "internal", E_THERMO)

    # ---- cooling head internals (BOM 8, 9, 12)
    add("Peltier module", m["tec"], C_TEC, "plastic", 8, "internal", (120, 0, 0))
    tx = P["tec"][0]
    h0 = sx + bxb + tx
    sw, sh = P["sink_w"], P["sink_h"]
    sink = _box(h0, h0 + P["sink_base"], -sw / 2, sw / 2, zc - sh / 2, zc + sh / 2)
    for i in range(P["fins"]):
        y = -sw / 2 + 1 + i * (sw - 2) / (P["fins"] - 1)
        sink += _box(h0 + P["sink_base"], h0 + P["sink_base"] + P["sink_fin"], y - 1, y + 1, zc - sh / 2, zc + sh / 2)
    add("Heat sink", sink, C_SINK, "metal", 9, "internal", (200, 0, 0))
    frame, rotor = _fan(P, L, zc)
    add("Fan frame", frame, C_FAN, "plastic", 9, "internal", (300, 0, 0))
    add("Fan rotor", rotor, "#2A2E35", "plastic", 9, "internal", (300, 0, 0))
    power = m["power"]
    add("Power board", power, C_PCB, "plastic", 12, "internal", (330, 0, -110))
    pc = None
    for (x, y, w, d, h) in ((158, -40, 18, 14, 8), (172, 10, 12, 12, 10), (150, 30, 10, 20, 6), (178, -20, 8, 8, 12)):
        c = Pos(x, y, 14 + h / 2) * Box(w, d, h)
        pc = c if pc is None else pc + c
    add("Power board modules", pc, C_CHIP, "plastic", 12, "internal", (330, 0, -110))

    # ---- battery and logger (BOM 11, 13)
    bx0, wt = L["bay_x0"], P["end_wall"]
    cd, ch, n = P["cell_d"], P["cell_h"], P["cells"]
    cells, caps = None, None
    for i in range(n):
        y = (i - (n - 1) / 2) * (cd + 2)
        xc = bx0 + wt + 2 + cd / 2
        c = Pos(xc, y, wt + 2 + ch / 2) * Cylinder(cd / 2, ch - 1.0)
        c = _fillet_try(c, c.edges(), [1.0, 0.5])
        cells = c if cells is None else cells + c
        cap = Pos(xc, y, wt + 2 + ch - 0.5) * Cylinder(cd / 2 - 2.0, 1.0)
        caps = cap if caps is None else caps + cap
    add("LiFePO4 cells", cells, C_CELL, "painted", 11, "internal", (-120, 0, 0))
    add("Cell terminals", caps, C_ALU, "metal", 11, "internal", (-120, 0, 0))
    bms = _box(bx0 + wt + 2, bx0 + wt + 2 + cd, -n * (cd + 2) / 2, n * (cd + 2) / 2, wt + 4 + ch, wt + 10 + ch)
    add("BMS board", bms, C_PCB, "plastic", 11, "internal", (-120, 0, 40))
    add("Logger controller board", m["logger"], C_PCB_DARK, "plastic", 13, "internal", (-80, 0, 60))

    # ---- accessory: padded shoulder strap, laid in front of the case
    ys, zs = -sy - 70.0, 0.0
    pad = _prism(200.0, 40.0, 14.0, zs, 10.0, y=ys)
    pad = _fillet_try(pad, _top_edges(pad), [4.0, 3.0, 2.0])
    add("Shoulder strap pad", pad, C_FABRIC, "fabric", 3, "accessory", (0, -80, -200))
    web = _box(-260, 260, ys - 12.5, ys + 12.5, zs, zs + 2.0)
    add("Shoulder strap webbing", web, "#3B424C", "fabric", 3, "accessory", (0, -80, -200))
    hooks = None
    for s in (-1, 1):
        hk = Pos(s * 272.0, ys, zs + 3.0) * (_prism(26.0, 30.0, 8.0, -3.0, 6.0) - _prism(14.0, 18.0, 4.0, -4.0, 8.0))
        hooks = hk if hooks is None else hooks + hk
    add("Shoulder strap snap hooks", hooks, C_STEEL, "metal", 3, "accessory", (0, -80, -200))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:40s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:8.2f} cm3")
