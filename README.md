# 📊 LLM Comparison for Educational Content Generation

## 📌 Opis projektu

Projekt został zrealizowany w ramach pracy magisterskiej pt.:

**„Wykorzystanie dużych modeli językowych (LLM) do generowania treści edukacyjnych”**

Celem projektu jest porównanie jakości generowanych materiałów edukacyjnych przez różne modele językowe.

---

## 🤖 Wykorzystane modele

W projekcie wykorzystano trzy modele:

- **TinyLlama (lokalny)**
- **Phi-2 (lokalny)**
- **Gemini (API Google)**

---

## 🎯 Cel badań

Porównanie modeli pod względem:

- poprawności merytorycznej
- jakości języka
- dopasowania poziomu do ucznia
- przydatności dydaktycznej

---

## 🧪 Metodologia

1. Zdefiniowano **główny prompt (systemowy)**:
   - model pełni rolę nauczyciela
   - generuje materiały edukacyjne

2. Przygotowano zestaw **6 promptów testowych**, np.:
   - wyjaśnienie pojęcia
   - pytania testowe
   - materiał dydaktyczny
   - zadania
   - streszczenie

3. Każdy model generował odpowiedzi

4. Odpowiedzi były oceniane w skali 1–5 według kryteriów:
   - poprawność
   - język
   - poziom
   - przydatność

---

## 📊 Wyniki

Średnie oceny modeli:

- **TinyLlama**: 1.0
- **Phi-2**: ~1.2
- **Gemini**: 5.0

📈 Wyniki pokazują wyraźną przewagę modelu Gemini w generowaniu treści edukacyjnych.

---

## 📉 Wizualizacja

Projekt generuje wykres porównawczy:

![Wykres](final_wykres.png)

---

## ⚙️ Technologie

- Python
- Transformers (HuggingFace)
- Google Gemini API
- Matplotlib
- CSV

---

## 🚀 Jak uruchomić

1. Zainstaluj wymagania:

```bash
pip install torch transformers matplotlib python-dotenv google-genai
