# Side Effect Define
def getDefinition(word):
    import requests
    response = requests.get(f"https://dictionaryapi.com/api/v3/references/medical/json/{word}?key=5b4a982a-af04-458a-99fe-ea9acfc9361d")
    for entry in response.json():
        if isinstance(entry, dict):
            meta = entry.get("meta")
            if "shortdef" in entry:
                return('\n'.join(entry['shortdef']))
    return ""

def decimalToPercentage(decimal):
    return "{0:.0%}".format(float(decimal))

def updateDDIResult(ddi_result):
    # Updates probability from decimal to percentage.
    for drug_interaction in ddi_result["drug_interactions"]:
        drug_interaction["probability"] = decimalToPercentage(drug_interaction["probability"])
        drug_interaction["other_drug_name"] = drug_interaction["other_drug_name"].replace("'", "''")

    # Adds definition to side-effect.
    # Ensure side effects are unique.
    side_effects = []
    side_effect_set = set()
    for data in ddi_result["cur_drug_side_effect"]:
        if data["side_effect_name"] in side_effect_set: continue
        side_effect_set.add(data["side_effect_name"])
        data["definition"] = getDefinition(data["side_effect_name"])
        side_effects.append(data)

    ddi_result["cur_drug_side_effect"] = side_effects


def makeUnique(curr_foods, food_interactions):
    res = []
    food_names = set()
    for data in food_interactions:
        if data["food_name"] not in curr_foods: continue
        if data["food_name"] in food_names: continue
        food_names.add(data["food_name"])
        res.append(data)
    return res