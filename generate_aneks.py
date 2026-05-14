"""
SKRYPT DO GENEROWANIA ANEKSU
==============================
Ten skrypt automatycznie zbiera wszystkie odpowiedzi modeli
z folderu 'answers/' i tworzy gotowy dokument aneksu.

Uruchomienie: python generate_aneks.py
"""

import os
import re
from pathlib import Path

# ========================
# PROMPTY - opisy
# ========================
prompts_info = {
    1:  {"kategoria": "Biologia",         "prompt": "Wyjaśnij czym jest fotosynteza dla ucznia szkoły podstawowej."},
    2:  {"kategoria": "Biologia",         "prompt": "Przygotuj zestaw 5 pytań testowych z biologii na temat podziału komórki dla ucznia liceum."},
    3:  {"kategoria": "Biologia",         "prompt": "Stwórz krótki materiał dydaktyczny na temat budowy DNA z 3 zadaniami i odpowiedziami."},
    4:  {"kategoria": "Biologia",         "prompt": "Napisz streszczenie procesu oddychania komórkowego dla ucznia szkoły średniej."},
    5:  {"kategoria": "Matematyka",       "prompt": "Wyjaśnij czym jest równanie kwadratowe dla ucznia klasy 8 szkoły podstawowej."},
    6:  {"kategoria": "Matematyka",       "prompt": "Przygotuj 5 zadań z matematyki na temat procentów dla ucznia gimnazjum z odpowiedziami."},
    7:  {"kategoria": "Matematyka",       "prompt": "Stwórz materiał dydaktyczny na temat twierdzenia Pitagorasa z przykładami i ćwiczeniami."},
    8:  {"kategoria": "Matematyka",       "prompt": "Napisz krótkie streszczenie dotyczące funkcji liniowej dla ucznia liceum."},
    9:  {"kategoria": "Historia",         "prompt": "Wyjaśnij przyczyny wybuchu I wojny światowej dla ucznia szkoły podstawowej."},
    10: {"kategoria": "Historia",         "prompt": "Przygotuj 5 pytań testowych na temat rewolucji francuskiej dla ucznia liceum."},
    11: {"kategoria": "Historia",         "prompt": "Stwórz krótki materiał dydaktyczny na temat II wojny światowej z zadaniami i odpowiedziami."},
    12: {"kategoria": "Historia",         "prompt": "Napisz streszczenie najważniejszych wydarzeń związanych z powstaniem Polski w 1918 roku."},
    13: {"kategoria": "Informatyka",      "prompt": "Wyjaśnij czym jest algorytm dla ucznia szkoły podstawowej używając prostego przykładu."},
    14: {"kategoria": "Informatyka",      "prompt": "Przygotuj 5 pytań testowych na temat podstaw programowania w Pythonie dla ucznia liceum."},
    15: {"kategoria": "Informatyka",      "prompt": "Stwórz materiał dydaktyczny na temat pętli w programowaniu z przykładami kodu i ćwiczeniami."},
    16: {"kategoria": "Informatyka",      "prompt": "Napisz krótkie streszczenie na temat sieci komputerowych i internetu dla ucznia szkoły średniej."},
    17: {"kategoria": "Język angielski",  "prompt": "Wyjaśnij różnicę między czasem Present Simple a Present Continuous dla ucznia szkoły podstawowej."},
    18: {"kategoria": "Język angielski",  "prompt": "Przygotuj 5 ćwiczeń gramatycznych na temat czasu Past Simple dla ucznia gimnazjum z odpowiedziami."},
    19: {"kategoria": "Język angielski",  "prompt": "Stwórz materiał dydaktyczny na temat słownictwa związanego z pogodą z ćwiczeniami i odpowiedziami."},
    20: {"kategoria": "Język angielski",  "prompt": "Napisz krótkie streszczenie zasad używania przedimków w języku angielskim dla ucznia liceum."},
}

models = ["TinyLlama", "Phi-2", "Gemini"]

# ========================
# WCZYTAJ ODPOWIEDZI
# ========================
def read_answer(prompt_num, model_name):
    """Wczytaj odpowiedź modelu z pliku"""
    answers_dir = Path("answers")
    safe_name = model_name.replace("/", "_").replace(" ", "_")
    filename = answers_dir / f"prompt_{prompt_num:02d}_{safe_name}.txt"

    if filename.exists():
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            # Pomijamy nagłówek pliku (pierwsze 5 linii)
            lines = content.split("\n")
            # Znajdź separator ====
            for i, line in enumerate(lines):
                if "=" * 10 in line:
                    return "\n".join(lines[i+1:]).strip()
            return content.strip()
    else:
        return "[Odpowiedź niedostępna — plik nie znaleziony]"

# ========================
# GENERUJ ANEKS
# ========================
output_file = "ZALACZNIK_1_pelne_odpowiedzi.txt"

with open(output_file, "w", encoding="utf-8") as f:

    # Nagłówek
    f.write("=" * 70 + "\n")
    f.write("ZAŁĄCZNIK 1\n")
    f.write("PEŁNE ODPOWIEDZI MODELI JĘZYKOWYCH\n")
    f.write("=" * 70 + "\n\n")

    f.write("Niniejszy załącznik zawiera pełne odpowiedzi trzech modeli językowych\n")
    f.write("(TinyLlama, Phi-2, Gemini) na 20 identycznych promptów edukacyjnych\n")
    f.write("zastosowanych w eksperymencie porównawczym.\n\n")

    f.write("Modele:\n")
    f.write("  - TinyLlama 1.1B-Chat-v1.0 (model lokalny, HuggingFace)\n")
    f.write("  - Phi-2 microsoft/phi-2 (model lokalny, HuggingFace)\n")
    f.write("  - Gemini 2.5 Flash (API Google)\n\n")

    f.write("Prompt systemowy zastosowany dla wszystkich modeli:\n")
    f.write('"Jesteś doświadczonym nauczycielem z wieloletnią praktyką dydaktyczną.\n')
    f.write('Twoim zadaniem jest tworzenie wysokiej jakości materiałów edukacyjnych\n')
    f.write('dostosowanych do poziomu ucznia. Dbaj o poprawność merytoryczną,\n')
    f.write('używaj prostego języka, podawaj przykłady i zachowuj logiczną strukturę."\n\n')

    f.write("Źródło: dane własne z eksperymentu\n")
    f.write("=" * 70 + "\n\n")

    # Odpowiedzi per prompt
    for prompt_num in range(1, 21):
        info = prompts_info[prompt_num]

        f.write(f"{'=' * 70}\n")
        f.write(f"PROMPT {prompt_num}/20\n")
        f.write(f"Kategoria: {info['kategoria']}\n")
        f.write(f"Treść promptu: {info['prompt']}\n")
        f.write(f"{'=' * 70}\n\n")

        for model in models:
            f.write(f"{'─' * 50}\n")
            f.write(f"Model: {model}\n")
            f.write(f"{'─' * 50}\n")

            answer = read_answer(prompt_num, model)

            if "niedostępna" in answer.lower() or "not available" in answer.lower() or "ERROR" in answer:
                f.write("[Model niedostępny podczas generowania — błąd API]\n")
            else:
                f.write(answer)

            f.write("\n\n")

        f.write("\n")

    # Stopka
    f.write("=" * 70 + "\n")
    f.write("KONIEC ZAŁĄCZNIKA 1\n")
    f.write("Źródło: dane własne z eksperymentu\n")
    f.write("=" * 70 + "\n")

print(f"✅ Aneks wygenerowany: {output_file}")
print(f"   Sprawdź plik i wstaw go do pracy magisterskiej jako Załącznik 1.")