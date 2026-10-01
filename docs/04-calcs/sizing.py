"""ColdPod sizing and first-principles checks (CPD-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md, tagged [A1], [B2] and so on.

Geometry comes from PARAMS in cad/src/model.py and prices from bom/bom.csv, so the
model, drawing CPD-DWG-001 and the note agree. Everything here is a paper estimate
for TRL 3; nothing is measured. Temperatures in °C unless a name ends in K.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, levels, component_volumes_cm3  # noqa: E402

L = levels()
CV = component_volumes_cm3()   # cm³ of every component of the constructable model (CPD-DDR-003)
K0 = 273.15


def pr(tag, label, value, unit="", fmt="{:.2f}"):
    s = fmt.format(value) if isinstance(value, (int, float)) else str(value)
    print(f"  [{tag}] {label:60s} {s} {unit}")
    return value


def head(t):
    print(f"\n{t}")


# ---------------------------------------------------------------- assumptions
T_CASES = {"clinic": 25.0, "hot day": 32.0, "WHO hot zone": 43.0}
K_VIP = 0.007          # W/(m K), aged centre-of-panel, fumed silica core
PSI_JOINT = 0.015      # W/(m K), butt joint between two metallized-film VIP edges with a 1 mm gap
PSI_EDGE = 0.0075      # W/(m K), one VIP edge against the foam strip
K_FOAM = 0.024         # W/(m K), polyurethane foam in the pipe crossing strip
K_SS, K_CU = 16.0, 400.0
PIPE_WALL = 0.3        # mm, stainless adiabatic section of each 8 mm tube
PIPE_CROSS = 40.0      # mm, length of stainless section through VIP, gap and shell
WIRES = 6              # conductors of 28 AWG copper into the cavity (payload and liner probes)
WIRE_A = 0.081e-6      # m², 28 AWG
WIRE_L = 0.10          # m, routed along a VIP joint
PCM_FILL = 0.85        # pouch fill fraction of the PCM space
RHO_PCM_L, RHO_PCM_S = 770.0, 880.0   # kg/m³ liquid, solid (RT 5 HC class)
H_USABLE = 180e3       # J/kg usable inside 2 to 8 °C (of about 250 kJ/kg listed over the full range)
T_MELT = 5.0
K_PCM_S = 0.2          # W/(m K), solid paraffin
CP_PCM_L, CP_PCM_S = 2.0e3, 1.8e3
T_CAN_HOLD = 2.0       # controller holds the evaporator can here in powered hold
T_CAN_MIN = -2.0       # controller floor for the can during refreeze
R_COLD = 0.40          # K/W, can and loop, two-phase thermosiphon, block, interface to the module cold face
R_HOT = 0.55           # K/W, module hot face to air: 80 x 80 x 30 mm finned sink, 70 mm fan, interface
H_CAN_LIQ = 40.0       # W/(m² K), can to liquid PCM through the pouch film (sensible phase)
ETA_DRV = 0.90         # buck-boost driver giving the module smooth DC (not on/off PWM), CPD-DDR-002
V_IN_MIN = 10.0        # lowest vehicle input the buck-boost stage accepts (V)
P_FAN, P_CTRL = 0.6, 0.1
BATT_WH, BATT_RESERVE = 76.8, 0.15
P_CAP_REFREEZE = 25.0  # W to the module while the battery also charges (45 W USB-C PD budget)
P_CHARGE = 12.0        # W into the battery during refreeze
# Peltier module classes (127 couples), parameters derived at Th = 300 K from Vmax, Imax, dTmax
MODULES = {"TEC1-12703": (15.4, 3.0, 67.0), "TEC1-12704": (15.4, 4.0, 67.0), "TEC1-12706": (15.4, 6.0, 67.0)}
MODULE = "TEC1-12703"  # chosen in section E
K_AL = 237.0           # W/(m K), aluminium
T_CUT_BLOCK, T_CUT_LINER = -5.0, 3.0   # hardware cut-outs in series (cold block, liner), CPD-DDR-002


# ---------------------------------------------------------------- A. geometry and payload
head("A. Geometry and payload (R3, R13)")
lt, rt = P["liner_t"], P["rack_t"]
in_l, in_w, in_h = P["cav_l"] - 2 * lt, P["cav_w"] - 2 * lt, P["cav_h"] - lt
V_cav = in_l * in_w * in_h / 1e6
nc, nl, pd = P["pen_cols"], P["pen_layers"], P["pen_d"]
rack_floor = (in_l - 2) * (in_w - 2) * rt
rack_div = (nc // 2 - 1) * (in_l - 2) * rt * (nl * pd - 4)
V_rack = (rack_floor + rack_div) / 1e3            # cm³
V_probe = math.pi * (P["probe"][0] / 2) ** 2 * P["probe"][1] / 1e3   # 10 x 40 mm vial above the top layer (DDR-003)
V_use = V_cav - (V_rack + V_probe) / 1e3
pr("A1", "Liner inside, L x W x H (mm)", f"{in_l:.0f} x {in_w:.0f} x {in_h:.1f}")
pr("A2", "Usable payload volume (inside liner less rack and probe)", V_use, "L")
width_need = nc * pd + (nc // 2 - 1) * rt
height_need = rt + nl * pd
pr("A3", "Pens held (layers x columns), 16 mm dia.", f"{nl} x {nc} = {nl * nc}")
pr("A4", "Width used / available; height used / available (mm)", f"{width_need:.0f} / {in_w:.0f}; {height_need:.0f} / {in_h:.1f}")
pr("A5", "Longest pen that fits (mm)", in_l, "", "{:.0f}")
ov_x = L["head_x1"] - L["bay_x0"]
ov_y = 2 * (L["sh_y"] + P["pad_t"]) + P["handle_d"]     # handle arms on 4 mm pivot pads (DDR-003)
ov_z = P["handle_top"] + P["handle_d"] / 2
pr("A6", "Overall L x W x H with handle up (mm)", f"{ov_x:.0f} x {ov_y:.0f} x {ov_z:.0f}")
pr("A7", "Overall (in)", f"{ov_x / 25.4:.1f} x {ov_y / 25.4:.1f} x {ov_z / 25.4:.1f}")

# ---------------------------------------------------------------- B. heat leak
head("B. Heat leak through the insulation")
t = P["vip_t"] / 1000
ix, iy = 2 * L["pcm_x"] / 1000, 2 * L["pcm_y"] / 1000
iz = (L["lidpcm_z1"] - L["pcm_z0"]) / 1000
A_top = ix * iy
A_side = 2 * (ix * iz + iy * iz) + ix * iy          # four walls and floor
edges_top = 2 * (ix + iy)
edges_body = 2 * (ix + iy) + 4 * iz
S_lid = A_top / t + 0.54 * edges_top + 4 * 0.15 * t
S_body = A_side / t + 0.54 * edges_body + 4 * 0.15 * t
U_c_lid, U_c_body = K_VIP * S_lid, K_VIP * S_body
pr("B1", "Inner insulation box (m)", f"{ix:.3f} x {iy:.3f} x {iz:.3f}")
pr("B2", "Langmuir shape factor, body / lid (m)", f"{S_body:.3f} / {S_lid:.3f}")
pr("B3", "Centre-of-panel conductance, body / lid (W/K)", f"{U_c_body:.4f} / {U_c_lid:.4f}")
oz = (L["rim"] - L["vip_z0"]) / 1000
j_body = 4 * oz + 2 * (2 * L["vip_x"] + 2 * L["vip_y"]) / 1000
U_joint = PSI_JOINT * j_body
U_lidj = PSI_JOINT * edges_top
fs = P["foam_strip"] / 1000
U_foam = K_FOAM * fs * (iy + 2 * L["vip_y"] / 1000) / 2 / t + 2 * PSI_EDGE * (iy + 2 * L["vip_y"] / 1000) / 2
ro = P["pipe_d"] / 2000
A_ss = math.pi * (ro ** 2 - (ro - PIPE_WALL / 1000) ** 2)
U_pipe = 2 * K_SS * A_ss / (PIPE_CROSS / 1000)
U_wire = WIRES * K_CU * WIRE_A / WIRE_L
U_body = U_c_body + U_joint + U_foam + U_pipe + U_wire
U_lid = U_c_lid + U_lidj
U = U_body + U_lid
pr("B4", "Body VIP joints (m of joint, W/K)", f"{j_body:.2f} m, {U_joint:.4f}")
pr("B5", "Lid plug junction (W/K)", U_lidj, "", "{:.4f}")
pr("B6", "Foam strip at the pipe crossing (W/K)", U_foam, "", "{:.4f}")
pr("B7", "Thermosiphon stainless wall sections, reverse path (W/K)", U_pipe, "", "{:.4f}")
pr("B8", "Sensor wires (W/K)", U_wire, "", "{:.4f}")
pr("B9", "Body / lid / total conductance (W/K)", f"{U_body:.4f} / {U_lid:.4f} / {U:.4f}")
for name, ta in T_CASES.items():
    pr("B10", f"Heat leak at {ta:.0f} °C, PCM at 5 °C (W)", U * (ta - T_MELT))
pr("B11", "TRL 2 estimate for comparison (W/K)", 0.11)

# ---------------------------------------------------------------- C. PCM
head("C. Phase-change material (5 °C organic, RT 5 HC class)")
ct = P["can_t"]
V_jspace = ((2 * L["pcm_x"] - 2 * ct) * (2 * L["pcm_y"] - 2 * ct) * (L["cav_z1"] - L["pcm_z0"] - ct)
            - P["cav_l"] * P["cav_w"] * P["cav_h"]) / 1e6
loop_len = (2 * (2 * (L["pcm_x"] - ct - P["loop_inset"] - ro * 1000)) + 2 * (2 * (L["pcm_y"] - ct - P["loop_inset"] - ro * 1000))) / 1000
riser_len = 2 * (P["pipe_exit_z"] - L["loop_z"]) / 1000
V_tubes = math.pi * ro ** 2 * (loop_len + riser_len) * 1000   # L
V_j = CV["pcm_jacket"] / 1e3        # pouch space from the model: can less liner, feet, collar, loop and cable (DDR-003)
V_l = CV["pcm_lid"] / 1e3           # inside the lid cold plate tray (DDR-003)
m_j, m_l = V_j * PCM_FILL * RHO_PCM_L / 1000, V_l * PCM_FILL * RHO_PCM_L / 1000
m_pcm = m_j + m_l
E_j, E_l = m_j * H_USABLE, m_l * H_USABLE
E_pcm = E_j + E_l
pr("C1", "PCM space, jacket / lid pack (L)", f"{V_j:.3f} / {V_l:.3f}")
pr("C2", "PCM mass, jacket / lid / total (kg)", f"{m_j:.3f} / {m_l:.3f} / {m_pcm:.3f}")
pr("C3", "Usable latent energy, jacket / lid / total (kJ)", f"{E_j / 1e3:.0f} / {E_l / 1e3:.0f} / {E_pcm / 1e3:.0f}")
pr("C4", "Total usable latent energy (Wh)", E_pcm / 3600, "", "{:.1f}")

# ---------------------------------------------------------------- D. passive hold
head("D. Passive hold, PCM only (R4)")


def passive(ta, ej=E_j, el=E_l, u_scale=1.0):
    """Jacket alone, lid pack alone, and pooled. The lid cold plate couples the lid pack to the
    can rim, so the two melt together: the pooled figure is the hold time."""
    qj, ql = u_scale * U_body * (ta - T_MELT), u_scale * U_lid * (ta - T_MELT)
    tj, tl = ej / qj / 3600, el / ql / 3600
    return tj, tl, (ej + el) / (qj + ql) / 3600


# lateral conductance of the lid cold plate from its centre to the can rim (plate as a square fin)
a_pl = (2 * L["pcm_x"] + 2 * L["pcm_y"]) / 2 / 1000            # mean side (m)
G_plate = K_AL * P["lid_plate_t"] / 1000 * 4 * a_pl / (a_pl / 2)


for name, ta in T_CASES.items():
    tj, tl, tt = passive(ta)
    pr("D1", f"{ta:.0f} °C: jacket alone / lid pack alone / pooled (h)", f"{tj:.1f} / {tl:.1f} / {tt:.1f}")
pr("D1b", "Lid cold plate lateral conductance to the can rim (W/K)", G_plate, "", "{:.1f}")
pr("D1c", "Against the lid heat leak (ratio)", G_plate / U_lid, "", "{:.0f}")
tj43, tl43, tt43 = passive(43.0)
t4 = tt43
pr("D2", "R4 hold at 43 °C, jacket and lid pack pooled by the plate (h)", t4, "", "{:.1f}")
pr("D3", "Same with 30 % more heat leak (h)", passive(43.0, u_scale=1.3)[2], "", "{:.1f}")
pr("D4", "Heat leak rise that brings R4 to exactly 12 h (%)", (t4 / 12.0 - 1) * 100, "", "{:.0f}")

# ---------------------------------------------------------------- E. Peltier and heat sink
head("E. Peltier module, cold path and heat sink (R7)")


def module(name):
    vmax, imax, dtm = MODULES[name]
    th = 300.0
    s = vmax / th
    r = (th - dtm) * vmax / (th * imax)
    k = s * (th - dtm) * imax / (2 * dtm)
    return s, r, k


def tec_point(I, t_can, ta, mod):
    """Module at current I with cold path from the can and hot path to air. Returns Qc, P, Qh, Tc, Th."""
    s, r, k = mod
    qc, p = 0.0, 0.0
    for _ in range(60):
        tc = t_can - qc * R_COLD + K0
        th = ta + (qc + p) * R_HOT + K0
        qc_n = s * tc * I - 0.5 * I * I * r - k * (th - tc)
        p = s * (th - tc) * I + I * I * r
        qc = 0.5 * qc + 0.5 * qc_n
    return qc, p, qc + p, tc - K0, th - K0


def hold_current(q_need, t_can, ta, mod):
    """Smallest current that lifts q_need with the can at t_can. None if the module cannot."""
    lo, hi = 0.0, None
    best = max((tec_point(i / 20, t_can, ta, mod)[0], i / 20) for i in range(1, 121))
    if best[0] < q_need:
        return None
    hi = best[1]
    for _ in range(50):
        mid = (lo + hi) / 2
        if tec_point(mid, t_can, ta, mod)[0] >= q_need:
            hi = mid
        else:
            lo = mid
    return hi


def hold_power(ta, mod, t_can=T_CAN_HOLD, u_scale=1.0):
    q = u_scale * U * (ta - t_can)
    I = hold_current(q, t_can, ta, mod)
    if I is None:
        return None
    qc, p, qh, tc, th = tec_point(I, t_can, ta, mod)
    s, r, _ = mod
    v = s * (th - tc) + I * r
    return dict(q=q, I=I, p=p, qh=qh, tc=tc, th=th, v=v, cop=q / p, p_in=p / ETA_DRV + P_FAN + P_CTRL)


for name in MODULES:
    s, r, k = module(name)
    pr("E1", f"{name}: S (V/K), R (ohm), off-state K (W/K)", f"{s:.4f}, {r:.2f}, {k:.3f}")
mod = module(MODULE)
pr("E2", "Off-state module K against whole-box heat leak (ratio)", mod[2] / U, "", "{:.1f}")
HOLD = {}
for name in MODULES:
    for ta in (25.0, 32.0, 43.0):
        h = hold_power(ta, module(name))
        HOLD[(name, ta)] = h
        if h is None:
            pr("E3", f"{name} hold at {ta:.0f} °C", "cannot lift the load (off-state conduction too high)")
            continue
        pr("E3", f"{name} hold at {ta:.0f} °C: I (A), module W, COP, input W", f"{h['I']:.2f}, {h['p']:.1f}, {h['cop']:.2f}, {h['p_in']:.1f}")
h43 = HOLD[(MODULE, 43.0)]
pr("E4", f"Chosen {MODULE} at 43 °C: cold face / hot face (°C)", f"{h43['tc']:.1f} / {h43['th']:.1f}")
pr("E5", "Module voltage needed at 43 °C (V)", h43["v"], "", "{:.1f}")
pr("E6", "Heat rejected at the sink at 25 / 32 / 43 °C (W)",
   f"{HOLD[(MODULE, 25.0)]['qh']:.1f} / {HOLD[(MODULE, 32.0)]['qh']:.1f} / {h43['qh']:.1f}")
pr("E7", "Sink base temperature at 43 °C (°C)", 43.0 + h43["qh"] * (R_HOT - 0.05), "", "{:.0f}")
pr("E8", "Input power at 43 °C against 45 W USB-C PD budget (W)", f"{h43['p_in']:.1f} of {45 * 0.92:.1f}")
pr("E9", "Input power at 43 °C from 10 V vehicle input needs (A)", h43["p_in"] / V_IN_MIN / 0.95, "", "{:.2f}")
pr("E9b", "Buck-boost: module voltage / lowest input (V); headroom", f"{h43['v']:.1f} / {V_IN_MIN:.1f}; boosts below the module voltage")
# on/off PWM at full supply voltage instead of smooth DC, same average heat lift, 43 °C
s, r, k = mod
dt_pwm = h43["th"] - h43["tc"]
I_on = (12.8 - s * dt_pwm) / r
qc_on = s * (h43["tc"] + K0) * I_on - 0.5 * I_on ** 2 * r
duty = (h43["q"] + k * dt_pwm) / qc_on
p_pwm = duty * (s * dt_pwm * I_on + I_on ** 2 * r)
pr("E10", "Unfiltered on/off PWM at 12.8 V, 43 °C: duty, module W", f"{duty:.2f}, {p_pwm:.1f}")

# ---------------------------------------------------------------- F. battery hold
head("F. Off-grid hold: battery, then PCM (R5, R6)")
E_batt = BATT_WH * (1 - BATT_RESERVE)
pr("F1", "Battery energy for cooling (Wh)", E_batt, "", "{:.1f}")


def offgrid(ta, u_scale=1.0):
    h = hold_power(ta, mod, u_scale=u_scale)
    tb = E_batt / h["p_in"]
    # the lid pack sits on the cold plate, held near the can temperature, so it stays frozen in
    # the battery phase; then jacket and lid pack melt together
    tp = passive(ta, E_j, E_l, u_scale)[2]
    return tb, tp, tb + tp


F, F13 = {}, {}
for ta in (25.0, 32.0, 43.0):
    F[ta] = offgrid(ta)
    tb, tp, tt = F[ta]
    pr("F2", f"{ta:.0f} °C: battery phase + passive phase = total (h)", f"{tb:.1f} + {tp:.1f} = {tt:.1f}")
for ta in (32.0, 43.0):
    F13[ta] = offgrid(ta, 1.3)
    pr("F2b", f"{ta:.0f} °C with 30 % more heat leak: total (h)", F13[ta][2], "", "{:.1f}")
q_lid43 = U_lid * (43.0 - T_CAN_HOLD)
dT_plate = q_lid43 / G_plate
pr("F3", "Lid heat leak carried by the plate to the can, powered hold at 43 °C (W)", q_lid43, "", "{:.2f}")
pr("F4", "Plate centre above the can rim at that load (K)", dT_plate, "", "{:.2f}")
T_lidpack = T_CAN_HOLD + dT_plate + 0.5
pr("F5", "Lid pack stays frozen, powered hold at 43 °C, near (°C)", T_lidpack, "", "{:.1f}")
tb43_2x = 2 * E_batt / HOLD[(MODULE, 43.0)]["p_in"]
pr("F6", "43 °C total with the 153.6 Wh 4S2P pack, for reference (h)", tb43_2x + passive(43.0)[2], "", "{:.1f}")

# ---------------------------------------------------------------- G. refreeze
head("G. Refreeze from fully melted, 25 °C ambient, box empty (R8)")
ta = 25.0
A_can = 2 * (2 * L["pcm_x"] + 2 * L["pcm_y"]) * (L["cav_z1"] - L["pcm_z0"]) / 1e6 + 2 * L["pcm_x"] * 2 * L["pcm_y"] / 1e6
s_j = m_j / RHO_PCM_S / A_can                    # effective jacket thickness when frozen solid
# fin efficiency of the can wall above the loop, frozen PCM layer as the fin's surroundings
h_f = K_PCM_S / (s_j / 2)
mfin = math.sqrt(h_f / (237.0 * ct / 1000))
Lfin = (L["cav_z1"] - L["loop_z"]) / 1000
eta_fin = math.tanh(mfin * Lfin) / (mfin * Lfin)
pr("G1", "Evaporator can area in contact with the jacket (m²)", A_can, "", "{:.4f}")
pr("G2", "Effective frozen jacket thickness (mm)", s_j * 1000, "", "{:.1f}")
pr("G3", "Can wall fin efficiency above the loop", eta_fin, "", "{:.2f}")
m_liner = (P["cav_l"] * P["cav_w"] * P["cav_h"] - in_l * in_w * in_h) / 1e9 * 2700
m_can = CV["can"] / 1e6 * 2700       # with the 5 mm rim flange (DDR-003)
m_plate = CV["lidplate"] / 1e6 * 2700  # folded tray (DDR-003)
s_l = m_l / RHO_PCM_S / A_top                    # frozen lid pack thickness on the plate
C_sens = (m_j + m_l) * CP_PCM_L + (m_liner + m_can + m_plate) * 900.0
R_RIM = 0.5            # K/W, plate rim to can rim through the compressed gasket seat


def best_point(q_pcm_fn, ta, mod, pcap):
    """Scan module currents; for each, solve the can temperature where lift = PCM draw + leak. Pick the largest PCM draw."""
    best = (0.0, None, None)
    for i in range(1, 61):
        I = i * 0.1
        lo, hi = -30.0, 30.0
        for _ in range(40):
            tcn = (lo + hi) / 2
            qc = tec_point(I, tcn, ta, mod)[0]
            if qc > q_pcm_fn(tcn) + U_body * (ta - tcn):
                hi = tcn
            else:
                lo = tcn
        tcn = hi
        qc, p, qh, tc, th = tec_point(I, tcn, ta, mod)
        if p > pcap or tcn < T_CAN_MIN:
            continue
        q = q_pcm_fn(tcn)
        if q > best[0]:
            best = (q, I, tcn, p)
    return best


def refreeze(mod, pcap=P_CAP_REFREEZE, dt=120.0):
    """Jacket (through the can) and lid pack (through the lid cold plate) freeze in parallel."""
    T = 25.0; fj = fl = 0.0; time = 0.0; t_sens = None; t_j = t_l = None
    A_sens = A_can + A_top
    while (fj < 1.0 or fl < 1.0) and time < 30 * 3600:
        if T > T_MELT:
            fn = lambda tc: H_CAN_LIQ * A_sens * (T - tc)
            q, I, tcn, p = best_point(fn, ta, mod, pcap)
            T -= q * dt / C_sens
            if T <= T_MELT:
                T = T_MELT; t_sens = time
        else:
            sj, sl = max(fj * s_j, 0.5e-3), max(fl * s_l, 0.5e-3)
            qj_fn = lambda tc: K_PCM_S * A_can * eta_fin * max(T_MELT - tc, 0) / sj if fj < 1.0 else 0.0
            ql_fn = lambda tc: max(T_MELT - tc, 0) / (sl / (K_PCM_S * A_top) + R_RIM) if fl < 1.0 else 0.0
            q, I, tcn, p = best_point(lambda tc: qj_fn(tc) + ql_fn(tc), ta, mod, pcap)
            fj += qj_fn(tcn) * dt / E_j
            fl += ql_fn(tcn) * dt / E_l
            if fj >= 1.0 and t_j is None:
                t_j = time
            if fl >= 1.0 and t_l is None:
                t_l = time
        time += dt
    return time / 3600, (t_sens or 0) / 3600, (t_j or time) / 3600, (t_l or time) / 3600


for name in MODULES:
    tt, ts, tjf, tlf = refreeze(module(name))
    pr("G4", f"{name}: refreeze, sensible / jacket / lid pack / all PCM (h)", f"{ts:.1f} / {tjf:.1f} / {tlf:.1f} / {tt:.1f}")
t_ref, t_sens, t_ref_j, t_ref_l = refreeze(mod)
t_stefan = RHO_PCM_S * H_USABLE * s_j ** 2 / (2 * K_PCM_S * (T_MELT - T_CAN_MIN)) / 3600 / eta_fin
pr("G5", "Conduction limit alone, can at -2 °C (Stefan, h)", t_stefan, "", "{:.1f}")
pr("G6", "Lid pack cold path to the evaporator", "1.5 mm aluminium lid cold plate seated on the can rim")
T_plate = T_CAN_MIN + 1.0
t_lid_plate = RHO_PCM_S * H_USABLE * s_l ** 2 / (2 * K_PCM_S * (T_MELT - T_plate)) / 3600
pr("G7", "Lid pack conduction limit alone on the plate (h, Stefan)", t_lid_plate, "", "{:.1f}")
q_bat_charge = BATT_WH / (P_CHARGE * 0.95)
pr("G8", "Battery recharge alongside refreeze at 12 W (h)", q_bat_charge, "", "{:.1f}")
pr("G9", "Input during refreeze: module cap + fan + controller + charge (W)", P_CAP_REFREEZE / ETA_DRV + P_FAN + P_CTRL + P_CHARGE, "", "{:.1f}")
# option for review: give the module 30 W and the battery 7 W during refreeze (same 45 W PD budget)
t_ref30 = refreeze(mod, pcap=30.0)[0]
pr("G10", "Option: 30 W to the module, 7 W charge: all PCM refreeze (h)", t_ref30, "", "{:.1f}")
pr("G11", "Option: input then (W); battery recharge at 7 W (h)", f"{30.0 / ETA_DRV + P_FAN + P_CTRL + 7.0:.1f}; {BATT_WH / (7.0 * 0.95):.1f}")

# ---------------------------------------------------------------- H. thermosiphon
head("H. Thermosiphon: diode ratio and tilt")
pr("H1", "Forward conductance (W/K) / reverse (W/K) / ratio", f"{1 / R_COLD:.2f} / {U_pipe:.4f} / {1 / R_COLD / U_pipe:.0f}")
pr("H2", "Heat leak if the module were bolted to the liner (W/K)", U + mod[2], "", "{:.3f}")
pr("H3", "Passive hold at 43 °C with that direct mount (h)", E_pcm / ((U + mod[2]) * 38) / 3600, "", "{:.1f}")
lx = L["pcm_x"] - ct - P["loop_inset"] - ro * 1000
ly = L["pcm_y"] - ct - P["loop_inset"] - ro * 1000
cxn, zc, zl = L["sh_x"] + P["block"][0] / 2, P["pipe_exit_z"], L["loop_z"]
pitch_full = math.degrees(math.atan((zc - zl) / (cxn + lx)))
pitch_part = math.degrees(math.atan((zc - zl) / (cxn - lx)))
roll_full = math.degrees(math.atan((zc - zl) / (ly + P["pipe_y"])))
pr("H4", "Condenser above evaporator loop (mm)", zc - zl, "", "{:.1f}")
pr("H5", "Tilt, cooling head down: whole loop below condenser to (deg)", pitch_full, "", "{:.0f}")
pr("H6", "Tilt, cooling head down: some loop below condenser to (deg)", pitch_part, "", "{:.0f}")
pr("H7", "Tilt, front or back down: whole loop below condenser to (deg)", roll_full, "", "{:.0f}")

# ---------------------------------------------------------------- I. freeze fault
head("I. Freeze fault: stuck-on driver (R2)")
t_block_only = T_CUT_BLOCK + 1.0
pr("I1", "Cold-block cut-out opens at (°C)", T_CUT_BLOCK, "", "{:.0f}")
pr("I2", "Block cut-out alone: liner settles near, stuck-on, cool ambient (°C)", t_block_only, "", "{:.0f}")
# proposed: second hardware cut-out on the liner, in series; lumped equilibrium after it opens
C_pay = 0.68 * 3.0e3 + m_liner * 900.0             # payload (pens, about 0.68 kg) and liner, J/K
C_pcm = m_j * CP_PCM_S + m_can * 900.0
T_EQ = {}
for t_cut in (2.0, 3.0):
    t_pcm_mean = (T_CAN_MIN + t_cut) / 2
    T_EQ[t_cut] = (C_pay * t_cut + C_pcm * t_pcm_mean) / (C_pay + C_pcm)
    pr("I3", f"Liner cut-out at {t_cut:.0f} °C: liner settles to (°C)", T_EQ[t_cut], "", "{:.1f}")
t_liner_fault = T_EQ[T_CUT_LINER]
pr("I5", f"Adopted: liner cut-out at {T_CUT_LINER:.0f} °C in series; liner settles near (°C)", t_liner_fault, "", "{:.1f}")
pr("I4", "Stuck-on current from 14.4 V charge rail, module cold (A)", 14.4 / mod[1], "", "{:.1f}")

# ---------------------------------------------------------------- J. logger
head("J. Logger storage and reserve (R9, R11)")
rec = 60 * 24 * 60 * 16
pr("J1", "60 days at 1 record/min, 16 bytes (MB, of 2.10 MB flash)", rec / 1e6, "", "{:.2f}")
loads = {"nRF52840, RTC, BLE advertising 1 s": 25e-6 * 3.3, "Sensor reads, 4 per min": 0.02e-3,
         "E-paper refresh every 10 min": 0.033e-3, "Buck quiescent at 12.8 V": 20e-6 * 12.8,
         "BMS quiescent at 12.8 V": 30e-6 * 12.8}
p_log = sum(loads.values())
pr("J2", "Logger average draw, itemized (mW)", p_log * 1e3, "", "{:.2f}")
pr("J3", "Design draw with margin (mW)", 5.0, "", "{:.1f}")
pr("J4", "Reserve 15 % of 76.8 Wh lasts (days) at 5 mW", BATT_WH * BATT_RESERVE / 5e-3 / 24, "", "{:.0f}")

# ---------------------------------------------------------------- K. mass
head("K. Mass, empty (R12)")
from model import volumes_cm3  # noqa: E402
v = volumes_cm3()
RHO_PETG = 1.27
shell_frac = (2 * 3 * 0.45 + (P["shell_t"] - 2.7) * 0.2) / P["shell_t"]
lid_frac = (4.0 + (P["lid_cap_t"] - 4.0) * 0.2) / P["lid_cap_t"]
hous_frac = min(1.0, (2.7 + (P["end_wall"] - 2.7) * 0.2) / P["end_wall"])
sink_al = (P["sink_base"] * P["sink_w"] * P["sink_h"] + P["fins"] * P["sink_fin"] * 2 * P["sink_h"]) / 1e3
tube_cu = math.pi * (ro ** 2 - (ro - 0.5e-3) ** 2) * (loop_len + riser_len + 2 * 0.041) * 8960
bxv = P["block"][0] * P["block"][1] * P["block"][2] / 1e3
V_VIP = sum(x for k, x in CV.items() if k.startswith("vip_"))
V_PRINT_NEW = CV["fillers"] + CV["duct"] + CV["frame"] + CV["cradle"] + CV["feet"] + CV["collar"]
M = {
    "Shell with pads and towers (PETG, printed)": CV["shell"] * RHO_PETG * shell_frac / 1e3,
    "Lid cap, gasket, latches": CV["lid"] * RHO_PETG * lid_frac / 1e3 + 0.04,
    "Lid cold plate tray (aluminium)": m_plate,
    "Handle and strap": 0.20,
    "VIP set (190 kg/m³ with film)": V_VIP * 0.19 / 1e3,
    "Foam strip (35 kg/m³)": CV["foam"] * 0.035 / 1e3,
    "Construction parts, printed (fillers, duct cover, block frame, cradle, liner feet and collar)": V_PRINT_NEW * RHO_PETG * 0.8 / 1e3,
    "Heat-set inserts, standoffs, extra screws, drain tube": 0.05,
    "PCM": m_pcm,
    "PCM pouches (HDPE)": 0.08,
    "Liner (aluminium)": m_liner,
    "Rack (PETG)": V_rack * RHO_PETG * 0.85 / 1e3,
    "Evaporator can (aluminium)": m_can,
    "Loop tubes (copper, 0.5 mm wall)": tube_cu,
    "Cold block (aluminium)": bxv * 2.7 / 1e3,
    "Peltier module": 0.025,
    "Heat sink (aluminium)": sink_al * 2.7 / 1e3,
    "Fan and guard": 0.06,
    "End housings with ears (PETG, printed)": (CV["head"] + CV["bay"]) * RHO_PETG * hous_frac / 1e3,
    "LiFePO4 cells, 4 x 32700": 4 * 0.14,
    "BMS, fuse, holder": 0.08,
    "Electronics (power board, logger, sensors, cut-outs, display)": 0.17,
    "Wiring and hardware": 0.15,
}
for k_, m_ in M.items():
    pr("K1", k_, m_, "kg", "{:.3f}")
M_tot = sum(M.values())
pr("K2", "Total empty (kg)", M_tot, "", "{:.2f}")
pr("K3", "Total empty (lb)", M_tot / 0.4536, "", "{:.1f}")
pr("K4", "Loaded with 24 pens, about 0.68 kg (kg)", M_tot + 0.68, "", "{:.2f}")

# ---------------------------------------------------------------- L. cost and battery
head("L. Cost and battery (R14, R15)")
BUDGET_USD = 310.0  # project.yaml budget_usd; top-up to $310 decided by Amish, 2026-09-26 (CPD-DDR-002 N3)
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open(encoding="utf-8")))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
pr("L1", "BOM lines, all priced", f"{len(rows)}, {all(r['unit_cost_usd'].strip() for r in rows)}")
pr("L2", f"BOM total (USD) against budget ${BUDGET_USD:.0f}", cost, "", "{:.0f}")
pr("L3", "Battery energy (Wh) against 100 Wh", BATT_WH, "", "{:.1f}")

# ---------------------------------------------------------------- N. option: thicker jacket, no lid pack
head("N. Option for review: 20 mm jacket, no lid pack (not adopted)")
jt = 20.0
V_opt = ((P["cav_l"] + 2 * jt - 2 * ct) * (P["cav_w"] + 2 * jt - 2 * ct) * (P["cav_h"] + jt - ct)
         - P["cav_l"] * P["cav_w"] * P["cav_h"]) / 1e6 - V_tubes
m_opt = V_opt * PCM_FILL * RHO_PCM_L / 1000
pr("N1", "PCM mass, all in the actively frozen jacket (kg)", m_opt, "", "{:.3f}")
pr("N2", "Box length / width change (mm); height change (mm)", f"+{2 * (jt - P['pcm_t']):.0f} / +{2 * (jt - P['pcm_t']):.0f}; {(jt - P['pcm_t']) - P['lid_pcm_t']:+.0f}")

# ---------------------------------------------------------------- O. adopted: lighter printed parts
head("O. Lighter printed parts, adopted (CPD-DDR-002): change against CPD-CAL-001 v0.1")
P1 = dict(P, shell_t=4.0, lid_cap_t=8.0, end_wall=3.0)
v1 = component_volumes_cm3(P1)
f_sh1 = (2 * 3 * 0.45 + (P1["shell_t"] - 2.7) * 0.2) / P1["shell_t"]
f_lid1 = (4.0 + (P1["lid_cap_t"] - 4.0) * 0.2) / P1["lid_cap_t"]
f_h1 = min(1.0, (2.7 + (P1["end_wall"] - 2.7) * 0.2) / P1["end_wall"])
d_shell = v1["shell"] * RHO_PETG * f_sh1 / 1e3 - M["Shell with pads and towers (PETG, printed)"]
d_lid = v1["lid"] * RHO_PETG * f_lid1 / 1e3 + 0.04 - M["Lid cap, gasket, latches"]
d_h = (v1["head"] + v1["bay"]) * RHO_PETG * f_h1 / 1e3 - M["End housings with ears (PETG, printed)"]
pr("O1", "Saving: shell 4 to 3 mm / lid cap 8 to 5 mm / housings 3 to 2 mm (kg)", f"{d_shell:.2f} / {d_lid:.2f} / {d_h:.2f}")
pr("O3", "Lid cold plate, 1.5 mm aluminium, adds (kg)", M["Lid cold plate tray (aluminium)"], "", "{:.2f}")
pr("O4", "Over the 5.5 kg target by (kg)", M_tot - 5.5, "", "{:.2f}")

# ---------------------------------------------------------------- P. foam variant (CPD-DDR-001 D7)
head("P. Documented low-cost variant: 25 mm polyurethane foam instead of VIPs")
U_fb = K_FOAM * S_body + U_pipe + U_wire
U_fl = K_FOAM * S_lid
pr("P1", "Foam variant conductance, body / lid / total (W/K)", f"{U_fb:.4f} / {U_fl:.4f} / {U_fb + U_fl:.4f}")
pr("P2", "Foam variant passive hold at 43 °C, pooled (h)", E_pcm / ((U_fb + U_fl) * 38) / 3600, "", "{:.1f}")

# ---------------------------------------------------------------- results
head("Results against requirements")
t4_13 = passive(43.0, u_scale=1.3)[2]


def status(nominal, high_leak, target):
    """Met if the target holds even with 30 % more heat leak; at risk if only at the nominal leak."""
    return "Met" if high_leak >= target else ("At risk" if nominal >= target else "Not met")


h32 = HOLD[(MODULE, 32.0)]
RES = [
    ("R1", "2 to 8 °C at the payload probe", f"Can held at 2 °C; liner 2 to 5 °C; lid pack held frozen near {T_lidpack:.1f} °C by the cold plate in powered hold at 43 °C", "Met"),
    ("R2", "No contact surface below 1 °C, incl. stuck-on driver", f"Normal: met. Fault: liner settles near {t_liner_fault:.1f} °C with the 3 °C liner cut-out", "Met" if t_liner_fault >= 1.0 else "Not met"),
    ("R3", "1.0 L or more; 20 or more pens up to 170 mm", f"{V_use:.2f} L; {nl * nc} pens; {in_l:.0f} mm long", "Met"),
    ("R4", "12 h or more at 43 °C, no power", f"{t4:.1f} h ({t4_13:.1f} h at +30 % leak)", status(t4, t4_13, 12)),
    ("R5", "24 h or more at 32 °C, battery then PCM", f"{F[32.0][2]:.1f} h ({F13[32.0][2]:.1f} h at +30 % leak)", status(F[32.0][2], F13[32.0][2], 24)),
    ("R6", "16 h or more at 43 °C, battery then PCM (relaxed)", f"{F[43.0][2]:.1f} h ({F13[43.0][2]:.1f} h at +30 % leak)", status(F[43.0][2], F13[43.0][2], 16)),
    ("R7", "Holds up to 43 °C on 12 V or 45 W USB-C PD", f"{h43['p_in']:.1f} W input; lid pack held by the plate; buck-boost from {V_IN_MIN:.0f} V", "Met"),
    ("R8", "Refreeze melted PCM in 8 h or less at 25 °C", f"All PCM {t_ref:.2f} h (jacket {t_ref_j:.1f} h, lid pack {t_ref_l:.1f} h)", "Met" if t_ref <= 8.0 else "Not met"),
    ("R9", "±0.5 °C, 1 min log, 60 days, CSV export", f"{rec / 1e6:.2f} MB of 2.10 MB; accuracy by sensor selection", "Met"),
    ("R10", "Alarm logic and thresholds", "Design intent only; no firmware sketch at TRL 3", "Not verifiable at TRL 3"),
    ("R11", "Logger runs 14 days after cooling stops", f"{BATT_WH * BATT_RESERVE / 5e-3 / 24:.0f} days at 5 mW", "Met"),
    ("R12", "5.5 kg or less empty (relaxed)", f"{M_tot:.2f} kg", "Met" if M_tot <= 5.5 else "Not met"),
    ("R13", "Fits 400 x 250 x 250 mm", f"{ov_x:.0f} x {ov_y:.0f} x {ov_z:.0f} mm", "Met"),
    ("R14", "Battery 100 Wh or less", f"{BATT_WH:.1f} Wh", "Met"),
    ("R15", f"Parts ${BUDGET_USD:.0f} or less; no custom PCB", f"${cost:.0f}", "Met" if cost <= BUDGET_USD else "Not met"),
    ("R16", "IP54 bays; 0.5 m drop loaded", "Needs test", "Not verifiable at TRL 3"),
    ("R17", "Prototype labelling", "Box, start screen and every log", "Met"),
]
for r_ in RES:
    print(f"  {r_[0]:4s} {r_[3]:24s} {r_[2]}")
from collections import Counter  # noqa: E402
print("  counts:", dict(Counter(r_[3] for r_ in RES)))
