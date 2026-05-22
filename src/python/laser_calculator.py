#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║         LASER CAVITY THRESHOLD GAIN CALCULATOR                  ║
║   Aplicaciones de Series Numéricas — Ganancia de Cavidad LASER  ║
║                                                                  ║
║  Autor       : Darío Ricardo de Santiago Sasinka                 ║
║  Institución : UTN FRC — Ingeniería Metalúrgica                  ║
║  DOI         : 10.13140/RG.2.2.29126.18241                       ║
║  Licencia    : CC BY 4.0 (Creative Commons Attribution 4.0)      ║
║                                                                  ║
║  Este programa es parte del trabajo de investigación y puede    ║
║  ser usado libremente citando la fuente original.               ║
║  Para más detalles: https://doi.org/10.13140/RG.2.2.29126.18241  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import math
import sys
import os

# ─── COLORES ANSI ──────────────────────────────────────────────────────────────
class Color:
    CYAN    = '\033[96m'
    BLUE    = '\033[94m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    RED     = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    RESET   = '\033[0m'

# ─── TRADUCCIONES (CORREGIDAS) ────────────────────────────────────────────────
STRINGS = {
    'es': {
        'title':         "CALCULADORA DE CAVIDAD LÁSER",
        'subtitle':      "Ganancia umbral por series de Taylor",
        'menu_title':    "═══ MENÚ PRINCIPAL ═══",
        'm1': "1. Cálculo simple (punto único)",
        'm2': "2. Barrido de parámetros",
        'm3': "3. Convergencia de la serie de Taylor",
        'm4': "4. Comparar presets de espejos",
        'm5': "5. Manual de ayuda",
        'm6': "6. Cambiar idioma",
        'm0': "0. Salir",
        'choose': "Elige una opción",
        'invalid': "Opción inválida.",

        'inp_L':    "Longitud total de cavidad L [cm]",
        'inp_lam':  "Longitud de onda λ [nm]",
        'inp_R1':   "Reflectividad R₁ — espejo posterior [%]",
        'inp_R2':   "Reflectividad R₂ — acoplador de salida [%]",
        'inp_loss': "Pérdidas adicionales por paso [%]",
        'inp_n':    "Índice de refracción del medio activo (n)",
        'inp_Lm':   "Longitud del medio activo [cm]",

        'res_header':   "─── RESULTADOS ───────────────────────────────",
        'res_alpha':    "Ganancia umbral lineal   αc",
        'res_exact':    "Ganancia umbral exacta   αc (trascendental)",
        'res_x':        "Parámetro               2αL",
        'res_err':      "Error de truncamiento",
        'res_valid':    "Validez de la aprox.",
        'res_finesse':  "Finesse de la cavidad",
        'res_fsr':      "Free Spectral Range (FSR)",
        'res_optpath':  "Longitud óptica ida/vuelta",

        'valid_ok':   f"{Color.GREEN}✓ VÁLIDA  (error < 0.5%){Color.RESET}",
        'valid_warn': f"{Color.YELLOW}⚠ MARGINAL (error entre 0.5% y 10%){Color.RESET}",
        'valid_bad':  f"{Color.RED}✗ INVÁLIDA (usar ecuación exacta){Color.RESET}",

        'sweep_title':  "═══ BARRIDO DE PARÁMETROS ═══",
        'sweep_var':    "Variable a barrer: (1) L   (2) R₁   (3) R₂",
        'sweep_from':   "Valor inicial",
        'sweep_to':     "Valor final",
        'sweep_pts':    "Número de puntos",

        'series_title': "═══ CONVERGENCIA DE SERIE DE TAYLOR ═══",
        'series_alpha': "Ganancia α [cm⁻¹]",
        'series_L':     "Longitud L [cm]",
        'series_terms': "Número de términos N",
        'ser_n':        "n",
        'ser_term':     "Término",
        'ser_partial':  "Suma parcial",
        'ser_exact':    "Exacto",
        'ser_err':      "Error %",

        'man_title': "═══ MANUAL DE AYUDA ═══",
        'man_text': f"""
{Color.CYAN}FUNDAMENTO TEÓRICO{Color.RESET}
═══════════════════
El láser opera cuando la ganancia de luz en la cavidad iguala las pérdidas
(condición de umbral). Para una cavidad Fabry-Pérot con dos espejos R₁ y R₂:

    φ_i · exp(2αL) · R₁ · R₂ = φ_f

En el umbral φ_i = φ_f, por lo que:

    exp(−2αL) = R₁ · R₂

Expandiendo en serie de Taylor (válido para 2αL ≪ 1):

    1 − 2αL ≈ R₁ · R₂

Despejando:

    αc = (1 − R₁ · R₂) / (2L)          ← {Color.GREEN}FÓRMULA CENTRAL{Color.RESET}

{Color.YELLOW}ERROR DE TRUNCAMIENTO{Color.RESET}
══════════════════════
El término dominante omitido es el cuadrático:
    ε_trunc ≈ (2αL)² / 2
    ε_rel   ≈ αL (× 100%)

  2αL < 0.1  →  error < 0.5%   {Color.GREEN}✓ Válido{Color.RESET}
  2αL < 0.5  →  error < 10%    {Color.YELLOW}⚠ Marginal{Color.RESET}
  2αL ≥ 1    →  error > 50%    {Color.RED}✗ Usar ecuación exacta{Color.RESET}

{Color.CYAN}OTRAS FÓRMULAS CALCULADAS{Color.RESET}
═══════════════════════════
  FSR [GHz]     = c / (2 · n · L)         (separación modos)
  Finesse       = π · √(R₁·R₂) / (1 − R₁·R₂)   ← {Color.GREEN}fórmula correcta{Color.RESET}
  Camino óptico = 2 · n · L               [µm]

{Color.MAGENTA}PARÁMETROS{Color.RESET}
═══════════
  L   [cm]  — Longitud total de la cavidad
  λ   [nm]  — Longitud de onda de operación
  R₁  [%]   — Espejo posterior (alta reflectancia, ≈99-100%)
  R₂  [%]   — Acoplador de salida (≈90-98%)
  Pérd [%]  — Pérdidas internas adicionales por paso
  n         — Índice de refracción del medio activo
  Lm [cm]   — Longitud física del medio activo

{Color.BLUE}PRESETS DISPONIBLES{Color.RESET}
════════════════════
  Ver Opción 4 del menú principal.
""",
        'comp_title': "═══ COMPARACIÓN DE PRESETS ═══",
    },
    'en': {
        'title':         "LASER CAVITY CALCULATOR",
        'subtitle':      "Threshold gain via Taylor series",
        'menu_title':    "═══ MAIN MENU ═══",
        'm1': "1. Single-point calculation",
        'm2': "2. Parameter sweep",
        'm3': "3. Taylor series convergence",
        'm4': "4. Compare mirror presets",
        'm5': "5. Help manual",
        'm6': "6. Change language",
        'm0': "0. Exit",
        'choose': "Choose an option",
        'invalid': "Invalid option.",

        'inp_L':    "Total cavity length L [cm]",
        'inp_lam':  "Wavelength λ [nm]",
        'inp_R1':   "Reflectivity R₁ — rear mirror [%]",
        'inp_R2':   "Reflectivity R₂ — output coupler [%]",
        'inp_loss': "Additional losses per pass [%]",
        'inp_n':    "Refractive index of gain medium (n)",
        'inp_Lm':   "Active medium length [cm]",

        'res_header':   "─── RESULTS ──────────────────────────────────",
        'res_alpha':    "Linear threshold gain   αc",
        'res_exact':    "Exact threshold gain    αc (transcendental)",
        'res_x':        "Parameter              2αL",
        'res_err':      "Truncation error",
        'res_valid':    "Approximation validity",
        'res_finesse':  "Cavity finesse",
        'res_fsr':      "Free Spectral Range (FSR)",
        'res_optpath':  "Round-trip optical path",

        'valid_ok':   f"{Color.GREEN}✓ VALID   (error < 0.5%){Color.RESET}",
        'valid_warn': f"{Color.YELLOW}⚠ MARGINAL (error 0.5% – 10%){Color.RESET}",
        'valid_bad':  f"{Color.RED}✗ INVALID (use exact equation){Color.RESET}",

        'sweep_title':  "═══ PARAMETER SWEEP ═══",
        'sweep_var':    "Variable to sweep: (1) L   (2) R₁   (3) R₂",
        'sweep_from':   "Start value",
        'sweep_to':     "End value",
        'sweep_pts':    "Number of points",

        'series_title': "═══ TAYLOR SERIES CONVERGENCE ═══",
        'series_alpha': "Gain α [cm⁻¹]",
        'series_L':     "Length L [cm]",
        'series_terms': "Number of terms N",
        'ser_n':     "n",
        'ser_term':  "Term",
        'ser_partial':"Partial sum",
        'ser_exact': "Exact",
        'ser_err':   "Error %",

        'man_title': "═══ HELP MANUAL ═══",
        'man_text': f"""
{Color.CYAN}THEORETICAL BACKGROUND{Color.RESET}
═══════════════════════
The laser operates when the cavity gain equals the losses (threshold condition).
For a Fabry-Pérot cavity with mirrors R₁ and R₂:

    φ_i · exp(2αL) · R₁ · R₂ = φ_f

At threshold φ_i = φ_f, so:

    exp(−2αL) = R₁ · R₂

Taylor series expansion (valid for 2αL ≪ 1):

    1 − 2αL ≈ R₁ · R₂

Solving for αc:

    αc = (1 − R₁ · R₂) / (2L)          ← {Color.GREEN}CENTRAL FORMULA{Color.RESET}

{Color.YELLOW}TRUNCATION ERROR{Color.RESET}
═════════════════
The dominant omitted term is the quadratic:
    ε_trunc ≈ (2αL)² / 2
    ε_rel   ≈ αL (× 100%)

  2αL < 0.1  →  error < 0.5%   {Color.GREEN}✓ Valid{Color.RESET}
  2αL < 0.5  →  error < 10%    {Color.YELLOW}⚠ Marginal{Color.RESET}
  2αL ≥ 1    →  error > 50%    {Color.RED}✗ Use exact equation{Color.RESET}

{Color.CYAN}CALCULATED QUANTITIES{Color.RESET}
══════════════════════
  FSR [GHz]   = c / (2 · n · L)
  Finesse     = π · √(R₁R₂) / (1 − R₁R₂)   ← {Color.GREEN}correct formula{Color.RESET}
  Opt. path   = 2 · n · L    [µm]
""",
        'comp_title': "═══ PRESET COMPARISON ═══",
    },
    'pt': {
        'title':         "CALCULADORA DE CAVIDADE LASER",
        'subtitle':      "Ganho limiar por séries de Taylor",
        'menu_title':    "═══ MENU PRINCIPAL ═══",
        'm1': "1. Cálculo simples (ponto único)",
        'm2': "2. Varredura de parâmetros",
        'm3': "3. Convergência da série de Taylor",
        'm4': "4. Comparar presets de espelhos",
        'm5': "5. Manual de ajuda",
        'm6': "6. Mudar idioma",
        'm0': "0. Sair",
        'choose': "Escolha uma opção",
        'invalid': "Opção inválida.",

        'inp_L':    "Comprimento total da cavidade L [cm]",
        'inp_lam':  "Comprimento de onda λ [nm]",
        'inp_R1':   "Refletividade R₁ — espelho posterior [%]",
        'inp_R2':   "Refletividade R₂ — acoplador de saída [%]",
        'inp_loss': "Perdas internas adicionais por passo [%]",
        'inp_n':    "Índice de refração do meio ativo (n)",
        'inp_Lm':   "Comprimento do meio ativo [cm]",

        'res_header':   "─── RESULTADOS ───────────────────────────────",
        'res_alpha':    "Ganho limiar linear   αc",
        'res_exact':    "Ganho limiar exato    αc (transcendental)",
        'res_x':        "Parâmetro            2αL",
        'res_err':      "Erro de truncamento",
        'res_valid':    "Validade da aprox.",
        'res_finesse':  "Finesse da cavidade",
        'res_fsr':      "Free Spectral Range (FSR)",
        'res_optpath':  "Caminho óptico ida e volta",

        'valid_ok':   f"{Color.GREEN}✓ VÁLIDA  (erro < 0.5%){Color.RESET}",
        'valid_warn': f"{Color.YELLOW}⚠ MARGINAL (erro entre 0.5% e 10%){Color.RESET}",
        'valid_bad':  f"{Color.RED}✗ INVÁLIDA (usar equação exata){Color.RESET}",

        'sweep_title':  "═══ VARREDURA DE PARÂMETROS ═══",
        'sweep_var':    "Variável a varrer: (1) L   (2) R₁   (3) R₂",
        'sweep_from':   "Valor inicial",
        'sweep_to':     "Valor final",
        'sweep_pts':    "Número de pontos",

        'series_title': "═══ CONVERGÊNCIA DA SÉRIE DE TAYLOR ═══",
        'series_alpha': "Ganho α [cm⁻¹]",
        'series_L':     "Comprimento L [cm]",
        'series_terms': "Número de termos N",
        'ser_n':     "n",
        'ser_term':  "Termo",
        'ser_partial':"Soma parcial",
        'ser_exact': "Exato",
        'ser_err':   "Erro %",

        'man_title': "═══ MANUAL DE AJUDA ═══",
        'man_text': f"""
{Color.CYAN}BASE TEÓRICA{Color.RESET}
═════════════
O laser opera quando o ganho na cavidade iguala as perdas (condição de limiar).
Para uma cavidade Fabry-Pérot com espelhos R₁ e R₂:

    φ_i · exp(2αL) · R₁ · R₂ = φ_f

No limiar φ_i = φ_f:

    exp(−2αL) = R₁ · R₂

Expansão em série de Taylor (válida para 2αL ≪ 1):

    1 − 2αL ≈ R₁ · R₂

Isolando αc:

    αc = (1 − R₁ · R₂) / (2L)          ← {Color.GREEN}FÓRMULA CENTRAL{Color.RESET}
""",
        'comp_title': "═══ COMPARAÇÃO DE PRESETS ═══",
    },
}

# ─── PRESETS ───────────────────────────────────────────────────────────────────
MIRROR_PRESETS = {
    "Nd:YAG HR/OC (1064 nm)":  {'R1': 99.0,  'R2': 95.0,  'lam': 1064, 'desc': 'Industrial cut/weld'},
    "CO₂ Metal Cut (10.6 µm)": {'R1': 99.5,  'R2': 92.0,  'lam': 10600,'desc': 'Sheet metal cutting'},
    "HeNe Lab (632.8 nm)":     {'R1': 99.9,  'R2': 98.0,  'lam': 633,  'desc': 'Alignment / holography'},
    "Diode VCSEL":             {'R1': 99.0,  'R2': 99.5,  'lam': 850,  'desc': 'Vertical cavity'},
    "Ruby pulsed (694 nm)":    {'R1': 100.0, 'R2': 70.0,  'lam': 694,  'desc': 'Q-switched'},
    "Ti:Sapphire fs (800 nm)": {'R1': 99.9,  'R2': 90.0,  'lam': 800,  'desc': 'Ultrafast / CPA'},
}

MEDIUM_PRESETS = {
    "Nd:YAG (crystal)": {'n': 1.82,   'Lm': 10.0},
    "CO₂ (gas, 10 bar)":{'n': 1.0003, 'Lm': 50.0},
    "HeNe (gas)":       {'n': 1.0001, 'Lm': 20.0},
    "Er:glass":         {'n': 1.53,   'Lm': 8.0},
    "Ti:Sapphire":      {'n': 1.76,   'Lm': 10.0},
    "GaAs Diode":       {'n': 3.6,    'Lm': 0.03},
}

C_LIGHT = 2.998e10  # cm/s

# ═══════════════════════════════════════════════════════════════════════════════
#  NÚCLEO FÍSICO (CORREGIDO)
# ═══════════════════════════════════════════════════════════════════════════════
def calc_threshold(L, R1, R2, loss_pct=0.0):
    loss = loss_pct / 100.0
    r1e = R1 * (1 - loss)
    r2e = R2 * (1 - loss)
    prod_efectivo = r1e * r2e

    alpha_lin = (1.0 - prod_efectivo) / (2.0 * L)

    if prod_efectivo <= 0:
        alpha_exact = float('inf')
    else:
        alpha_exact = -math.log(prod_efectivo) / (2.0 * L)

    x = 2.0 * alpha_lin * L
    exact_exp = math.exp(-x)
    approx_exp = 1.0 - x
    if abs(exact_exp) > 1e-15:
        rel_err = abs(exact_exp - approx_exp) / abs(exact_exp) * 100.0
    else:
        rel_err = float('inf')

    trunc_err = x * x / 2.0
    return {
        'alpha_lin':   alpha_lin,
        'alpha_exact': alpha_exact,
        'x':           x,
        'rel_err':     rel_err,
        'trunc_err':   trunc_err,
        'r1e':         r1e,
        'r2e':         r2e,
    }

def calc_fsr(L, n):
    return C_LIGHT / (2.0 * n * L * 1e9)

def calc_finesse(R1, R2):
    producto = R1 * R2
    if producto >= 1.0:
        return float('inf')
    return math.pi * math.sqrt(producto) / (1.0 - producto)

def validity_tag(x, strings):
    if x < 0.1:
        return strings['valid_ok']
    elif x < 0.5:
        return strings['valid_warn']
    else:
        return strings['valid_bad']

# ─── FUNCIONES UI ─────────────────────────────────────────────────────────────
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner(lang):
    s = STRINGS[lang]
    print()
    print(f"{Color.CYAN}╔══════════════════════════════════════════════════════════╗{Color.RESET}")
    print(f"{Color.CYAN}║{Color.RESET}  {Color.BOLD}{Color.CYAN}LASER·CALC{Color.RESET}{' ' * 47}{Color.CYAN}║{Color.RESET}")
    print(f"{Color.CYAN}║{Color.RESET}  {s['title']:^54}  {Color.CYAN}║{Color.RESET}")
    print(f"{Color.CYAN}║{Color.RESET}  {s['subtitle']:^54}  {Color.CYAN}║{Color.RESET}")
    print(f"{Color.CYAN}╚══════════════════════════════════════════════════════════╝{Color.RESET}")
    print(f"  {Color.DIM}UTN FRC — Ingeniería Metalúrgica | DOI 10.13140/RG.2.2.29126.18241{Color.RESET}")
    print()

def ask_float(prompt, default=None):
    while True:
        dflt = f" [{default}]" if default is not None else ""
        raw  = input(f"  {prompt}{dflt}: ").strip()
        if raw == '' and default is not None:
            return float(default)
        try:
            return float(raw)
        except ValueError:
            print(f"  {Color.RED}⚠ Valor numérico requerido.{Color.RESET}")

def ask_int(prompt, default=None, lo=None, hi=None):
    while True:
        dflt = f" [{default}]" if default is not None else ""
        raw  = input(f"  {prompt}{dflt}: ").strip()
        if raw == '' and default is not None:
            return int(default)
        try:
            v = int(raw)
            if lo is not None and v < lo: raise ValueError
            if hi is not None and v > hi: raise ValueError
            return v
        except ValueError:
            print(f"  {Color.RED}⚠ Entero requerido [{lo}-{hi}].{Color.RESET}")

def print_results(res, fsr, finesse, opt_path, strings):
    s = strings
    print()
    print(f"  {Color.CYAN}{s['res_header']}{Color.RESET}")
    print(f"  {s['res_alpha']:<38} {Color.GREEN}{res['alpha_lin']:.6e}{Color.RESET}  cm⁻¹")
    print(f"  {s['res_exact']:<38} {Color.BLUE}{res['alpha_exact']:.6e}{Color.RESET}  cm⁻¹")
    print(f"  {s['res_x']:<38} {res['x']:.6f}")
    print(f"  {s['res_err']:<38} {res['rel_err']:.4f} %")
    print(f"  {s['res_valid']:<38} {validity_tag(res['x'], s)}")
    print(f"  {s['res_finesse']:<38} {Color.MAGENTA}{finesse:.2f}{Color.RESET}")
    print(f"  {s['res_fsr']:<38} {fsr:.4f} GHz")
    print(f"  {s['res_optpath']:<38} {opt_path*1e4:.2f} µm")
    print()

def get_params(lang):
    s = STRINGS[lang]
    print()
    L    = ask_float(s['inp_L'],    10.0)
    lam  = ask_float(s['inp_lam'],  1064.0)
    R1   = ask_float(s['inp_R1'],   99.0) / 100.0
    R2   = ask_float(s['inp_R2'],   95.0) / 100.0
    loss = ask_float(s['inp_loss'], 0.0)
    n    = ask_float(s['inp_n'],    1.82)
    Lm   = ask_float(s['inp_Lm'],  10.0)
    return L, lam, R1, R2, loss, n, Lm

# ═══════════════════════════════════════════════════════════════════════════════
#  OPCIONES DEL MENÚ
# ═══════════════════════════════════════════════════════════════════════════════
def option_single(lang):
    s = STRINGS[lang]
    L, lam, R1, R2, loss, n, Lm = get_params(lang)
    res      = calc_threshold(L, R1, R2, loss)
    fsr      = calc_fsr(L, n)
    finesse  = calc_finesse(R1, R2)
    opt_path = 2.0 * n * L
    print_results(res, fsr, finesse, opt_path, s)
    input(f"  {Color.DIM}[Enter]{Color.RESET}")

def option_sweep(lang):
    s = STRINGS[lang]
    print(f"\n  {Color.CYAN}{s['sweep_title']}{Color.RESET}")

    L0   = ask_float(s['inp_L'],   10.0)
    R1   = ask_float(s['inp_R1'],  99.0) / 100.0
    R2   = ask_float(s['inp_R2'],  95.0) / 100.0
    loss = ask_float(s['inp_loss'], 0.0)

    print(f"\n  {s['sweep_var']}")
    var_choice = ask_int("  Opción", 1, 1, 3)

    if var_choice == 1:
        vname, unit = "L", "cm"
        dfrom, dto = 1.0, 30.0
    elif var_choice == 2:
        vname, unit = "R₁", "%"
        dfrom, dto = 85.0, 99.9
    else:
        vname, unit = "R₂", "%"
        dfrom, dto = 80.0, 99.0

    vfrom = ask_float(s['sweep_from'], dfrom)
    vto   = ask_float(s['sweep_to'],   dto)
    pts   = ask_int(s['sweep_pts'],    20, 2, 200)

    print()
    header = (f"  {Color.BOLD}{'Val':>10} │ {'αc (cm⁻¹)':>14} │ {'Exacta':>14} │ {'2αL':>8} │ {'Err%':>8} │ Status{Color.RESET}")
    print(header)
    print(f"  {Color.DIM}{'─' * 78}{Color.RESET}")

    for i in range(pts):
        v = vfrom + (vto - vfrom) * i / (pts - 1)
        if var_choice == 1:
            L, r1, r2 = v, R1, R2
        elif var_choice == 2:
            L, r1, r2 = L0, v/100.0, R2
        else:
            L, r1, r2 = L0, R1, v/100.0

        res = calc_threshold(L, r1, r2, loss)
        if res['x'] < 0.1:
            tag = f"{Color.GREEN}✓ OK{Color.RESET}"
        elif res['x'] < 0.5:
            tag = f"{Color.YELLOW}⚠ MARGINAL{Color.RESET}"
        else:
            tag = f"{Color.RED}✗ INVALID{Color.RESET}"
        print(f"  {v:>10.3f} │ {res['alpha_lin']:>14.6e} │ {res['alpha_exact']:>14.6e} │ "
              f"{res['x']:>8.4f} │ {res['rel_err']:>8.3f} │ {tag}")
    print()
    input(f"  {Color.DIM}[Enter]{Color.RESET}")

def option_series(lang):
    s = STRINGS[lang]
    print(f"\n  {Color.CYAN}{s['series_title']}{Color.RESET}")
    alpha  = ask_float(s['series_alpha'], 0.003)
    L      = ask_float(s['series_L'],    10.0)
    nterms = ask_int(s['series_terms'],   8, 1, 15)

    x     = 2.0 * alpha * L
    exact = math.exp(-x)

    print(f"\n  {Color.YELLOW}x = 2αL = {x:.6f}{Color.RESET}   |   {Color.CYAN}e^(−x) exacto = {exact:.10f}{Color.RESET}")
    print()

    hdr = (f"  {Color.BOLD}{s['ser_n']:>4} │ {s['ser_term']:>18} │ {s['ser_partial']:>18} │ "
           f"{s['ser_exact']:>18} │ {s['ser_err']:>10}{Color.RESET}")
    print(hdr)
    print(f"  {Color.DIM}{'─' * 78}{Color.RESET}")

    partial = 0.0
    factorial = 1
    for n in range(nterms):
        if n > 0:
            factorial *= n
        term     = (-x)**n / factorial
        partial += term
        if abs(exact) > 1e-15:
            err = abs(partial - exact) / abs(exact) * 100.0
        else:
            err = 0.0
        marker = f" {Color.GREEN}← lineal{Color.RESET}" if n == 1 else ""
        if err < 0.1:
            err_color = Color.GREEN
        elif err < 5:
            err_color = Color.YELLOW
        else:
            err_color = Color.RED
        print(f"  {n:>4} │ {term:>18.10f} │ {partial:>18.10f} │ {exact:>18.10f} │ "
              f"{err_color}{err:>10.6f}{Color.RESET}%{marker}")
    print()
    input(f"  {Color.DIM}[Enter]{Color.RESET}")

def option_compare(lang):
    s = STRINGS[lang]
    print(f"\n  {Color.CYAN}{s['comp_title']}{Color.RESET}")
    L_base = ask_float(STRINGS[lang]['inp_L'], 10.0)

    print()
    hdr = (f"  {Color.BOLD}{'Preset':<30} │ {'R₁%':>6} │ {'R₂%':>6} │ {'αc':>14} │ {'2αL':>8} │ "
           f"{'Err%':>8} │ {'Finesse':>9}{Color.RESET}")
    print(hdr)
    print(f"  {Color.DIM}{'─' * 90}{Color.RESET}")

    for name, mp in MIRROR_PRESETS.items():
        r1 = mp['R1'] / 100.0
        r2 = mp['R2'] / 100.0
        res     = calc_threshold(L_base, r1, r2, loss_pct=0.0)
        finesse = calc_finesse(r1, r2)
        if res['x'] < 0.1:
            tag = f"{Color.GREEN}✓{Color.RESET}"
        elif res['x'] < 0.5:
            tag = f"{Color.YELLOW}⚠{Color.RESET}"
        else:
            tag = f"{Color.RED}✗{Color.RESET}"
        print(f"  {name:<30} │ {mp['R1']:>6.1f} │ {mp['R2']:>6.1f} │ "
              f"{res['alpha_lin']:>14.6e} │ {res['x']:>8.4f} │ "
              f"{res['rel_err']:>8.3f} │ {finesse:>9.1f}  {tag}")

    print()
    print(f"  {Color.CYAN}─── Active media:{Color.RESET}")
    print(f"  {Color.BOLD}{'Medium':<22} │ {'n':>7} │ {'Lm [cm]':>9} │ {'FSR (GHz)':>12} (L={L_base} cm){Color.RESET}")
    print(f"  {Color.DIM}{'─' * 60}{Color.RESET}")
    for name, med in MEDIUM_PRESETS.items():
        fsr = calc_fsr(L_base, med['n'])
        print(f"  {name:<22} │ {med['n']:>7.4f} │ {med['Lm']:>9.2f} │ {fsr:>12.4f}")
    print()
    input(f"  {Color.DIM}[Enter]{Color.RESET}")

def option_manual(lang):
    s = STRINGS[lang]
    print(f"\n  {Color.CYAN}{s['man_title']}{Color.RESET}")
    print(s['man_text'])
    print()
    input(f"  {Color.DIM}[Enter]{Color.RESET}")

def select_language():
    print(f"\n  {Color.CYAN}Select language / Seleccionar idioma / Selecionar idioma:{Color.RESET}")
    print("   1. Español (ES)")
    print("   2. English (EN)")
    print("   3. Português (PT)")
    ch = ask_int("  Opción", 1, 1, 3)
    return ['es', 'en', 'pt'][ch - 1]

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN (CON COMPATIBILIDAD ANSI Y NOTA DE COPYRIGHT)
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    # Forzar soporte ANSI en terminales Windows modernas
    if os.name == 'nt':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass

    lang = 'es'

    while True:
        cls()
        banner(lang)
        s = STRINGS[lang]
        print(f"  {Color.YELLOW}{s['menu_title']}{Color.RESET}")
        print()
        for key in ['m1','m2','m3','m4','m5','m6','m0']:
            print(f"  {s[key]}")
        print()

        # Nota de copyright en el menú (opcional, pero queda bien)
        print(f"  {Color.DIM}══════════════════════════════════════════════════════════{Color.RESET}")
        print(f"  {Color.DIM}© {Color.RESET}{Color.DIM}Darío Ricardo de Santiago Sasinka — CC BY 4.0 — DOI: 10.13140/RG.2.2.29126.18241{Color.RESET}")
        print()

        try:
            choice = input(f"  {s['choose']} [0-6]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {Color.GREEN}Bye.{Color.RESET}")
            sys.exit(0)

        if choice == '1':
            option_single(lang)
        elif choice == '2':
            option_sweep(lang)
        elif choice == '3':
            option_series(lang)
        elif choice == '4':
            option_compare(lang)
        elif choice == '5':
            option_manual(lang)
        elif choice == '6':
            lang = select_language()
        elif choice == '0':
            print(f"\n  {Color.GREEN}Hasta luego / Goodbye / Até logo.{Color.RESET}\n")
            sys.exit(0)
        else:
            print(f"\n  {Color.RED}{s['invalid']}{Color.RESET}")
            input(f"  {Color.DIM}[Enter]{Color.RESET}")

if __name__ == '__main__':
    main()