import torch
import csv
import os
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM
from google import genai
import collections
from dotenv import load_dotenv
import os

load_dotenv()

# ========================
# 🔑 CONFIG
# ========================
MODEL_1_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MODEL_2_NAME = "microsoft/phi-2"
GEMINI_API_KEY = "AIzaSyAoqY7uIKY9peK2ZEUrpw0Yb-hw_sL5TTY"

# ========================
# 🔹 GEMINI (NEW API)
# ========================
client = genai.Client(api_key=GEMINI_API_KEY)

# ========================
# 🔹 LOAD LOCAL MODELS
# ========================
print("Loading models...")

tokenizer1 = AutoTokenizer.from_pretrained(MODEL_1_NAME)
model1 = AutoModelForCausalLM.from_pretrained(MODEL_1_NAME)

tokenizer2 = AutoTokenizer.from_pretrained(MODEL_2_NAME)
model2 = AutoModelForCausalLM.from_pretrained(MODEL_2_NAME)

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
# 🔹 GENERATE GEMINI (FIXED)
# ========================
def generate_gemini(system_prompt, user_prompt):
    prompt = f"{system_prompt}\n\n{user_prompt}"

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text

# ========================
# 📌 SYSTEM PROMPT
# ========================
system_prompt = """Jesteś doświadczonym nauczycielem z wieloletnią praktyką dydaktyczną.
Twoim zadaniem jest tworzenie wysokiej jakości materiałów edukacyjnych dostosowanych do poziomu ucznia.

Dbaj o poprawność merytoryczną, używaj prostego języka, podawaj przykłady i zachowuj logiczną strukturę."""

# ========================
# 📌 PROMPTS (6)
# ========================
prompts = [
    "Wyjaśnij czym jest fotosynteza dla ucznia szkoły podstawowej.",
    "Przygotuj zestaw 5 pytań testowych z biologii na temat fotosyntezy dla ucznia liceum.",
    "Stwórz krótki materiał dydaktyczny + 3 zadania + odpowiedzi na temat fotosyntezy.",
    "Wyjaśnij fotosyntezę prostym językiem z przykładem.",
    "Stwórz zadania edukacyjne z fotosyntezy.",
    "Napisz krótkie streszczenie fotosyntezy."
]

# ========================
# 📊 OCENA
# ========================
def get_scores(model_name):
    print(f"\nOceń {model_name} (1-5)")
    return {
        "poprawnosc": int(input("Poprawność: ")),
        "jezyk": int(input("Język: ")),
        "poziom": int(input("Poziom: ")),
        "przydatnosc": int(input("Przydatność: "))
    }

# ========================
# 💾 CSV
# ========================
def save_to_csv(data, filename="results.csv"):
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["prompt", "model", "poprawnosc", "jezyk", "poziom", "przydatnosc"])

        writer.writerows(data)

# ========================
# 🚀 MAIN LOOP
# ========================
all_results = []

for i, user_prompt in enumerate(prompts):
    print(f"\n===== PROMPT {i+1} =====")
    print(user_prompt)

    out1 = generate_local(model1, tokenizer1, system_prompt, user_prompt)
    out2 = generate_local(model2, tokenizer2, system_prompt, user_prompt)
    out3 = generate_gemini(system_prompt, user_prompt)

    print("\n--- TinyLlama ---\n", out1)
    print("\n--- Phi-2 ---\n", out2)
    print("\n--- Gemini ---\n", out3)

    s1 = get_scores("TinyLlama")
    s2 = get_scores("Phi-2")
    s3 = get_scores("Gemini")

    all_results.append([i+1, "TinyLlama", *s1.values()])
    all_results.append([i+1, "Phi-2", *s2.values()])
    all_results.append([i+1, "Gemini", *s3.values()])

# ========================
# 💾 SAVE
# ========================
save_to_csv(all_results)

# ========================
# 📊 ŚREDNIE
# ========================
avg_scores = collections.defaultdict(lambda: {"poprawnosc":0,"jezyk":0,"poziom":0,"przydatnosc":0,"count":0})

for row in all_results:
    _, model, p, j, po, pr = row
    avg_scores[model]["poprawnosc"] += p
    avg_scores[model]["jezyk"] += j
    avg_scores[model]["poziom"] += po
    avg_scores[model]["przydatnosc"] += pr
    avg_scores[model]["count"] += 1

for model in avg_scores:
    for k in ["poprawnosc","jezyk","poziom","przydatnosc"]:
        avg_scores[model][k] /= avg_scores[model]["count"]

# ========================
# 📈 WYKRES
# ========================
models = list(avg_scores.keys())

poprawnosc = [avg_scores[m]["poprawnosc"] for m in models]
jezyk = [avg_scores[m]["jezyk"] for m in models]
poziom = [avg_scores[m]["poziom"] for m in models]
przydatnosc = [avg_scores[m]["przydatnosc"] for m in models]

x = range(len(models))

plt.figure()
plt.plot(x, poprawnosc, marker='o', label="Poprawność")
plt.plot(x, jezyk, marker='o', label="Język")
plt.plot(x, poziom, marker='o', label="Poziom")
plt.plot(x, przydatnosc, marker='o', label="Przydatność")

plt.xticks(x, models)
plt.title("Średnia ocena modeli")
plt.legend()

plt.savefig("final_wykres.png")
plt.show()

# ========================
# 📊 PRINT AVG
# ========================
def avg(scores):
    return (scores["poprawnosc"] + scores["jezyk"] + scores["poziom"] + scores["przydatnosc"]) / 4

print("\nŚrednia ocena modeli:")
for m in models:
    print(m, ":", avg_scores[m])