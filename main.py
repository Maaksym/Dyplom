import torch
import csv
import os
import time
<<<<<<< HEAD
import numpy as np
=======
>>>>>>> 326a4aeb9e20a01e932fad65ddc899b0c1e2af5e
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM
from google import genai
import collections
from dotenv import load_dotenv
<<<<<<< HEAD
from scipy import stats
=======
>>>>>>> 326a4aeb9e20a01e932fad65ddc899b0c1e2af5e

# ========================
# 🔑 LOAD ENV
# ========================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

# ========================
# 🔹 GEMINI CLIENT
# ========================
client = genai.Client(api_key=GEMINI_API_KEY)

# ========================
# 🔹 MODELS
# ========================
MODEL_1_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MODEL_2_NAME = "microsoft/phi-2"

print("Loading models...")

tokenizer1 = AutoTokenizer.from_pretrained(MODEL_1_NAME)
model1 = AutoModelForCausalLM.from_pretrained(MODEL_1_NAME)

tokenizer2 = AutoTokenizer.from_pretrained(MODEL_2_NAME)
model2 = AutoModelForCausalLM.from_pretrained(MODEL_2_NAME)

print("✅ Modele załadowane!")

# ========================
# 🔹 GENERATE LOCAL
# ========================
def generate_local(model, tokenizer, system_prompt, user_prompt):
    prompt = f"{system_prompt}\n\n{user_prompt}"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        do_sample=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# ========================
<<<<<<< HEAD
# 🔹 GENERATE GEMINI (FIXED - rate limit handling)
=======
# 🔹 GENERATE GEMINI (RETRY)
>>>>>>> 326a4aeb9e20a01e932fad65ddc899b0c1e2af5e
# ========================
def generate_gemini(system_prompt, user_prompt):
    prompt = f"{system_prompt}\n\n{user_prompt}"

<<<<<<< HEAD
    for attempt in range(5):
=======
    for attempt in range(3):
>>>>>>> 326a4aeb9e20a01e932fad65ddc899b0c1e2af5e
        try:
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )
<<<<<<< HEAD
            time.sleep(4)  # pauza 4 sek między zapytaniami (limit 15/min)
            return response.text

        except Exception as e:
            error_str = str(e)

            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                wait_time = 60
                print(f"⚠ Limit Gemini - czekam {wait_time} sek (próba {attempt+1}/5)...")
                time.sleep(wait_time)

            elif "503" in error_str or "UNAVAILABLE" in error_str:
                wait_time = 15
                print(f"⚠ Gemini niedostępny - czekam {wait_time} sek (próba {attempt+1}/5)...")
                time.sleep(wait_time)

            elif "quota" in error_str.lower():
                wait_time = 120
                print(f"⚠ Quota wyczerpana - czekam {wait_time} sek (próba {attempt+1}/5)...")
                time.sleep(wait_time)

            else:
                print(f"⚠ Błąd Gemini (próba {attempt+1}/5): {e}")
                time.sleep(10)

    print("❌ Gemini niedostępny po 5 próbach")
=======
            return response.text

        except Exception as e:
            print(f"⚠ Gemini error (attempt {attempt+1}):", e)
            time.sleep(5)

>>>>>>> 326a4aeb9e20a01e932fad65ddc899b0c1e2af5e
    return "ERROR: Gemini not available"

# ========================
# 📌 SYSTEM PROMPT
# ========================
system_prompt = """Jesteś doświadczonym nauczycielem z wieloletnią praktyką dydaktyczną.
Twoim zadaniem jest tworzenie wysokiej jakości materiałów edukacyjnych dostosowanych do poziomu ucznia.

Dbaj o poprawność merytoryczną, używaj prostego języka, podawaj przykłady i zachowuj logiczną strukturę."""

# ========================
<<<<<<< HEAD
# 📌 PROMPTS - 20 promptów, 5 kategorii x 4 prompty
# ========================
prompts = [
    # --- BIOLOGIA (1-4) ---
    ("Biologia", "Wyjaśnij czym jest fotosynteza dla ucznia szkoły podstawowej."),
    ("Biologia", "Przygotuj zestaw 5 pytań testowych z biologii na temat podziału komórki dla ucznia liceum."),
    ("Biologia", "Stwórz krótki materiał dydaktyczny na temat budowy DNA z 3 zadaniami i odpowiedziami."),
    ("Biologia", "Napisz streszczenie procesu oddychania komórkowego dla ucznia szkoły średniej."),

    # --- MATEMATYKA (5-8) ---
    ("Matematyka", "Wyjaśnij czym jest równanie kwadratowe dla ucznia klasy 8 szkoły podstawowej."),
    ("Matematyka", "Przygotuj 5 zadań z matematyki na temat procentów dla ucznia gimnazjum z odpowiedziami."),
    ("Matematyka", "Stwórz materiał dydaktyczny na temat twierdzenia Pitagorasa z przykładami i ćwiczeniami."),
    ("Matematyka", "Napisz krótkie streszczenie dotyczące funkcji liniowej dla ucznia liceum."),

    # --- HISTORIA (9-12) ---
    ("Historia", "Wyjaśnij przyczyny wybuchu I wojny światowej dla ucznia szkoły podstawowej."),
    ("Historia", "Przygotuj 5 pytań testowych na temat rewolucji francuskiej dla ucznia liceum."),
    ("Historia", "Stwórz krótki materiał dydaktyczny na temat II wojny światowej z zadaniami i odpowiedziami."),
    ("Historia", "Napisz streszczenie najważniejszych wydarzeń związanych z powstaniem Polski w 1918 roku."),

    # --- INFORMATYKA (13-16) ---
    ("Informatyka", "Wyjaśnij czym jest algorytm dla ucznia szkoły podstawowej używając prostego przykładu."),
    ("Informatyka", "Przygotuj 5 pytań testowych na temat podstaw programowania w Pythonie dla ucznia liceum."),
    ("Informatyka", "Stwórz materiał dydaktyczny na temat pętli w programowaniu z przykładami kodu i ćwiczeniami."),
    ("Informatyka", "Napisz krótkie streszczenie na temat sieci komputerowych i internetu dla ucznia szkoły średniej."),

    # --- JĘZYK ANGIELSKI (17-20) ---
    ("Język angielski", "Wyjaśnij różnicę między czasem Present Simple a Present Continuous dla ucznia szkoły podstawowej."),
    ("Język angielski", "Przygotuj 5 ćwiczeń gramatycznych na temat czasu Past Simple dla ucznia gimnazjum z odpowiedziami."),
    ("Język angielski", "Stwórz materiał dydaktyczny na temat słownictwa związanego z pogodą z ćwiczeniami i odpowiedziami."),
    ("Język angielski", "Napisz krótkie streszczenie zasad używania przedimków w języku angielskim dla ucznia liceum."),
=======
# 📌 PROMPTS
# ========================
prompts = [
    "Wyjaśnij czym jest fotosynteza dla ucznia szkoły podstawowej.",
    "Przygotuj zestaw 5 pytań testowych z biologii na temat fotosyntezy dla ucznia liceum.",
    "Stwórz krótki materiał dydaktyczny + 3 zadania + odpowiedzi na temat fotosyntezy.",
    "Wyjaśnij fotosyntezę prostym językiem z przykładem.",
    "Napisz krótkie streszczenie fotosyntezy."
>>>>>>> 326a4aeb9e20a01e932fad65ddc899b0c1e2af5e
]

# ========================
# 💾 SAVE ANSWERS TO FILES
# ========================
os.makedirs("answers", exist_ok=True)

def save_answer(prompt_num, category, prompt_text, model_name, answer):
    safe_name = model_name.replace("/", "_").replace(" ", "_")
    filename = f"answers/prompt_{prompt_num:02d}_{safe_name}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"PROMPT {prompt_num}\n")
        f.write(f"Kategoria: {category}\n")
        f.write(f"Prompt: {prompt_text}\n")
        f.write(f"Model: {model_name}\n")
        f.write("=" * 60 + "\n")
        f.write(answer)

# ========================
# 📊 OCENA - z walidacją
# ========================
def get_scores(model_name):
    print(f"\nOceń {model_name} (1-5)")
    scores = {}
    criteria = [
        ("Poprawność", "poprawnosc"),
        ("Język", "jezyk"),
        ("Poziom", "poziom"),
        ("Przydatność", "przydatnosc"),
    ]
    for display_name, key in criteria:
        while True:
            try:
                val = int(input(f"{display_name}: "))
                if 1 <= val <= 5:
                    scores[key] = val
                    break
                else:
                    print("⚠ Podaj liczbę od 1 do 5!")
            except ValueError:
                print("⚠ Podaj liczbę (1, 2, 3, 4 lub 5), nie tekst!")
    return scores

# ========================
# 💾 CSV - zapis po każdym prompcie
# ========================
def save_to_csv(data, filename="results.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["prompt_num", "category", "model",
                         "poprawnosc", "jezyk", "poziom", "przydatnosc"])
        writer.writerows(data)

# ========================
# 🚀 MAIN LOOP
# ========================
all_results = []
all_answers = {}

print("\n" + "=" * 60)
print("EKSPERYMENT: Ocena jakości treści edukacyjnych LLM")
print("20 promptów × 3 modele = 60 odpowiedzi")
print("=" * 60)

for i, (category, user_prompt) in enumerate(prompts):
    print(f"\n{'=' * 60}")
    print(f"PROMPT {i + 1}/20 | Kategoria: {category}")
    print(f"Prompt: {user_prompt}")
    print("=" * 60)

    print("\n⏳ Generowanie odpowiedzi...")

    out1 = generate_local(model1, tokenizer1, system_prompt, user_prompt)
    out2 = generate_local(model2, tokenizer2, system_prompt, user_prompt)
    out3 = generate_gemini(system_prompt, user_prompt)

    # Zapisz odpowiedzi do plików
    save_answer(i + 1, category, user_prompt, "TinyLlama", out1)
    save_answer(i + 1, category, user_prompt, "Phi-2", out2)
    save_answer(i + 1, category, user_prompt, "Gemini", out3)

    all_answers[i + 1] = {
        "category": category,
        "prompt": user_prompt,
        "TinyLlama": out1,
        "Phi-2": out2,
        "Gemini": out3
    }

    print("\n--- TinyLlama ---")
    print(out1[:400] + ("..." if len(out1) > 400 else ""))
    print("\n--- Phi-2 ---")
    print(out2[:400] + ("..." if len(out2) > 400 else ""))
    print("\n--- Gemini ---")
    if out3 == "ERROR: Gemini not available":
        print("❌ Gemini niedostępny")
    else:
        print(out3[:400] + ("..." if len(out3) > 400 else ""))

    s1 = get_scores("TinyLlama")
    s2 = get_scores("Phi-2")

    if out3 == "ERROR: Gemini not available":
        print("\n⚠ Gemini niedostępny - ocena pominięta (zapisano 0)")
        s3 = {"poprawnosc": 0, "jezyk": 0, "poziom": 0, "przydatnosc": 0}
    else:
        s3 = get_scores("Gemini")

    all_results.append([i + 1, category, "TinyLlama",
                        s1["poprawnosc"], s1["jezyk"], s1["poziom"], s1["przydatnosc"]])
    all_results.append([i + 1, category, "Phi-2",
                        s2["poprawnosc"], s2["jezyk"], s2["poziom"], s2["przydatnosc"]])
    all_results.append([i + 1, category, "Gemini",
                        s3["poprawnosc"], s3["jezyk"], s3["poziom"], s3["przydatnosc"]])

    # Zapisz po każdym prompcie (bezpieczeństwo danych)
    save_to_csv(all_results)
    print(f"\n✅ Prompt {i + 1}/20 zapisany do results.csv!")

# ========================
# 📄 DOKUMENT DLA DRUGIEGO OCENIAJĄCEGO
# ========================
with open("ocena_drugi_oceniajacy.txt", "w", encoding="utf-8") as f:
    f.write("DOKUMENT DLA DRUGIEGO OCENIAJĄCEGO\n")
    f.write("=" * 60 + "\n\n")
    f.write("Instrukcja:\n")
    f.write("Proszę ocenić każdą odpowiedź modelu w skali 1-5:\n")
    f.write("1=bardzo słabe, 2=słabe, 3=średnie, 4=dobre, 5=bardzo dobre\n\n")
    f.write("Kryteria oceny:\n")
    f.write("- Poprawność: czy informacje są merytorycznie poprawne?\n")
    f.write("- Język: czy tekst jest gramatycznie i stylistycznie poprawny?\n")
    f.write("- Poziom: czy trudność jest dopasowana do ucznia?\n")
    f.write("- Przydatność: czy materiał nadaje się do użycia w nauczaniu?\n\n")
    f.write("=" * 60 + "\n\n")

    for prompt_num, data in all_answers.items():
        f.write(f"PROMPT {prompt_num}/20\n")
        f.write(f"Kategoria: {data['category']}\n")
        f.write(f"Zadanie: {data['prompt']}\n\n")

        for model_name in ["TinyLlama", "Phi-2", "Gemini"]:
            answer = data[model_name]
            f.write(f"--- {model_name} ---\n")
            if answer == "ERROR: Gemini not available":
                f.write("[Model niedostępny - nie oceniaj]\n\n")
            else:
                f.write(answer[:800] + ("..." if len(answer) > 800 else "") + "\n\n")
                f.write(f"Ocena {model_name}:\n")
                f.write(f"  Poprawność (1-5): ___\n")
                f.write(f"  Język (1-5): ___\n")
                f.write(f"  Poziom (1-5): ___\n")
                f.write(f"  Przydatność (1-5): ___\n\n")

        f.write("-" * 60 + "\n\n")

print("\n✅ Dokument dla drugiego oceniającego: ocena_drugi_oceniajacy.txt")

# ========================
# 📊 STATYSTYKI
# ========================
avg_scores = collections.defaultdict(lambda: {
    "poprawnosc": [], "jezyk": [], "poziom": [], "przydatnosc": []
})
category_scores = collections.defaultdict(lambda: collections.defaultdict(list))

for row in all_results:
    prompt_num, category, model, p, j, po, pr = row
    if p > 0:  # pomiń oceny 0 (Gemini niedostępny)
        avg_scores[model]["poprawnosc"].append(p)
        avg_scores[model]["jezyk"].append(j)
        avg_scores[model]["poziom"].append(po)
        avg_scores[model]["przydatnosc"].append(pr)
        category_scores[category][model].append((p + j + po + pr) / 4)

print("\n" + "=" * 60)
print("WYNIKI STATYSTYCZNE")
print("=" * 60)

for model in avg_scores:
    print(f"\n{model}:")
    for criterion in ["poprawnosc", "jezyk", "poziom", "przydatnosc"]:
        values = avg_scores[model][criterion]
        if values:
            m = np.mean(values)
            sd = np.std(values, ddof=1) if len(values) > 1 else 0
            print(f"  {criterion}: M={m:.2f} SD={sd:.2f} (n={len(values)})")

    all_vals = []
    for c in ["poprawnosc", "jezyk", "poziom", "przydatnosc"]:
        all_vals.extend(avg_scores[model][c])
    if all_vals:
        print(f"  Ogólna średnia: M={np.mean(all_vals):.2f}")

# ========================
# 📊 TEST KRUSKALA-WALLISA
# ========================
print("\n" + "=" * 60)
print("TEST KRUSKALA-WALLISA")
print("=" * 60)

models_list = list(avg_scores.keys())

for criterion in ["poprawnosc", "jezyk", "poziom", "przydatnosc"]:
    groups = [avg_scores[m][criterion] for m in models_list if avg_scores[m][criterion]]
    if len(groups) >= 2:
        try:
            h_stat, p_val = stats.kruskal(*groups)
            significance = "✅ ISTOTNA (p<0.05)" if p_val < 0.05 else "❌ NIE istotna"
            print(f"\n{criterion}:")
            print(f"  H={h_stat:.3f}, p={p_val:.4f} → {significance}")
        except Exception as e:
            print(f"\n{criterion}: Błąd - {e}")

# ========================
# 📈 WYKRESY
# ========================
models = list(avg_scores.keys())
means = {m: {c: np.mean(avg_scores[m][c]) if avg_scores[m][c] else 0
             for c in ["poprawnosc", "jezyk", "poziom", "przydatnosc"]}
         for m in models}

# Wykres 1 - Liniowy
x = range(len(models))
plt.figure(figsize=(10, 6))
plt.plot(x, [means[m]["poprawnosc"] for m in models], marker='o', linewidth=2, label="Poprawność")
plt.plot(x, [means[m]["jezyk"] for m in models], marker='s', linewidth=2, label="Język")
plt.plot(x, [means[m]["poziom"] for m in models], marker='^', linewidth=2, label="Poziom")
plt.plot(x, [means[m]["przydatnosc"] for m in models], marker='D', linewidth=2, label="Przydatność")
plt.xticks(x, models, fontsize=12)
plt.yticks(range(1, 6))
plt.ylim(0.5, 5.5)
plt.title("Średnia ocena modeli językowych według kryteriów", fontsize=14)
plt.ylabel("Ocena (1-5)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("final_wykres.png", dpi=150)
plt.show()
print("✅ Zapisano: final_wykres.png")

# Wykres 2 - Radarowy
categories_chart = ['Poprawność', 'Język', 'Poziom', 'Przydatność']
N = len(categories_chart)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(1, 1, figsize=(7, 7), subplot_kw=dict(polar=True))
colors = ['#e74c3c', '#f39c12', '#2ecc71']

for idx, model in enumerate(models):
    values = [means[model]["poprawnosc"], means[model]["jezyk"],
              means[model]["poziom"], means[model]["przydatnosc"]]
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, color=colors[idx % len(colors)], label=model)
    ax.fill(angles, values, alpha=0.1, color=colors[idx % len(colors)])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories_chart, size=12)
ax.set_ylim(0, 5)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_title('Porównanie modeli według kryteriów oceny', size=13, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.15), fontsize=11)
plt.tight_layout()
plt.savefig("radar_chart.png", dpi=150, bbox_inches='tight')
plt.show()
print("✅ Zapisano: radar_chart.png")

# Wykres 3 - Słupkowy według kategorii
subject_cats = list(dict.fromkeys(row[1] for row in all_results))
fig, ax = plt.subplots(figsize=(12, 6))
x_cat = np.arange(len(subject_cats))
width = 0.25
colors_bar = ['#e74c3c', '#f39c12', '#2ecc71']

for idx, model in enumerate(models):
    cat_means = []
    for cat in subject_cats:
        cat_vals = [row for row in all_results
                    if row[1] == cat and row[2] == model and row[3] > 0]
        if cat_vals:
            all_s = [(r[3] + r[4] + r[5] + r[6]) / 4 for r in cat_vals]
            cat_means.append(np.mean(all_s))
        else:
            cat_means.append(0)
    ax.bar(x_cat + idx * width, cat_means, width,
           label=model, color=colors_bar[idx % len(colors_bar)], alpha=0.8)

ax.set_xlabel('Kategoria przedmiotowa')
ax.set_ylabel('Średnia ocena (1-5)')
ax.set_title('Porównanie modeli według kategorii przedmiotowej')
ax.set_xticks(x_cat + width)
ax.set_xticklabels(subject_cats, rotation=15, ha='right')
ax.set_ylim(0, 5.5)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig("wykres_kategorie.png", dpi=150)
plt.show()
print("✅ Zapisano: wykres_kategorie.png")

# ========================
<<<<<<< HEAD
# 📊 PODSUMOWANIE KOŃCOWE
# ========================
print("\n" + "=" * 60)
print("PODSUMOWANIE KOŃCOWE")
print("=" * 60)
for m in models:
    all_vals = []
    for c in ["poprawnosc", "jezyk", "poziom", "przydatnosc"]:
        all_vals.extend(avg_scores[m][c])
    if all_vals:
        n = len(avg_scores[m]['poprawnosc'])
        print(f"{m}: M={np.mean(all_vals):.2f} (n={n} promptów)")

print("\n✅ EKSPERYMENT ZAKOŃCZONY!")
print("\nPliki wynikowe:")
print("  📊 results.csv                    - wyniki ocen")
print("  📁 answers/                       - odpowiedzi modeli")
print("  📝 ocena_drugi_oceniajacy.txt     - dla drugiego oceniającego")
print("  📈 final_wykres.png               - wykres liniowy")
print("  📈 radar_chart.png                - wykres radarowy")
print("  📈 wykres_kategorie.png           - wykres według kategorii")
=======
# 📊 PRINT
# ========================
print("\nŚrednie wyniki:")
for m in models:
    print(m, avg_scores[m])
>>>>>>> 326a4aeb9e20a01e932fad65ddc899b0c1e2af5e
