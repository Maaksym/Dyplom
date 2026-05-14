"""
SKRYPT DO OBLICZENIA COHEN'S KAPPA
===================================
Oceny drugiego oceniającego (brat) są już wpisane.
Wystarczy uruchomić: python calculate_kappa.py
"""

import numpy as np
import csv
from scipy import stats
from collections import defaultdict

# ========================
# 📊 COHEN'S KAPPA
# ========================
def cohens_kappa(rater1, rater2):
    n = len(rater1)
    if n == 0:
        return 0
    po = sum(1 for a, b in zip(rater1, rater2) if a == b) / n
    pe = sum((rater1.count(c) / n) * (rater2.count(c) / n) for c in range(1, 6))
    if pe == 1:
        return 1.0
    return round((po - pe) / (1 - pe), 3)

def interpret_kappa(kappa):
    if kappa < 0:
        return "brak zgodności"
    elif kappa < 0.20:
        return "minimalna zgodność"
    elif kappa < 0.40:
        return "słaba zgodność"
    elif kappa < 0.60:
        return "umiarkowana zgodność"
    elif kappa < 0.80:
        return "dobra zgodność"
    else:
        return "bardzo dobra zgodność"

# ========================
# 📥 OCENY OCENIAJĄCEGO 1 (z results.csv)
# ========================
rater1_data = {}
with open("results.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (int(row["prompt_num"]), row["model"])
        rater1_data[key] = {
            "poprawnosc": int(row["poprawnosc"]),
            "jezyk": int(row["jezyk"]),
            "poziom": int(row["poziom"]),
            "przydatnosc": int(row["przydatnosc"])
        }

print(f"✅ Wczytano oceny oceniającego 1: {len(rater1_data)} ocen")

# ========================
# 📝 OCENY OCENIAJĄCEGO 2 (brat) - już wpisane
# ========================
rater2_data = {
    (1, "TinyLlama"): {"poprawnosc": 1, "jezyk": 3, "poziom": 1, "przydatnosc": 1},
    (1, "Phi-2"):     {"poprawnosc": 1, "jezyk": 2, "poziom": 1, "przydatnosc": 1},
    (1, "Gemini"):    {"poprawnosc": 4, "jezyk": 4, "poziom": 4, "przydatnosc": 5},
    (2, "TinyLlama"): {"poprawnosc": 1, "jezyk": 3, "poziom": 1, "przydatnosc": 1},
    (2, "Phi-2"):     {"poprawnosc": 1, "jezyk": 2, "poziom": 1, "przydatnosc": 1},
    (2, "Gemini"):    {"poprawnosc": 4, "jezyk": 4, "poziom": 2, "przydatnosc": 4},
    (3, "TinyLlama"): {"poprawnosc": 1, "jezyk": 3, "poziom": 1, "przydatnosc": 1},
    (3, "Phi-2"):     {"poprawnosc": 1, "jezyk": 1, "poziom": 1, "przydatnosc": 1},
    (3, "Gemini"):    {"poprawnosc": 4, "jezyk": 4, "poziom": 5, "przydatnosc": 3},
    (4, "TinyLlama"): {"poprawnosc": 1, "jezyk": 1, "poziom": 1, "przydatnosc": 1},
    (4, "Phi-2"):     {"poprawnosc": 1, "jezyk": 2, "poziom": 1, "przydatnosc": 1},
    (4, "Gemini"):    {"poprawnosc": 5, "jezyk": 5, "poziom": 3, "przydatnosc": 4},
    (5, "TinyLlama"): {"poprawnosc": 1, "jezyk": 2, "poziom": 1, "przydatnosc": 1},
    (5, "Phi-2"):     {"poprawnosc": 1, "jezyk": 2, "poziom": 1, "przydatnosc": 1},
    (5, "Gemini"):    {"poprawnosc": 4, "jezyk": 4, "poziom": 2, "przydatnosc": 4},
    (6, "TinyLlama"): {"poprawnosc": 2, "jezyk": 1, "poziom": 2, "przydatnosc": 2},
    (6, "Phi-2"):     {"poprawnosc": 2, "jezyk": 2, "poziom": 2, "przydatnosc": 2},
    (6, "Gemini"):    {"poprawnosc": 5, "jezyk": 4, "poziom": 3, "przydatnosc": 4},
    (7, "TinyLlama"): {"poprawnosc": 1, "jezyk": 2, "poziom": 2, "przydatnosc": 1},
    (7, "Phi-2"):     {"poprawnosc": 1, "jezyk": 3, "poziom": 1, "przydatnosc": 1},
    (7, "Gemini"):    {"poprawnosc": 4, "jezyk": 4, "poziom": 2, "przydatnosc": 1},
    (8, "TinyLlama"): {"poprawnosc": 1, "jezyk": 3, "poziom": 2, "przydatnosc": 2},
    (8, "Phi-2"):     {"poprawnosc": 1, "jezyk": 4, "poziom": 1, "przydatnosc": 1},
    (8, "Gemini"):    {"poprawnosc": 4, "jezyk": 5, "poziom": 3, "przydatnosc": 4},
    (9, "TinyLlama"): {"poprawnosc": 1, "jezyk": 4, "poziom": 2, "przydatnosc": 1},
    (9, "Phi-2"):     {"poprawnosc": 2, "jezyk": 3, "poziom": 1, "przydatnosc": 1},
    (9, "Gemini"):    {"poprawnosc": 2, "jezyk": 5, "poziom": 2, "przydatnosc": 3},
    (10, "TinyLlama"): {"poprawnosc": 2, "jezyk": 3, "poziom": 2, "przydatnosc": 1},
    (10, "Phi-2"):     {"poprawnosc": 1, "jezyk": 2, "poziom": 1, "przydatnosc": 1},
    (10, "Gemini"):    {"poprawnosc": 4, "jezyk": 5, "poziom": 2, "przydatnosc": 3},
    (11, "TinyLlama"): {"poprawnosc": 1, "jezyk": 2, "poziom": 2, "przydatnosc": 1},
    (11, "Phi-2"):     {"poprawnosc": 1, "jezyk": 2, "poziom": 1, "przydatnosc": 1},
    (11, "Gemini"):    {"poprawnosc": 4, "jezyk": 4, "poziom": 3, "przydatnosc": 4},
    (12, "TinyLlama"): {"poprawnosc": 1, "jezyk": 1, "poziom": 1, "przydatnosc": 1},
    (12, "Phi-2"):     {"poprawnosc": 1, "jezyk": 2, "poziom": 2, "przydatnosc": 1},
    (12, "Gemini"):    {"poprawnosc": 5, "jezyk": 5, "poziom": 4, "przydatnosc": 5},
    (13, "TinyLlama"): {"poprawnosc": 1, "jezyk": 3, "poziom": 2, "przydatnosc": 1},
    (13, "Phi-2"):     {"poprawnosc": 2, "jezyk": 1, "poziom": 2, "przydatnosc": 2},
    (13, "Gemini"):    {"poprawnosc": 5, "jezyk": 5, "poziom": 5, "przydatnosc": 5},
    (14, "TinyLlama"): {"poprawnosc": 1, "jezyk": 1, "poziom": 1, "przydatnosc": 1},
    (14, "Phi-2"):     {"poprawnosc": 1, "jezyk": 2, "poziom": 1, "przydatnosc": 1},
    (14, "Gemini"):    {"poprawnosc": 4, "jezyk": 5, "poziom": 4, "przydatnosc": 4},
    (15, "TinyLlama"): {"poprawnosc": 1, "jezyk": 1, "poziom": 1, "przydatnosc": 1},
    (15, "Phi-2"):     {"poprawnosc": 1, "jezyk": 2, "poziom": 1, "przydatnosc": 1},
    (15, "Gemini"):    {"poprawnosc": 5, "jezyk": 4, "poziom": 4, "przydatnosc": 5},
    (16, "TinyLlama"): {"poprawnosc": 1, "jezyk": 1, "poziom": 1, "przydatnosc": 1},
    (16, "Phi-2"):     {"poprawnosc": 1, "jezyk": 1, "poziom": 1, "przydatnosc": 1},
    (16, "Gemini"):    {"poprawnosc": 4, "jezyk": 3, "poziom": 4, "przydatnosc": 4},
    (17, "TinyLlama"): {"poprawnosc": 1, "jezyk": 2, "poziom": 2, "przydatnosc": 1},
    (17, "Phi-2"):     {"poprawnosc": 1, "jezyk": 1, "poziom": 1, "przydatnosc": 1},
    (17, "Gemini"):    {"poprawnosc": 5, "jezyk": 5, "poziom": 4, "przydatnosc": 5},
    (18, "TinyLlama"): {"poprawnosc": 1, "jezyk": 1, "poziom": 1, "przydatnosc": 1},
    (18, "Phi-2"):     {"poprawnosc": 1, "jezyk": 1, "poziom": 1, "przydatnosc": 1},
    (18, "Gemini"):    {"poprawnosc": 3, "jezyk": 5, "poziom": 3, "przydatnosc": 3},
    (19, "TinyLlama"): {"poprawnosc": 1, "jezyk": 2, "poziom": 1, "przydatnosc": 1},
    (19, "Phi-2"):     {"poprawnosc": 2, "jezyk": 2, "poziom": 1, "przydatnosc": 2},
    # Gemini niedostępny dla promptu 19
    (20, "TinyLlama"): {"poprawnosc": 1, "jezyk": 1, "poziom": 1, "przydatnosc": 2},
    (20, "Phi-2"):     {"poprawnosc": 2, "jezyk": 2, "poziom": 1, "przydatnosc": 1},
    (20, "Gemini"):    {"poprawnosc": 4, "jezyk": 5, "poziom": 4, "przydatnosc": 4},
}

print(f"✅ Oceny oceniającego 2 (brat): {len(rater2_data)} ocen")

# ========================
# WSPÓLNE KLUCZE
# ========================
common_keys = [k for k in rater1_data
               if k in rater2_data
               and rater1_data[k]["poprawnosc"] > 0
               and rater2_data[k]["poprawnosc"] > 0]

print(f"✅ Wspólne oceny (obaj oceniający): {len(common_keys)}")

# ========================
# KAPPA PER KRYTERIUM
# ========================
print("\n" + "="*55)
print("WYNIKI COHEN'S KAPPA")
print("="*55)

criteria = ["poprawnosc", "jezyk", "poziom", "przydatnosc"]
kappas = []

for c in criteria:
    r1 = [rater1_data[k][c] for k in common_keys]
    r2 = [rater2_data[k][c] for k in common_keys]
    k = cohens_kappa(r1, r2)
    kappas.append(k)
    print(f"  {c:15}: κ = {k:6.3f}  →  {interpret_kappa(k)}")

overall_k = round(np.mean(kappas), 3)
print(f"\n  {'Średnia κ':15}: κ = {overall_k:6.3f}  →  {interpret_kappa(overall_k)}")

# ========================
# KAPPA PER MODEL
# ========================
print("\nKappa per model:")
for model in ["TinyLlama", "Phi-2", "Gemini"]:
    model_keys = [k for k in common_keys if k[1] == model]
    r1_all, r2_all = [], []
    for k in model_keys:
        for c in criteria:
            r1_all.append(rater1_data[k][c])
            r2_all.append(rater2_data[k][c])
    if r1_all:
        mk = cohens_kappa(r1_all, r2_all)
        print(f"  {model:12}: κ = {mk:.3f}  →  {interpret_kappa(mk)}")

# ========================
# SREDNIE + SD
# ========================
print("\n" + "="*55)
print("ŚREDNIE OCENY I ODCHYLENIE STANDARDOWE")
print("="*55)

model_scores = defaultdict(lambda: defaultdict(list))
for key, vals in rater1_data.items():
    model = key[1]
    if vals["poprawnosc"] > 0:
        for c in criteria:
            model_scores[model][c].append(vals[c])

for model in ["TinyLlama", "Phi-2", "Gemini"]:
    print(f"\n{model}:")
    all_vals = []
    for c in criteria:
        vals = model_scores[model][c]
        if vals:
            m = np.mean(vals)
            sd = np.std(vals, ddof=1)
            all_vals.extend(vals)
            print(f"  {c:15}: M={m:.2f}  SD={sd:.2f}  (n={len(vals)})")
    if all_vals:
        print(f"  {'Ogólna':15}: M={np.mean(all_vals):.2f}")

# ========================
# KRUSKAL-WALLIS
# ========================
print("\n" + "="*55)
print("TEST KRUSKALA-WALLISA")
print("="*55)

for c in criteria:
    groups = [model_scores[m][c] for m in ["TinyLlama", "Phi-2", "Gemini"]
              if model_scores[m][c]]
    if len(groups) >= 2:
        h, p = stats.kruskal(*groups)
        sig = "✅ ISTOTNA (p<0.05)" if p < 0.05 else "❌ NIE istotna"
        print(f"  {c:15}: H={h:.3f}, p={p:.6f}  →  {sig}")

print("\n" + "="*55)
print("GOTOWE! Użyj tych wyników w pracy magisterskiej.")
print("="*55)