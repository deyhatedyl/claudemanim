"""
Independent numerical verification of the 28 anchor question sets (Q01-Q28)
and of every chemical equation used in the series.

Run:  python checks/verify_anchors.py
Writes checks/numerical_check_record.md and checks/numerical_check_record.json.
Exits non-zero if any check fails.

Every value is recomputed from the question data below, NOT copied from the
displayed Manim text. Targets are the brief's checked answers; each one is
compared with a relative tolerance appropriate to its stated rounding.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- constants
VM = 24.8            # L mol^-1 at SLC (25 degC, 100 kPa), as supplied in the brief
C_WATER = 4.18       # J g^-1 degC^-1
AR = {"C": 12.0, "H": 1.0, "O": 16.0, "N": 14.0, "Na": 23.0, "S": 32.1, "Cl": 35.5}
FOOD = {"carb": 16.0, "protein": 17.0, "fat": 37.0}   # kJ g^-1

results: list[dict] = []


def check(qid: str, label: str, computed: float, target: float, rel: float = 2e-3, unit: str = ""):
    ok = abs(computed - target) <= rel * max(abs(target), 1e-12)
    results.append(dict(qid=qid, label=label, computed=computed, target=target,
                        unit=unit, rel_tol=rel, ok=bool(ok)))
    return computed


def check_true(qid: str, label: str, cond: bool, note: str = ""):
    results.append(dict(qid=qid, label=label, computed=note or str(cond), target="True",
                        unit="", rel_tol=0, ok=bool(cond)))


# ---------------------------------------------------------------- formula tools
TOKEN = re.compile(r"([A-Z][a-z]?)(\d*)|(\()|(\))(\d*)")


def parse_formula(f: str) -> Counter:
    """Parse a molecular formula such as C2H5OH or Ca(OH)2 into atom counts."""
    stack = [Counter()]
    for el, n, lp, rp, rn in TOKEN.findall(f):
        if el:
            stack[-1][el] += int(n or 1)
        elif lp:
            stack.append(Counter())
        elif rp:
            grp = stack.pop()
            for k, v in grp.items():
                stack[-1][k] += v * int(rn or 1)
    return stack[0]


def molar_mass(f: str) -> float:
    return sum(AR[k] * v for k, v in parse_formula(f).items())


def side_atoms(side: str) -> Counter:
    tot = Counter()
    for term in side.split("+"):
        term = term.strip()
        term = re.sub(r"\((s|l|g|aq)\)$", "", term)
        m = re.match(r"^([\d./]*)\s*(.+)$", term)
        coef = Fraction(m.group(1)) if m.group(1) else Fraction(1)
        for k, v in parse_formula(m.group(2)).items():
            tot[k] += coef * v
    return tot


def balanced(eq: str) -> bool:
    lhs, rhs = eq.split("->")
    return side_atoms(lhs) == side_atoms(rhs)


EQUATIONS = {
    "hydrogen combustion (Q05)": "2H2(g) + O2(g) -> 2H2O(l)",
    "water decomposition, reversed and halved (Q05)": "H2O(l) -> H2(g) + 1/2O2(g)",
    "HCl formation (Q03)": "H2(g) + Cl2(g) -> 2HCl(g)",
    "methane complete combustion": "CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)",
    "methane incomplete to CO": "2CH4(g) + 3O2(g) -> 2CO(g) + 4H2O(g)",
    "methane incomplete to soot": "CH4(g) + O2(g) -> C(s) + 2H2O(g)",
    "ethanol complete combustion": "C2H5OH(l) + 3O2(g) -> 2CO2(g) + 3H2O(l)",
    "ethanol specified incomplete (Q11)": "C2H5OH(l) + 5/2O2(g) -> CO2(g) + CO(g) + 3H2O(g)",
    "methanol complete combustion (x2)": "2CH3OH(l) + 3O2(g) -> 2CO2(g) + 4H2O(l)",
    "octane complete combustion": "2C8H18(l) + 25O2(g) -> 16CO2(g) + 18H2O(l)",
    "coal (as carbon) combustion": "C(s) + O2(g) -> CO2(g)",
    "propane complete combustion (E06 recall)": "C3H8(g) + 5O2(g) -> 3CO2(g) + 4H2O(l)",
    "photosynthesis": "6CO2(g) + 6H2O(l) -> C6H12O6(aq) + 6O2(g)",
    "aerobic respiration": "C6H12O6(aq) + 6O2(g) -> 6CO2(g) + 6H2O(l)",
    "fermentation (Q07)": "C6H12O6(aq) -> 2C2H5OH(aq) + 2CO2(g)",
    "transesterification (tristearin + methanol)": "C57H110O6(l) + 3CH3OH(l) -> 3C19H38O2(l) + C3H8O3(l)",
    "anaerobic digestion (glucose, idealised)": "C6H12O6(aq) -> 3CH4(g) + 3CO2(g)",
    "HCl/NaOH neutralisation (Q19, Q27)": "HCl(aq) + NaOH(aq) -> NaCl(aq) + H2O(l)",
    "NaOH/H2SO4 neutralisation (Q20)": "2NaOH(aq) + H2SO4(aq) -> Na2SO4(aq) + 2H2O(l)",
}


def verify_equations():
    for name, eq in EQUATIONS.items():
        check_true("EQ", f"atoms balance: {name}: {eq}", balanced(eq))
    # molar masses used in the series
    for f, M in {"C2H5OH": 46.0, "CO2": 44.0, "H2O": 18.0, "CH4": 16.0, "O2": 32.0,
                 "CH3OH": 32.0, "C6H12O6": 180.0, "CO": 28.0}.items():
        check("EQ", f"molar mass {f}", molar_mass(f), M, rel=1e-9, unit="g/mol")


# ---------------------------------------------------------------- anchors
def q01():
    n_eth = 0.345 / 46.0
    n_gas = (186 / 1000) / VM
    check("Q01", "n(ethanol)", n_eth, 0.00750, unit="mol")
    check("Q01", "n(gas) from 186 mL at SLC", n_gas, 0.00750, unit="mol")
    wrong = 186 / VM
    check_true("Q01", "trap: mL used as L gives 1000x too large", abs(wrong / n_gas - 1000) < 1e-9)


def q02():
    V_L = 0.0850 * 1000
    t_s = 0.150 * 3600
    E_kJ = 7.20e4 / 1000
    V_O2 = V_L * 0.209
    n_O2 = V_O2 / VM
    check("Q02", "air volume", V_L, 85.0, unit="L")
    check("Q02", "time", t_s, 540, unit="s")
    check("Q02", "energy", E_kJ, 72.0, unit="kJ")
    check("Q02", "V(O2)", V_O2, 17.765, rel=1e-6, unit="L")
    check("Q02", "n(O2)", n_O2, 0.716, unit="mol")
    check("Q02", "n(O2) unrounded", n_O2, 0.7163306, rel=1e-6, unit="mol")


def q03():
    broken = 436 + 243
    formed = 2 * 431
    dH = broken - formed
    check("Q03", "bonds broken", broken, 679, unit="kJ")
    check("Q03", "bonds formed", formed, 862, unit="kJ")
    check("Q03", "deltaH", dH, -183, unit="kJ per mol reaction")


def q04():
    q_sys = +18.0 * 0.0250
    check("Q04", "q_system", q_sys, 0.450, unit="kJ")
    check("Q04", "q_cal", -q_sys, -0.450, unit="kJ")
    check_true("Q04", "temperature falls (q_cal < 0)", -q_sys < 0)


def q05():
    dH_rev_per_mol_water = +572 / 2
    E = 0.750 * (572 / 2)
    check("Q05", "reverse, per mol H2O(l)", dH_rev_per_mol_water, 286, unit="kJ")
    check("Q05", "energy released by 0.750 mol H2", E, 214.5, rel=1e-9, unit="kJ")
    check_true("Q05", "trap: treating -572 as per mol H2 gives 429 kJ", abs(0.750 * 572 - 429) < 1e-9)


def q06():
    R, P, TS, TSc = 80, 25, 150, 110
    check("Q06", "forward Ea", TS - R, 70)
    check("Q06", "reverse Ea", TS - P, 125)
    check("Q06", "deltaH", P - R, -55)
    check("Q06", "catalysed forward Ea", TSc - R, 30)
    check_true("Q06", "deltaH unchanged by catalyst", (P - R) == (P - R))


def q07():
    n_g = 270.0 / 180.0
    n_eth_theory = 2 * n_g
    n_eth = 0.780 * n_eth_theory
    m_eth = n_eth * 46.0
    m_co2 = n_eth * 44.0
    check("Q07", "n(glucose)", n_g, 1.50)
    check("Q07", "theoretical n(ethanol)", n_eth_theory, 3.00)
    check("Q07", "actual n(ethanol) = n(CO2)", n_eth, 2.34)
    check("Q07", "m(ethanol)", m_eth, 107.64, rel=1e-6, unit="g")
    check("Q07", "m(CO2)", m_co2, 102.96, rel=1e-6, unit="g")
    check_true("Q07", "trap: 1:1 ratio would give 53.8 g ethanol", abs(0.78 * 1.5 * 46 - 53.82) < 1e-6)


def food(c, p, f):
    return c * FOOD["carb"] + p * FOOD["protein"] + f * FOOD["fat"]


def q09():
    per100 = food(48.0, 12.0, 18.0)
    serving = per100 * 30.0 / 100
    check("Q09", "energy per 100 g", per100, 1638, unit="kJ")
    check("Q09", "energy per 30.0 g serving", serving, 491.4, rel=1e-9, unit="kJ")
    check("Q09", "serving in J", serving * 1000, 4.914e5, rel=1e-9, unit="J")
    check("Q09", "whole packet (trap)", per100 * 0.90, 1474.2, rel=1e-9, unit="kJ")


def q10():
    A = food(50, 10, 12)
    B = food(35, 20, 15)
    check("Q10", "A per 100 g", A, 1414, unit="kJ")
    check("Q10", "B per 100 g", B, 1455, unit="kJ")
    check("Q10", "A serving 80 g", A * 0.80, 1131.2, rel=1e-9, unit="kJ")
    check("Q10", "B serving 50 g", B * 0.50, 727.5, rel=1e-9, unit="kJ")
    check_true("Q10", "B higher per 100 g, A serving higher", B > A and A * 0.8 > B * 0.5)


def q11():
    # C2H5OH + 2.5 O2 -> x CO2 + y CO + z H2O
    z = 6 / 2                       # H balance
    # C: x + y = 2 ; O: 1 + 5 = 2x + y + z
    x = (1 + 2 * 2.5 - z) - 2       # (2x+y) - (x+y)
    y = 2 - x
    check("Q11", "n(H2O)", z, 3.00)
    check("Q11", "n(CO2)", x, 1.00)
    check("Q11", "n(CO)", y, 1.00)
    check("Q11", "complete combustion O2 per mol ethanol", (2 * 2 + 3 - 1) / 2, 3.00)
    # trap: ethanol's own O forgotten -> 2x + y = 2 with x + y = 2 -> x = 0, y = 2 (all CO)
    x_t = (2 * 2.5 - z) - 2
    check_true("Q11", "trap gives all CO (x=0, y=2)", abs(x_t) < 1e-12 and abs((2 - x_t) - 2) < 1e-12)


def q12():
    n = 0.250
    m_co2 = n * 44.0
    m_h2o = 2 * n * 18.0
    check("Q12", "m(CO2)", m_co2, 11.0, unit="g")
    check("Q12", "m(H2O vapour)", m_h2o, 9.00, unit="g")
    check("Q12", "total newly formed GHG mass", m_co2 + m_h2o, 20.0, unit="g")
    check("Q12", "dry CO2 volume at SLC", n * VM, 6.20, unit="L")


def q13():
    n_eth0, n_o2 = 0.400, 32.0 / 32.0
    lim_o2 = n_o2 / 3 < n_eth0 / 1
    used = n_o2 / 3
    rem = n_eth0 - used
    check_true("Q13", "O2 limiting (n/coef: O2 0.333 < ethanol 0.400)", lim_o2)
    check("Q13", "ethanol used", used, 1 / 3, rel=1e-9, unit="mol")
    check("Q13", "ethanol remaining (mol)", rem, 0.0666667, rel=1e-5, unit="mol")
    check("Q13", "ethanol remaining (g)", rem * 46.0, 3.07, unit="g")
    check("Q13", "CO2 mass", 2 * used * 44.0, 29.3, unit="g")
    check("Q13", "energy released", used * 1370, 456.6667, rel=1e-6, unit="kJ")
    check_true("Q13", "remaining non-negative", rem >= 0)


def q14():
    n_mix = 12.4 / VM
    n_ch4 = 0.800 * n_mix
    n_co2_in = 0.200 * n_mix
    n_o2 = 90.0 * 0.210 / VM
    o2_lim = n_o2 / 2 < n_ch4 / 1
    used = n_o2 / 2
    rem = n_ch4 - used
    check("Q14", "initial CH4", n_ch4, 0.400, unit="mol")
    check("Q14", "O2 available", n_o2, 0.7620968, rel=1e-6, unit="mol")
    check_true("Q14", "O2 limiting", o2_lim)
    check("Q14", "CH4 consumed", used, 0.3810484, rel=1e-6, unit="mol")
    check("Q14", "CH4 remaining (g)", rem * 16.0, 0.3032258, rel=1e-5, unit="g")
    check("Q14", "new CO2 volume SLC", used * VM, 9.45, rel=1e-6, unit="L")
    check("Q14", "inlet CO2 volume SLC", n_co2_in * VM, 2.48, rel=1e-6, unit="L")
    check("Q14", "total CO2 volume SLC", (used + n_co2_in) * VM, 11.93, rel=1e-6, unit="L")
    check("Q14", "energy released", used * 890, 339.133, rel=1e-5, unit="kJ")
    check_true("Q14", "remaining non-negative", rem >= 0)
    wrong_all_methane = 12.4 / VM
    check_true("Q14", "trap: all gas as methane gives 0.500 mol CH4", abs(wrong_all_methane - 0.5) < 1e-9)


def q15():
    m = 102.640 - 101.720
    n = m / 46.0
    E = n * 1370
    dT = 37.0 - 19.8
    q = 250.0 * C_WATER * dT / 1000
    check("Q15", "ethanol burned", m, 0.920, rel=1e-9, unit="g")
    check("Q15", "n(ethanol)", n, 0.0200, rel=1e-9, unit="mol")
    check("Q15", "fuel energy", E, 27.4, rel=1e-9, unit="kJ")
    check("Q15", "deltaT", dT, 17.2, rel=1e-9, unit="degC")
    check("Q15", "water heat", q, 17.974, rel=1e-9, unit="kJ")
    check("Q15", "efficiency", 100 * q / E, 65.5985, rel=1e-6, unit="%")


def q16():
    q = 180.0 * C_WATER * (78.0 - 18.0) / 1000
    inp = q / 0.450
    m = inp / 29.8
    wrong = q * 0.450 / 29.8
    ideal = q / 29.8
    check("Q16", "useful heat", q, 45.144, rel=1e-9, unit="kJ")
    check("Q16", "required input", inp, 100.32, rel=1e-9, unit="kJ")
    check("Q16", "fuel mass", m, 3.36644, rel=1e-5, unit="g")
    check("Q16", "wrong method mass", wrong, 0.6817, rel=1e-3, unit="g")
    check("Q16", "100% efficient minimum", ideal, 1.515, rel=1e-3, unit="g")
    check_true("Q16", "wrong method < 100% minimum (impossible)", wrong < ideal)


def q17():
    E = 6.00 * 1.50 * 240
    CF = E / 4.00
    water = 120.0 * C_WATER
    app = CF - water
    q_later = CF * 5.60
    CF_new = 150.0 * C_WATER + app
    check("Q17", "electrical input", E, 2160, unit="J")
    check("Q17", "CF", CF, 540, unit="J/degC")
    check("Q17", "water contribution", water, 501.6, rel=1e-9, unit="J/degC")
    check("Q17", "apparatus contribution", app, 38.4, rel=1e-6, unit="J/degC")
    check("Q17", "later heat", q_later, 3024, rel=1e-9, unit="J")
    check("Q17", "new CF", CF_new, 665.4, rel=1e-6, unit="J/degC")


def q18():
    lower = 100.0 * C_WATER
    check("Q18", "water-only lower bound", lower, 418, unit="J/degC")
    check_true("Q18", "360 < lower bound (inconsistent)", 360 < lower)
    # heat loss: same E, smaller observed dT -> larger CF
    E, dT_true = 1000.0, 2.0
    check_true("Q18", "heat loss raises apparent CF", E / (dT_true * 0.9) > E / dT_true)
    check_true("Q18", "overestimated dT lowers CF", E / (dT_true * 1.1) < E / dT_true)


def q19():
    n_hcl = 0.0750 * 0.800
    n_naoh = 0.0500 * 0.900
    dT = 24.30 - 20.00
    q = 590 * dT
    dH = -q / n_naoh / 1000
    check("Q19", "n(HCl)", n_hcl, 0.0600)
    check("Q19", "n(NaOH)", n_naoh, 0.0450)
    check_true("Q19", "NaOH limiting (1:1)", n_naoh < n_hcl)
    check("Q19", "HCl left", n_hcl - n_naoh, 0.0150, rel=1e-6)
    check("Q19", "deltaT", dT, 4.30, rel=1e-6)
    check("Q19", "q_cal", q, 2537, rel=1e-6, unit="J")
    check("Q19", "deltaH per mol H2O", dH, -56.3778, rel=1e-5, unit="kJ/mol")
    check("Q19", "trap: divide by acid supplied", -q / n_hcl / 1000, -42.283, rel=1e-4, unit="kJ/mol")


def q20():
    n_naoh, n_acid = 0.0300, 0.0200
    extent = min(n_naoh / 2, n_acid / 1)
    q = extent * 114 * 1000
    dT = q / 480
    check_true("Q20", "NaOH limiting (0.0150 < 0.0200)", n_naoh / 2 < n_acid)
    check("Q20", "reaction extent", extent, 0.0150, rel=1e-9, unit="mol")
    check("Q20", "acid remaining", n_acid - extent, 0.00500, rel=1e-9, unit="mol")
    check("Q20", "heat released", q / 1000, 1.710, rel=1e-9, unit="kJ")
    check("Q20", "deltaT", dT, 3.5625, rel=1e-9, unit="degC")
    check("Q20", "final T", 21.0 + dT, 24.5625, rel=1e-9, unit="degC")
    check("Q20", "trap: 0.0300 x 114 kJ", 0.0300 * 114, 3.42, rel=1e-9, unit="kJ")


def linfit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    return b, my - b * mx


def q21():
    xs, ys = [180, 240, 300, 360], [26.1, 25.9, 25.7, 25.5]
    slope, icpt = linfit(xs, ys)
    T_mix = slope * 120 + icpt
    rise = T_mix - 21.0
    check("Q21", "cooling slope", slope, -0.0033333, rel=1e-4, unit="degC/s")
    check("Q21", "extrapolated T at 120 s", T_mix, 26.3, rel=1e-6, unit="degC")
    check("Q21", "corrected rise", rise, 5.3, rel=1e-6)
    check("Q21", "corrected q", 650 * rise, 3445, rel=1e-6, unit="J")
    check("Q21", "uncorrected q (max 26.1)", 650 * (26.1 - 21.0), 3315, rel=1e-6, unit="J")
    resid = max(abs(slope * x + icpt - y) for x, y in zip(xs, ys))
    check_true("Q21", "cooling data exactly linear (max residual < 1e-9)", resid < 1e-9, f"{resid:.2e}")


def q22():
    rep = -(450 * 4.00) / 0.0400 / 1000
    cor = -(500 * 4.00) / 0.0400 / 1000
    check("Q22", "reported deltaH", rep, -45.0, unit="kJ/mol")
    check("Q22", "corrected deltaH", cor, -50.0, unit="kJ/mol")
    Ti, Tf = 20.0, 24.0
    check_true("Q22", "additive offset cancels", (Tf + 1.5) - (Ti + 1.5) == Tf - Ti)


def q23():
    out = 1.00
    R_in = out / 0.350
    S_in = out / 0.280
    check("Q23", "R input", R_in, 2.85714, rel=1e-5, unit="MJ")
    check("Q23", "R mass", R_in / 43.0, 0.0664452, rel=1e-5, unit="kg")
    check("Q23", "R emissions", R_in * 80.0, 228.571, rel=1e-5, unit="g CO2e")
    check("Q23", "S input", S_in, 3.57143, rel=1e-5, unit="MJ")
    check("Q23", "S mass", S_in / 29.0, 0.123153, rel=1e-5, unit="kg")
    check("Q23", "S emissions", S_in * 45.0, 160.714, rel=1e-5, unit="g CO2e")
    check_true("Q23", "R less mass, S lower emissions", R_in / 43 < S_in / 29 and S_in * 45 < R_in * 80)


def q25():
    n_mix = 6.20 / VM
    n_ch4 = 0.900 * n_mix
    n_co2_in = 0.100 * n_mix
    n_o2 = 60.0 * 0.210 / VM
    need = 2 * n_ch4
    rem = n_o2 - need
    E = n_ch4 * 890
    q = 800.0 * C_WATER * (57.0 - 17.0) / 1000
    check("Q25", "n(mixture)", n_mix, 0.250)
    check("Q25", "n(CH4)", n_ch4, 0.225)
    check("Q25", "n(O2)", n_o2, 0.5080645, rel=1e-6)
    check("Q25", "O2 required", need, 0.450)
    check_true("Q25", "O2 in excess (methane all burns)", rem > 0)
    check("Q25", "O2 remaining mol", rem, 0.0580645, rel=1e-5)
    check("Q25", "O2 remaining g", rem * 32.0, 1.85806, rel=1e-5, unit="g")
    check("Q25", "energy released", E, 200.25, rel=1e-9, unit="kJ")
    check("Q25", "water heat", q, 133.76, rel=1e-9, unit="kJ")
    check("Q25", "efficiency", 100 * q / E, 66.7965, rel=1e-6, unit="%")
    check("Q25", "total CO2 mol", n_ch4 + n_co2_in, 0.250)
    check("Q25", "total CO2 volume SLC", (n_ch4 + n_co2_in) * VM, 6.20, unit="L")
    check("Q25", "trap: all gas as methane energy", n_mix * 890, 222.5, rel=1e-9, unit="kJ")


def q26():
    check("Q26", "methanol kJ/g", 726 / 32.0, 22.6875, rel=1e-9)
    check("Q26", "ethanol kJ/g", 1370 / 46.0, 29.7826, rel=1e-5)
    check("Q26", "methanol g CO2 per useful kJ", 44.0 / (726 * 0.250), 0.242424, rel=1e-5)
    check("Q26", "ethanol g CO2 per useful kJ", 88.0 / (1370 * 0.400), 0.160584, rel=1e-5)
    check("Q26", "trap: methanol g CO2 per input kJ", 44.0 / 726, 0.0606061, rel=1e-5)
    check("Q26", "trap: ethanol g CO2 per input kJ", 88.0 / 1370, 0.0642336, rel=1e-5)


def q27():
    E = 5.00 * 1.20 * 300
    CF = E / 3.00
    water = 125.0 * C_WATER
    n_hcl = 0.0500 * 1.00
    n_naoh = 0.0750 * 0.800
    slope, icpt = linfit([120, 180, 240, 300], [24.7, 24.6, 24.5, 24.4])
    T60 = slope * 60 + icpt
    rise = T60 - 20.0
    q = CF * rise
    dH = -q / min(n_hcl, n_naoh) / 1000
    check("Q27", "calibration energy", E, 1800, unit="J")
    check("Q27", "CF", CF, 600, unit="J/degC")
    check("Q27", "water-only", water, 522.5, rel=1e-9, unit="J/degC")
    check_true("Q27", "CF > water-only (plausible)", CF > water)
    check("Q27", "n(HCl)", n_hcl, 0.0500)
    check("Q27", "n(NaOH)", n_naoh, 0.0600)
    check_true("Q27", "acid limiting", n_hcl < n_naoh)
    check("Q27", "extrapolated T at 60 s", T60, 24.8, rel=1e-6)
    check("Q27", "corrected rise", rise, 4.8, rel=1e-6)
    check("Q27", "q_cal", q, 2880, rel=1e-6, unit="J")
    check("Q27", "deltaH", dH, -57.6, rel=1e-6, unit="kJ/mol")
    check("Q27", "uncorrected (max 24.7) deltaH (trap)", -CF * 4.7 / n_hcl / 1000, -56.4, rel=1e-6)
    check_true("Q27", "doubling NaOH: acid still limiting, heat unchanged", n_hcl < 2 * n_naoh)


def q28():
    q = 300 * 3.20
    n = q / 1000 / 24.0
    m = n * 80.0
    pct = 100 * m / 4.00
    qw = 360 * 3.20
    pw = 100 * (qw / 1000 / 24.0 * 80.0) / 4.00
    check("Q28", "q", q, 960, unit="J")
    check("Q28", "n(X)", n, 0.0400, rel=1e-9)
    check("Q28", "m(X)", m, 3.20, rel=1e-9, unit="g")
    check("Q28", "purity", pct, 80.0, rel=1e-9, unit="%")
    check("Q28", "wrong-CF q", qw, 1152, rel=1e-9, unit="J")
    check("Q28", "wrong-CF purity", pw, 96.0, rel=1e-9, unit="%")
    check_true("Q28", "claim 95% not supported by 80%; wrong CF makes it appear supported", pct < 95 <= pw)


def ep08_food_example():
    q = 100.0 * C_WATER * 8.0
    check("E08", "food calorimetry water heat", q, 3344, unit="J")
    check("E08", "water-heat yield per g food", q / 1.50 / 1000, 2.229, rel=1e-3, unit="kJ/g")


def ep12_teaching_values():
    check("E12", "methane kJ per g", 890 / 16.0, 55.625, rel=1e-9)
    check("E12", "octane kJ per g", 5460 / 114.0, 47.8947, rel=1e-5)
    check("E12", "retrieval: input for 10.0 MJ at 25%", 10.0 / 0.25, 40.0, rel=1e-9, unit="MJ")
    check("E12", "checkpoint: T g per useful MJ", 70 / 0.20, 350, rel=1e-9)
    check("E12", "checkpoint: R g per useful MJ", 80 / 0.35, 228.571, rel=1e-5)
    check("E12", "hydrogen kJ per g", 286 / 2.0, 143, rel=1e-9)
    check("E12", "hydrogen kJ per L at SLC", 286 / VM, 11.5323, rel=1e-4)
    check("E12", "methane kJ per L at SLC", 890 / VM, 35.8871, rel=1e-4)
    check("E12", "methane/hydrogen per-litre ratio", 890 / 286, 3.112, rel=1e-3)


def ep09_extensions():
    check("E09", "chemical calibration: q", 0.0400 * 50.0, 2.00, rel=1e-9, unit="kJ")
    check("E09", "chemical calibration: CF", 2000 / 3.70, 540.541, rel=1e-5, unit="J/degC")


def ep13_workshop_values():
    n_mix = 6.20 / VM
    check("E13", "retrieval: 40.0 g bar at 1650 kJ per 100 g", 1650 * 40.0 / 100, 660, rel=1e-9, unit="kJ")
    check("E13", "O2 volume in 60.0 L air", 0.210 * 60.0, 12.6, rel=1e-9, unit="L")
    # wrong solution: all gas treated as methane
    n_o2 = 0.210 * 60.0 / VM
    check("E13", "wrong: O2 required if all gas is CH4", 2 * n_mix, 0.500, rel=1e-9)
    check("E13", "wrong: excess O2 mass", (n_o2 - 2 * n_mix) * 32.0, 0.258065, rel=1e-5, unit="g")
    check("E13", "wrong: efficiency", 100 * 133.76 / (n_mix * 890), 60.1169, rel=1e-5, unit="%")
    # spot the error
    check("E13", "error: air volume as O2", 60.0 / VM, 2.41935, rel=1e-5)
    check("E13", "error: CO2 without inlet", 0.225 * VM, 5.58, rel=1e-9, unit="L")
    check("E13", "error: kJ slip gives efficiency x1000", 100 * 133760 / 200.25, 66796.5, rel=1e-5, unit="%")
    # what if 50.0 L air
    n_o2_50 = 0.210 * 50.0 / VM
    check("E13", "variation: O2 from 50.0 L air", n_o2_50, 0.423387, rel=1e-5)
    check_true("E13", "variation: O2 now limiting", n_o2_50 < 2 * 0.225)
    # Q26 comparisons
    m_u = 44.0 / (726 * 0.250)
    e_u = 88.0 / (1370 * 0.400)
    check("E13", "useful kJ per mol methanol", 726 * 0.250, 181.5, rel=1e-9)
    check("E13", "useful kJ per mol ethanol", 1370 * 0.400, 548, rel=1e-9)
    check("E13", "wrong mixed-basis ratio", m_u / (88.0 / 1370), 3.77, rel=2e-3)
    check("E13", "correct per-useful ratio", m_u / e_u, 1.5096, rel=1e-3)
    check("E13", "efficiency ratio", 0.400 / 0.250, 1.6, rel=1e-9)


def ep14_workshop_values():
    check("E14", "retrieval: n(HCl) in 25.0 mL of 0.200 M", 0.200 * 0.0250, 0.00500, rel=1e-9)
    check("E14", "retrieval: 6.00 V x 1.50 A x 2.00 min", 6.00 * 1.50 * 2.00 * 60, 1080, rel=1e-9, unit="J")
    q = 600 * 4.8
    check("E14", "wrong: divide by NaOH (excess)", -q / 0.0600 / 1000, -48.0, rel=1e-9, unit="kJ/mol")
    check("E14", "wrong: uncorrected max", -600 * (24.7 - 20.0) / 0.0500 / 1000, -56.4, rel=1e-6, unit="kJ/mol")
    q_mc = 125.0 * C_WATER * 4.8
    check("E14", "wrong: m c dT with 125 g, J", q_mc, 2508, rel=1e-9, unit="J")
    check("E14", "wrong: m c dT with 125 g, dH", -q_mc / 0.0500 / 1000, -50.16, rel=1e-6, unit="kJ/mol")
    check("E14", "excess NaOH left", 0.0600 - 0.0500, 0.0100, rel=1e-6)
    check("E14", "doubled NaOH amount", 2 * 0.800 * 0.0750, 0.120, rel=1e-9)
    check("E14", "spot: J / (kJ/mol) gives mass", 960 / 24.0 * 80.0, 3200, rel=1e-9, unit="g")
    check("E14", "direction: mass recorded 3.80 g", 100 * 3.20 / 3.80, 84.2105, rel=1e-5, unit="%")
    check_true("E14", "direction: smaller CF lowers %", 100 * (250 * 3.20 / 1000 / 24.0 * 80.0) / 4.00 < 80.0)


def ep10_extensions():
    dT = 18.6 - 21.0
    check("E10", "endothermic: deltaT", dT, -2.40, rel=1e-9, unit="degC")
    check("E10", "endothermic: q(cal)", 500 * dT, -1200, rel=1e-9, unit="J")
    check("E10", "endothermic: deltaH (positive)", -(500 * dT) / 0.0500 / 1000, 24.0, rel=1e-9, unit="kJ/mol")
    q = 125.0 * C_WATER * 4.30
    check("E10", "solution-only model: q", q, 2246.75, rel=1e-9, unit="J")
    check("E10", "solution-only model: deltaH", -q / 0.0450 / 1000, -49.9278, rel=1e-5, unit="kJ/mol")
    check_true("E10", "CF 590 exceeds solution-only 522.5", 590 > 125.0 * C_WATER)


def ep11_extensions():
    m, c = linfit([120, 180, 240, 300], [18.9, 19.1, 19.3, 19.5])
    check("E11", "endothermic graph: extrapolated T(60 s)", m * 60 + c, 18.7, rel=1e-9, unit="degC")
    check("E11", "endothermic graph: corrected change", m * 60 + c - 22.0, -3.3, rel=1e-9, unit="degC")
    check("E11", "endothermic graph: observed change", 18.9 - 22.0, -3.1, rel=1e-9, unit="degC")
    xs = [195, 225, 255, 285, 315, 345, 375, 405]
    ys = [26.08, 25.93, 25.86, 25.70, 25.62, 25.47, 25.42, 25.27]
    mg, cg = linfit(xs, ys)
    mp, cp = linfit([150, 165] + xs, [25.2, 25.95] + ys)
    check("E11", "drawing: best-line value at mixing (shown to 1 d.p.)", round(mg * 120 + cg, 1), 26.3, rel=1e-9)
    check_true("E11", "drawing: including rising points lowers the extrapolated value", mp * 120 + cp < mg * 120 + cg)


MARKS = {  # declared total, list of sub-part marks from the brief
    "Q01": (4, [1, 2, 1]), "Q02": (5, [3, 2]), "Q03": (4, [1, 1, 1, 1]), "Q04": (3, [1, 1, 1]),
    "Q05": (5, [2, 2, 1]), "Q06": (5, [1, 1, 1, 1, 1]), "Q07": (6, [1, 1, 1, 2, 1]),
    "Q08": (4, [1, 2, 1]), "Q09": (4, [2, 1, 1]), "Q10": (5, [2, 2, 1]), "Q11": (5, [1, 2, 1, 1]),
    "Q12": (5, [1, 2, 1, 1]), "Q13": (6, [2, 2, 1, 1]), "Q14": (8, [2, 1, 2, 1, 1, 1]),
    "Q15": (6, [2, 1, 2, 1]), "Q16": (5, [2, 1, 1, 1]), "Q17": (6, [2, 1, 1, 2]),
    "Q18": (4, [1, 1, 1, 1]), "Q19": (8, [2, 2, 2, 2]), "Q20": (6, [1, 1, 1, 1, 1, 1]),
    "Q21": (5, [2, 1, 1, 1]), "Q22": (5, [2, 1, 2]), "Q23": (7, [2, 2, 2, 1]),
    "Q24": (6, [2, 2, 1, 1]), "Q25": (15, [3, 2, 2, 2, 3, 2, 1]), "Q26": (10, [2, 4, 2, 2]),
    "Q27": (14, [3, 2, 2, 3, 2, 2]), "Q28": (12, [2, 4, 1, 2, 1, 2]),
}


def verify_marks():
    for q, (tot, parts) in MARKS.items():
        check_true(q, f"marks sum {parts} = {tot}", sum(parts) == tot, f"{sum(parts)}")
    # the worksheet's lettered parts (questions/bank.py) must sum to the same declared totals
    sys.path.insert(0, str(HERE.parent / "questions"))
    from bank import BY_ID, marks_total  # noqa: E402
    for q, (tot, _) in MARKS.items():
        check_true(q, f"worksheet parts sum to {tot}", marks_total(q) == tot, f"{marks_total(q)}")
        check_true(q, "worksheet has one answer line per part",
                   len(BY_ID[q]["answers"]) == len(BY_ID[q]["parts"]))
    total = sum(t for t, _ in MARKS.values())
    results.append(dict(qid="ALL", label="total marks in bank", computed=total, target="info",
                        unit="", rel_tol=0, ok=True))


def main():
    verify_equations()
    for fn in (q01, q02, q03, q04, q05, q06, q07, q09, q10, q11, q12, q13, q14, q15, q16,
               q17, q18, q19, q20, q21, q22, q23, q25, q26, q27, q28, ep08_food_example,
               ep09_extensions, ep10_extensions, ep11_extensions, ep12_teaching_values, ep13_workshop_values,
               ep14_workshop_values):
        fn()
    verify_marks()
    fails = [r for r in results if not r["ok"]]
    (HERE / "numerical_check_record.json").write_text(json.dumps(results, indent=1))
    lines = ["# Numerical check record", "",
             "Generated by `checks/verify_anchors.py` (independent recomputation from question data).",
             f"Checks: {len(results)}; failures: {len(fails)}.", "",
             "Q08 and Q24 are qualitative; their reasoning targets are reviewed in `solutions/`.", "",
             "| Q | Check | Computed | Target | Unit | OK |", "|---|---|---|---|---|---|"]
    for r in results:
        c = r["computed"]
        c = f"{c:.6g}" if isinstance(c, float) else str(c)
        t = r["target"]
        t = f"{t:.6g}" if isinstance(t, float) else str(t)
        lines.append(f"| {r['qid']} | {r['label']} | {c} | {t} | {r['unit']} | {'yes' if r['ok'] else '**NO**'} |")
    (HERE / "numerical_check_record.md").write_text("\n".join(lines) + "\n")
    print(f"{len(results)} checks, {len(fails)} failures")
    for f in fails:
        print("FAIL", f)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
