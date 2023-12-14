def main():
    names = ["Small-leaved", "Lime"]
    cleaned_names = []
    result = {}

    for element in names:
        normalized_names = normalize_word(element)
        cleaned_names.extend(normalized_names)

    input_word = ""
    for name in cleaned_names:
        name_to_use = replace_last_word(name)
        input_word += name_to_use

        abbrs = get_my_abbreviations(input_word)
        best_per_word = min(get_abbreviation_point_from_abbreviation(cleaned_names, abbrs).items(), key=lambda x: x[1])

        if best_per_word not in result.items():
            result[best_per_word[0]] = best_per_word[1]