"""ColdPod concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the case length (electronics and battery bay at -X, cooling head at +X),
Y front (-Y) to back (+Y), Z up. Units mm.
Layers from the inside out: payload cavity in an aluminium liner (175 x 110 x 80 mm),
15 mm phase-change material (PCM) jacket, 25 mm vacuum-insulated panels (VIP), 4 mm outer shell.
A gravity thermosiphon (a one-way thermal diode) carries heat up and out from an evaporator
plate on the outer face of the PCM to a cold block on the Peltier module in the +X cooling head.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


# Key envelopes (half widths in X and Y, mm)
CAV_X, CAV_Y, CAV_Z0, CAV_Z1 = 87.5, 55.0, 44.0, 124.0     # payload cavity (liner outside)
PCM_X, PCM_Y, PCM_Z0 = 102.5, 70.0, 29.0                   # PCM jacket outside
VIP_X, VIP_Y, VIP_Z0 = 127.5, 95.0, 4.0                    # VIP outside
SH_X, SH_Y, SH_T = 131.5, 99.0, 4.0                        # outer shell
RIM = 164.0                                                # top of the body walls
LID_TOP = 172.0

# 1 Outer shell: open-topped tub
shell = box(-SH_X, SH_X, -SH_Y, SH_Y, 0, RIM) - box(-VIP_X, VIP_X, -VIP_Y, VIP_Y, SH_T, RIM + 1)
for y in (-25, 25):  # pass-throughs for the thermosiphon into the cooling head
    shell = shell - Pos(SH_X - 2, y, 112) * Rot(0, 90, 0) * Cylinder(5, 8)

# 2 Lid: cap with gasket, VIP plug under it
lid = box(-SH_X, SH_X, -SH_Y, SH_Y, RIM, LID_TOP) + box(-PCM_X, PCM_X, -PCM_Y, PCM_Y, 139, RIM)

# 3 Bail handle, pivots on the front and back faces
handle = (box(-8, 8, -SH_Y - 8, -SH_Y, 128, 199) + box(-8, 8, SH_Y, SH_Y + 8, 128, 199)
          + Pos(0, 0, 199) * Rot(90, 0, 0) * Cylinder(8, 2 * SH_Y + 16))

# 4 VIP set: five body panels (walls and floor)
vip = box(-VIP_X, VIP_X, -VIP_Y, VIP_Y, VIP_Z0, RIM) - box(-PCM_X, PCM_X, -PCM_Y, PCM_Y, PCM_Z0, RIM + 1)
for y in (-25, 25):  # foam-plugged gap where the heat pipes cross (VIPs cannot be pierced)
    vip = vip - Pos(115, y, 112) * Rot(0, 90, 0) * Cylinder(8, 26)

# 5 PCM packs: jacket around the liner plus a lid pack
evap = box(99.5, PCM_X, -45, 45, 35, 95)
pcm = (box(-PCM_X, PCM_X, -PCM_Y, PCM_Y, PCM_Z0, CAV_Z1) - box(-CAV_X, CAV_X, -CAV_Y, CAV_Y, CAV_Z0, CAV_Z1 + 1)
       - evap - box(94, PCM_X, -30, 30, 35, 118))
pcm_lid = box(-PCM_X, PCM_X, -PCM_Y, PCM_Y, CAV_Z1, 139)

# 6 Aluminium liner and payload rack
liner = (box(-CAV_X, CAV_X, -CAV_Y, CAV_Y, CAV_Z0, CAV_Z1)
         - box(-CAV_X + 1.5, CAV_X - 1.5, -CAV_Y + 1.5, CAV_Y - 1.5, CAV_Z0 + 1.5, CAV_Z1 + 1))
rack = box(-84, 84, -52, 52, 45.5, 47.5)
for y in (-18, 18):
    rack = rack + box(-84, 84, y - 1, y + 1, 47.5, 100)
liner = liner + rack

# Payload (not supplied): two layers of insulin pens
pens = None
for z in (56.0, 73.0):
    for y in (-44, -28, -8, 8, 28, 44):
        pen = Pos(-4, y, z) * Rot(0, 90, 0) * Cylinder(7.5, 160)
        pens = pen if pens is None else pens + pen

# 7 Thermosiphon: evaporator plate on the outer face of the PCM, two pipes, cold block
pipes = evap
for y in (-25, 25):
    pipes = pipes + Pos(97, y, 76) * Cylinder(4, 72)                          # riser, 40 to 112
    pipes = pipes + Pos(119, y, 112) * Rot(0, 90, 0) * Cylinder(4, 44)        # out through the wall
pipes = pipes + box(SH_X, SH_X + 10, -35, 35, 97, 127)                        # cold block (condenser)

# 8 Peltier module, 40 x 40 mm
tec = box(SH_X + 10, SH_X + 14, -20, 20, 92, 132)

# 9 Hot-side heat sink and 70 mm fan
HS0 = SH_X + 14
sink = box(HS0, HS0 + 6, -40, 40, 72, 152)
for i in range(9):
    y = -40 + i * 10
    sink = sink + box(HS0 + 6, HS0 + 30, y - 1, y + 1, 72, 152)
fan = box(HS0 + 31, HS0 + 41, -35, 35, 77, 147) - Pos(HS0 + 36, 0, 112) * Rot(0, 90, 0) * Cylinder(31, 12)
fan = fan + Pos(HS0 + 36, 0, 112) * Rot(0, 90, 0) * Cylinder(10, 10)
sink = sink + fan

# 10 End housings: cooling head (+X) and battery and electronics bay (-X)
CH1 = SH_X + 60
head = box(SH_X, CH1, -80, 80, 0, LID_TOP) - box(SH_X, CH1 - 3, -77, 77, 3, LID_TOP - 3)
for i in range(7):  # exhaust grille on the +X face
    z = 80 + i * 10
    head = head - box(CH1 - 4, CH1 + 1, -35, 35, z, z + 5)
for i in range(5):  # intake slots on the front face, low down
    x = SH_X + 12 + i * 9
    head = head - box(x, x + 5, -81, -76, 30, 70)
BX0 = -SH_X - 45
bay = box(BX0, -SH_X, -80, 80, 0, LID_TOP) - box(BX0 + 3, -SH_X, -77, 77, 3, LID_TOP - 3)
housings = head + bay

# 11 LiFePO4 pack: 4S1P 32700 cells standing in the -X bay
cells = None
for y in (-51, -17, 17, 51):
    c = Pos(BX0 + 22.5, y, 43) * Cylinder(16, 70)
    cells = c if cells is None else cells + c
cells = cells + box(BX0 + 8, BX0 + 37, -68, 68, 80, 86)   # BMS board on top of the cells

# 12 Power board: USB-C PD and 12 V input, LiFePO4 charger, Peltier and fan drivers
power = box(SH_X + 8, CH1 - 8, -65, 65, 8, 14)

# 13 Logger controller board, standing in the -X bay
logger = box(-SH_X - 6, -SH_X - 3, -50, 50, 95, 155)

# 14 Temperature sensors: buffered payload probe in the cavity, ambient sensor at the cooling-head intake
sensors = Pos(70, -40, 64) * Cylinder(7, 36) + box(SH_X + 14, SH_X + 30, -83, -80, 80, 92)

# 15 E-paper display and alarm (buzzer and LED) on top of the bay
display = box(BX0 + 7, BX0 + 37, -33, 33, LID_TOP, LID_TOP + 3) + Pos(BX0 + 22, 50, LID_TOP + 2) * Cylinder(5, 4)

parts = [
    Part("Outer shell", shell, "#D1D5DB", 1, (0, 0, -260)),
    Part("Lid with VIP plug and gasket", lid, "#9CA3AF", 2, (0, 0, 440)),
    Part("Bail handle and shoulder strap", handle, "#374151", 3, (0, 0, 560)),
    Part("Vacuum-insulated panels, 25 mm", vip, "#E7E5E4", 4, (0, 0, 0)),
    Part("PCM packs, 5 °C (RT 5 HC class)", pcm + pcm_lid, "#60A5FA", 5, (0, 0, 190)),
    Part("Aluminium liner and payload rack", liner, "#A8A29E", 6, (0, 0, 330)),
    Part("Payload: insulin pens (not supplied)", pens, "#F9FAFB", None, (0, 0, 330)),
    Part("Thermosiphon heat pipes and cold block", pipes, "#B87333", 7, (70, 0, 0)),
    Part("Peltier module, 40 x 40 mm", tec, "#F3F4F6", 8, (130, 0, 0)),
    Part("Hot-side heat sink and fan", sink, "#4B5563", 9, (200, 0, 0)),
    Part("End housings (cooling head, battery bay)", housings, "#0F766E", 10, (0, 0, -260)),
    Part("LiFePO4 pack, 12.8 V 6 Ah, with BMS", cells, "#C2410C", 11, (-160, 0, 0)),
    Part("Power board (USB-C PD, 12 V, drivers)", power, "#15803D", 12, (100, 0, -30)),
    Part("Logger controller (nRF52840 class)", logger, "#1F2937", 13, (-110, 0, 70)),
    Part("Temperature sensors (buffered probe)", sensors, "#D4A017", 14, (0, -190, 0)),
    Part("E-paper display and alarm", display, "#38BDF8", 15, (-60, 0, 170)),
]

# Context for scale: a table top and a phone lying next to the case
table = box(-260, 330, -250, 190, -25, 0)
phone = box(215, 290, -235, -85, 0, 9)
context = [Part("Table top", table, "#C8CDD3"), Part("phone", phone, "#6B7280")]

render_all(
    parts, project="ColdPod", title="Portable medicine cooler concept", dwg_no="CPD-DWG-010",
    key_figures=["1.2 L payload held at 2 to 8 °C (about 24 insulin pens)",
                 "No power: about 13 h at 43 °C, 18 h at 32 °C (est.)",
                 "Battery then PCM: about 26 h at 32 °C, 16 h at 43 °C (est.)",
                 "PCM refreeze about 5 h on 12 V or USB-C PD (est.)",
                 "Logs every 1 min; alarms below 2 °C and above 8 °C",
                 "About 370 x 215 x 205 mm, 5.2 kg empty (est.)"],
    scale_figure=False, context=context, cut_exclude=("Bail handle and shoulder strap",),
    flow={"title": "heat flow, powered hold at 32 °C ambient (all values are estimates)", "unit": "",
          "stages": [("Ambient heat leak", "3.0 W through walls"), ("PCM buffer at 5 °C", "191 kJ latent"),
                     ("Thermosiphon diode", "carries heat up only"), ("Peltier module", "3.0 W lifted, 7.4 W in"),
                     ("Heat sink and fan", "10.4 W to ambient")]},
)
