from collections import Counter
from typing import Dict, Any, List
from ..crypto.utils import sanitize_text
from .corpora import (
    FREQ_INDONESIAN, FREQ_ENGLISH,
    COMMON_BIGRAMS_ID, COMMON_BIGRAMS_EN,
    COMMON_TRIGRAMS_ID, COMMON_TRIGRAMS_EN
)

def compute_index_of_coincidence(text: str) -> float:
    n = len(text)
    if n <= 1:
        return 0.0
    counts = Counter(text)
    numerator = sum(f * (f - 1) for f in counts.values())
    denominator = n * (n - 1)
    return round(numerator / denominator, 4)

def analyze_frequency(ciphertext: str, language: str = "id") -> Dict[str, Any]:
    clean_c = sanitize_text(ciphertext)
    n = len(clean_c)

    if n == 0:
        return {
            "total_chars": 0,
            "ioc": 0.0,
            "unigram_frequencies": [],
            "top_bigrams": [],
            "top_trigrams": [],
            "reference_language": language
        }

    ioc = compute_index_of_coincidence(clean_c)
    counts = Counter(clean_c)

    # Reference frequency table
    ref_freq = FREQ_INDONESIAN if language.lower() == "id" else FREQ_ENGLISH

    # Build 26-letter unigram distribution
    unigram_list: List[Dict[str, Any]] = []
    for char_code in range(ord('A'), ord('Z') + 1):
        ch = chr(char_code)
        count = counts.get(ch, 0)
        percentage = round((count / n) * 100, 2)
        expected_percentage = ref_freq.get(ch, 0.0)
        unigram_list.append({
            "letter": ch,
            "count": count,
            "percentage": percentage,
            "expected_percentage": expected_percentage,
            "diff": round(percentage - expected_percentage, 2)
        })

    # Sort descending by observed count
    sorted_unigrams = sorted(unigram_list, key=lambda x: x["count"], reverse=True)

    # Bigrams
    bigrams = [clean_c[i:i+2] for i in range(n - 1)]
    bigram_counts = Counter(bigrams)
    top_bigrams = [
        {"ngram": bg, "count": cnt, "percentage": round((cnt / len(bigrams)) * 100, 2) if bigrams else 0}
        for bg, cnt in bigram_counts.most_common(12)
    ]

    # Trigrams
    trigrams = [clean_c[i:i+3] for i in range(n - 2)]
    trigram_counts = Counter(trigrams)
    top_trigrams = [
        {"ngram": tg, "count": cnt, "percentage": round((cnt / len(trigrams)) * 100, 2) if trigrams else 0}
        for tg, cnt in trigram_counts.most_common(12)
    ]

    # Interpretation of IoC
    ioc_note = ""
    if ioc >= 0.060:
        ioc_note = "Nilai IoC tinggi (~0.06 - 0.08), mengindikasikan kuat cipher abjad-tunggal (Monoalphabetic Substitution)."
    elif ioc >= 0.045:
        ioc_note = "Nilai IoC menengah, kemungkinan cipher abjad-tunggal dengan teks pendek atau polialfabetik periode panjang."
    else:
        ioc_note = "Nilai IoC rendah (~0.038), mendekati distribusi acak atau cipher polialfabetik (seperti Vigenere)."

    return {
        "total_chars": n,
        "ioc": ioc,
        "ioc_note": ioc_note,
        "language": language.upper(),
        "unigrams": unigram_list,
        "sorted_unigrams": sorted_unigrams,
        "top_bigrams": top_bigrams,
        "top_trigrams": top_trigrams,
        "reference_bigrams": COMMON_BIGRAMS_ID if language.lower() == "id" else COMMON_BIGRAMS_EN,
        "reference_trigrams": COMMON_TRIGRAMS_ID if language.lower() == "id" else COMMON_TRIGRAMS_EN
    }
