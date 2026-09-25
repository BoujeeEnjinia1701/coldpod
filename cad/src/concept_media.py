"""ColdPod concept media (TRL 3), generated from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Massing-plus model: main dimensions and interfaces; not for fabrication.

Axes: X along the case length (battery and electronics bay at -X, cooling head at +X),
Y front (-Y) to back (+Y), Z up. Units mm. Numbers on the media come from
docs/04-calcs/sizing.py (CPD-CAL-001) and are estimates.
"""
import contextlib
import io
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parents[2] / ".kit"), str(HERE.parent), str(HERE.parents[2] / "docs" / "04-calcs")]
from build123d import Box, Pos  # noqa: E402
from concept import Part, render_all  # noqa: E402
from model import build_parts  # noqa: E402

COLORS = {"shell": "#D1D5DB", "lid": "#9CA3AF", "handle": "#374151", "vip": "#E7E5E4", "pcm": "#60A5FA",
          "liner": "#A8A29E", "pens": "#F9FAFB", "thermo": "#B87333", "tec": "#F3F4F6", "sink": "#4B5563",
          "housings": "#0F766E", "cells": "#C2410C", "power": "#15803D", "logger": "#1F2937",
          "sensors": "#D4A017", "display": "#38BDF8"}
EXPLODE = {"shell": (0, 0, -260), "thermo": (0, 0, 180), "pcm": (0, 0, 320), "liner": (0, 0, 460),
           "pens": (0, 0, 460), "lid": (0, 0, 600), "handle": (0, 0, 720), "tec": (150, 0, 0),
           "sink": (220, 0, 0), "housings": (0, 0, -260), "cells": (-170, 0, 0), "power": (110, 0, -40),
           "logger": (-120, 0, 70), "sensors": (0, -190, 0), "display": (-60, 0, 170)}
parts = [Part(name, shape, COLORS[k], bom, EXPLODE.get(k, (0, 0, 0))) for k, name, shape, bom in build_parts()]

# Context for scale: a table top and a phone lying next to the case
table = Pos(35, -30, -12.5) * Box(590, 440, 25)
phone = Pos(252, -160, 4.5) * Box(75, 150, 9)
context = [Part("Table top", table, "#C8CDD3"), Part("phone", phone, "#6B7280")]

with contextlib.redirect_stdout(io.StringIO()):
    import sizing as C  # noqa: E402

h32 = C.HOLD[(C.MODULE, 32.0)]

if __name__ == "__main__":
    render_all(
        parts, project="ColdPod", title="Portable medicine cooler concept", dwg_no="CPD-DWG-010",
        key_figures=[f"{C.V_use:.2f} L payload at 2 to 8 °C (24 insulin pens)",
                     f"No power: about {C.t4:.0f} h at 43 °C, {C.passive(32.0)[0]:.0f} h at 32 °C (est.)",
                     f"Battery then PCM: about {C.F[32.0][2]:.0f} h at 32 °C, {C.F[43.0][2]:.1f} h at 43 °C (est.)",
                     f"PCM jacket refreeze about {C.t_ref:.1f} h on 12 V or USB-C PD (est.)",
                     "Logs every 1 min; alarms outside 2 to 8 °C",
                     f"About {C.ov_x:.0f} x {C.ov_y:.0f} x {C.ov_z:.0f} mm, {C.M_tot:.1f} kg empty (est.)"],
        scale_figure=False, context=context, cut_exclude=("Bail handle and shoulder strap",),
        flow={"title": "heat flow, powered hold at 32 °C ambient (all values are estimates, CPD-CAL-001)", "unit": "",
              "stages": [("Ambient heat leak", f"{h32['q']:.1f} W through walls"),
                         ("PCM buffer at 5 °C", f"{C.E_pcm / 1e3:.0f} kJ latent"),
                         ("Thermosiphon diode", "carries heat up only"),
                         ("Peltier module", f"{h32['q']:.1f} W lifted, {h32['p']:.1f} W in"),
                         ("Heat sink and fan", f"{h32['qh']:.1f} W to ambient")]},
    )
