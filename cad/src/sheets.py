"""ColdPod general arrangement sheet CPD-DWG-001, Rev P2 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/CPD-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Overall dimensions are drawn from the model
bounding box and PARAMS, so they follow any parameter change. The concept sheet in
media/ is CPD-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, project_views, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, build, levels  # noqa: E402

DATE = "2026-09-25"


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text):
    a = 1.4
    cx, cy = x - 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def main():
    Lv = levels()
    work = ROOT / "cad" / "drawings" / "_views"
    asm = build()
    views = project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="ColdPod", title="General arrangement", dwg_no="CPD-DWG-001", rev="P3",
              author="Amish Chadha", date=DATE, scale=1 / 5, theme="technical",
              material="Printed PETG shell, 25 mm VIPs, 5 °C PCM, aluminium liner; see bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Lid cold plate, liner cut-out, thinner walls (CPD-DDR-002)", DATE, "AC"),
                         ("P3", "Layout and labels tidied", "2026-09-30", "AC")])
    s.add_ortho(views, dims=False)
    k = s.scale
    c = ortho_cells(s, views)
    out = []
    # top view: overall length above, overall width at left, shell body length below
    x, y, w, h = c["top"]
    out += dim_h(x, x + w, y - 3.5, f"{bb.size.X:.0f} overall")
    out += dim_v(x - 4, y, y + h, f"{bb.size.Y:.0f}")
    xs0 = x + (-Lv["sh_x"] - bb.min.X) * k
    xs1 = x + (Lv["sh_x"] - bb.min.X) * k
    out += [ext(xs0, y + 2, xs0, y - 10), ext(xs1, y + 2, xs1, y - 10)]
    out += dim_h(xs0, xs1, y - 9, f"{2 * Lv['sh_x']:.0f} body")
    # front view (from -Y): overall height, rim and lid top at left
    x, y, w, h = c["front"]
    zb = y + h
    out += dim_v(x - 4, y, zb, f"{bb.size.Z:.0f} handle up")
    zt = zb - Lv["lid_top"] * k
    out += [ext(x - 11, zt, x + (-Lv["sh_x"] - bb.min.X) * k, zt)]
    out += dim_v(x - 10, zt, zb, f"{Lv['lid_top']:.0f}")
    # right view (from +X): shell width and end housing width
    x, y, w, h = c["right"]
    yc = x + w / 2
    wl, wr = yc - Lv["sh_y"] * k, yc + Lv["sh_y"] * k
    ys = y + h - Lv["lid_top"] * k
    out += [ext(wl, ys, wl, y - 5), ext(wr, ys, wr, y - 5)]
    out += dim_h(wl, wr, y - 4, f"{2 * Lv['sh_y']:.0f} shell")
    s._layers += out
    s.add_svg(views["iso"], 276, 44, 140, 82, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Overall {bb.size.X:.0f} L x {bb.size.Y:.0f} W x {bb.size.Z:.0f} H, handle up",
        f"Body {2 * Lv['sh_x']:.0f} x {2 * Lv['sh_y']:.0f} x {Lv['lid_top']:.0f}; bay {P['bay_l']:.0f}, head {P['head_l']:.0f}",
        f"Liner {P['cav_l']:.0f} x {P['cav_w']:.0f} x {P['cav_h']:.0f} outside; 24 pens, 4 x 6",
        f"PCM jacket {P['pcm_t']:.0f} in a {P['can_t']:.1f} Al can; lid pack {P['lid_pcm_t']:.0f}",
        f"Lid cold plate {P['lid_plate_t']:.1f} Al, seats on can rim",
        f"VIP {P['vip_t']:.0f}; shell {P['shell_t']:.0f}; lid cap {P['lid_cap_t']:.0f}; housings {P['end_wall']:.0f}",
        f"Thermosiphon loop Z {Lv['loop_z']:.1f}; pipes cross +X wall at Z {P['pipe_exit_z']:.0f}, Y +/-{P['pipe_y']:.0f}",
        "Peltier 40 x 40 (TEC1-12703 class); sink 80 x 80 x 30",
        "Cut-outs in series: cold block −5 °C, liner 3 °C",
        "Empty mass about 5.53 kg (CPD-CAL-001 v0.2, K2)",
        "Third-angle; front view from -Y, right view from +X",
    ], x=276, y=145, width=140)
    path = s.save(ROOT / "cad" / "drawings" / "CPD-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {path} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
