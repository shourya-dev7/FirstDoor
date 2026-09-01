import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def retrieve(query: str, limit: int = 5):
    query_words = set(query.lower().split())

    disease_data = load_json("disease.json")
    diseases = disease_data["conditions"]
    symptoms = load_json("symptoms.json")
    tests = load_json("tests.json")
    relationships = load_json("relationships.json")

    results = []

    for disease in diseases:
        text = " ".join(
            [
                disease.get("name", ""),
                disease.get("specialty", ""),
                *disease.get("symptoms", []),
                *disease.get("tests", [])
            ]
        ).lower()

        score = sum(word in text for word in query_words)

        if score > 0:
            results.append({
                "type": "disease",
                "name": disease["name"],
                "specialty": disease.get("specialty"),
                "score": score,
                "symptoms": disease.get("symptoms", []),
                "tests": disease.get("tests", [])
            })

    for relation in relationships:
        text = (
            f"{relation['source']} "
            f"{relation['relationship']} "
            f"{relation['target']}"
        ).lower()

        score = sum(word in text for word in query_words)

        if score > 0:
            results.append({
                "type": "relationship",
                "source": relation["source"],
                "relationship": relation["relationship"],
                "target": relation["target"],
                "score": score
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:limit]