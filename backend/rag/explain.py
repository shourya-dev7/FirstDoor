def explain_results(results):
    """
    Convert RAG retrieval results into a simple explanation
    for the FirstDoor prototype.
    """

    if not results:
        return {
            "message": "No closely matching conditions were found.",
            "conditions": [],
            "specialists": []
        }

    conditions = []
    specialists = []

    for result in results:
        name = result.get("name", "Unknown condition")
        specialty = result.get("specialty", "General Medicine")
        symptoms = result.get("symptoms", [])
        tests = result.get("tests", [])

        conditions.append({
            "name": name,
            "matching_symptoms": symptoms,
            "possible_tests": tests
        })

        if specialty not in specialists:
            specialists.append(specialty)

    return {
        "message": "These are possible matches based on the symptoms provided. This is not a diagnosis.",
        "conditions": conditions,
        "specialists": specialists
    }