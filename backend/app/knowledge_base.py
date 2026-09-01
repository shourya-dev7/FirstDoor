# =========================================================
# FIRSTDOOR MEDICAL KNOWLEDGE BASE
# =========================================================

import json
from pathlib import Path


# =========================================================
# DATA DIRECTORY
# =========================================================

DATA_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
)


# =========================================================
# JSON LOADER
# =========================================================

def load_json(filename):
    """
    Load a JSON file from the FirstDoor data directory.
    """

    file_path = DATA_DIR / filename

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# =========================================================
# LOAD MEDICAL DATA
# =========================================================

DISEASE_DATA = load_json(
    "disease.json"
)

TREATMENTS_DATA = load_json(
    "medication.json"
)

RELATIONSHIPS_DATA = load_json(
    "relationships.json"
)

SPECIALTIES_DATA = load_json(
    "specialities.json"
)

SYMPTOMS_DATA = load_json(
    "symptoms.json"
)

LABORATORY_TESTS_DATA = load_json(
    "tests.json"
)


# =========================================================
# EXTRACT CONDITIONS FROM DISEASE DATA
# =========================================================

if isinstance(
    DISEASE_DATA,
    dict
):

    CONDITIONS_DATA = DISEASE_DATA.get(
        "conditions",
        []
    )

else:

    CONDITIONS_DATA = []


# =========================================================
# VALIDATE DATA TYPES
# =========================================================

if not isinstance(
    CONDITIONS_DATA,
    list
):

    CONDITIONS_DATA = []


if not isinstance(
    TREATMENTS_DATA,
    (list, dict)
):

    TREATMENTS_DATA = []


if not isinstance(
    RELATIONSHIPS_DATA,
    (list, dict)
):

    RELATIONSHIPS_DATA = []


if not isinstance(
    SPECIALTIES_DATA,
    (list, dict)
):

    SPECIALTIES_DATA = []


if not isinstance(
    SYMPTOMS_DATA,
    (list, dict)
):

    SYMPTOMS_DATA = []


if not isinstance(
    LABORATORY_TESTS_DATA,
    (list, dict)
):

    LABORATORY_TESTS_DATA = []


# =========================================================
# BUILD SYMPTOM KNOWLEDGE BASE
# =========================================================

KNOWLEDGE_BASE = {}


for condition in CONDITIONS_DATA:

    if not isinstance(
        condition,
        dict
    ):

        continue


    # -----------------------------------------------------
    # CONDITION NAME
    # -----------------------------------------------------

    condition_name = str(
        condition.get(
            "name",
            ""
        )
    ).strip()


    # -----------------------------------------------------
    # SYMPTOMS
    # -----------------------------------------------------

    condition_symptoms = condition.get(
        "symptoms",
        []
    )


    if not isinstance(
        condition_symptoms,
        list
    ):

        continue


    # -----------------------------------------------------
    # SPECIALTY
    # -----------------------------------------------------

    specialty = condition.get(
        "specialty"
    )


    if specialty:

        specialty = str(
            specialty
        ).strip()


    # -----------------------------------------------------
    # COMMON TESTS
    # -----------------------------------------------------

    common_tests = condition.get(
        "common_tests",
        []
    )


    if not isinstance(
        common_tests,
        list
    ):

        common_tests = []


    # -----------------------------------------------------
    # ADD EACH SYMPTOM TO KNOWLEDGE BASE
    # -----------------------------------------------------

    for symptom in condition_symptoms:

        symptom = str(
            symptom
        ).strip().lower()


        if not symptom:

            continue


        # -------------------------------------------------
        # CREATE SYMPTOM ENTRY
        # -------------------------------------------------

        if symptom not in KNOWLEDGE_BASE:

            KNOWLEDGE_BASE[symptom] = {

                "conditions": [],

                "tests": [],

                "specialty": specialty,

                "red_flags": [],
            }


        # -------------------------------------------------
        # ADD CONDITION
        # -------------------------------------------------

        if (
            condition_name
            and condition_name
            not in KNOWLEDGE_BASE[
                symptom
            ]["conditions"]
        ):

            KNOWLEDGE_BASE[
                symptom
            ]["conditions"].append(
                condition_name
            )


        # -------------------------------------------------
        # ADD COMMON TESTS
        # -------------------------------------------------

        for test in common_tests:

            test = str(
                test
            ).strip()


            if (
                test
                and test
                not in KNOWLEDGE_BASE[
                    symptom
                ]["tests"]
            ):

                KNOWLEDGE_BASE[
                    symptom
                ]["tests"].append(
                    test
                )


        # -------------------------------------------------
        # ADD SPECIALTY
        # -------------------------------------------------

        if (
            not KNOWLEDGE_BASE[
                symptom
            ].get("specialty")
            and specialty
        ):

            KNOWLEDGE_BASE[
                symptom
            ]["specialty"] = specialty


# =========================================================
# SPECIALTY PRIORITY
# =========================================================

SPECIALTY_PRIORITY = {

    "Cardiology": 5,

    "Neurology": 5,

    "Pulmonology": 5,

    "Gastroenterology": 4,

    "Endocrinology": 4,

    "General Medicine": 1,
}


# =========================================================
# MEDICAL HISTORY
# =========================================================

MEDICAL_HISTORY = {

    "diabetes": {

        "associated_conditions": [

            "Diabetes mellitus",

            "Diabetes-related complications",

        ],

        "recommended_tests": [

            "Blood glucose",

            "HbA1c",

        ],
    },


    "high blood pressure": {

        "associated_conditions": [

            "Hypertension",

            "Cardiovascular risk",

            "Cerebrovascular risk",

        ],

        "recommended_tests": [

            "Blood pressure measurement",

            "Blood tests",

            "ECG",

        ],
    },


    "heart disease": {

        "associated_conditions": [

            "Cardiovascular disease",

            "Cardiovascular condition",

        ],

        "recommended_tests": [

            "ECG",

            "Blood tests",

            "Cardiac evaluation",

        ],
    },


    "asthma": {

        "associated_conditions": [

            "Asthma",

            "Asthma-related condition",

            "Respiratory condition",

        ],

        "recommended_tests": [

            "Pulmonary function testing",

            "Spirometry",

            "Pulse oximetry",

        ],
    },


    "previous stroke": {

        "associated_conditions": [

            "Neurological disorder",

            "Cerebrovascular risk",

            "Neurological condition",

        ],

        "recommended_tests": [

            "Neurological examination",

            "Brain imaging",

        ],
    },
}


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_symptom_information(
    symptom: str
):
    """
    Return medical knowledge associated
    with a specific symptom.
    """

    symptom = str(
        symptom
    ).lower().strip()


    return KNOWLEDGE_BASE.get(
        symptom,
        {
            "conditions": [],

            "tests": [],

            "specialty": None,

            "red_flags": [],
        },
    )


def get_history_information(
    history: str
):
    """
    Return medical knowledge associated
    with a patient's medical history.
    """

    history = str(
        history
    ).lower().strip()


    return MEDICAL_HISTORY.get(
        history,
        {
            "associated_conditions": [],

            "recommended_tests": [],
        },
    )