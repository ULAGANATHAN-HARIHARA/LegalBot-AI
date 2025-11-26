# modules/ai/recommender.py

import re
from difflib import get_close_matches

CRIME_KEYWORDS = {
    "theft": ["steal", "stole", "phone stolen", "rob", "robbed", "snatched"],
    "assault": ["hit", "beat", "attacked", "fight", "violence"],
    "fraud": ["cheat", "fraud", "scam", "fake", "deceive"],
    "harassment": ["harass", "abuse", "threaten", "stalk"],
    "murder": ["kill", "killed", "murdered", "dead", "stabbed"],
}

IPC_MAP = {
    "theft": ["Section 378 – Theft", "Section 379 – Punishment for Theft"],
    "assault": ["Section 351 – Assault", "Section 352 – Punishment for Assault"],
    "fraud": ["Section 415 – Cheating", "Section 420 – Cheating & Dishonesty"],
    "harassment": ["Section 354 – Outrage Modesty", "Section 506 – Criminal Intimidation"],
    "murder": ["Section 299 – Culpable Homicide", "Section 302 – Murder Punishment"],
}


def detect_crime_category(text):
    text = text.lower()

    for crime, keywords in CRIME_KEYWORDS.items():
        for word in keywords:
            if word in text:
                return crime

    # fuzzy fallback
    for crime, keywords in CRIME_KEYWORDS.items():
        if get_close_matches(text, keywords, cutoff=0.4):
            return crime

    return None


def recommend_section(user_query, retriever=None):
    results = []

    # 1️⃣ Semantic FAISS retrieval (if retriever exists)
    if retriever:
        try:
            docs = retriever.invoke(user_query)
            for d in docs:
                results.append(d.page_content)
        except:
            pass

    # 2️⃣ Keyword-based crime detection
    crime = detect_crime_category(user_query)

    if crime and crime in IPC_MAP:
        results += IPC_MAP[crime]

    # 3️⃣ Remove duplicates
    results = list(dict.fromkeys(results))

    return results[:5]  # top 5 only
