# remove appostrophes and other non-letter characters and
# break apart hyphenated words
def normalise_word(word):
    # Select all the characters that are either letters or hyphen
    select_word = ''.join(c for c in word if c.isalpha() or c.isspace() or c == '-')

    # Break them up into words by splitting them by hyphen and spaces
    new_word = [w.upper() for w in select_word.split('-')]

    return new_word

# convert the last letter of a word to lowercase to know the last letter of each word
def replace_last_word(word):
    last_char = word[-1]
    return word[:-1] + last_char.lower()

# get three character abbreviation from word
def get_three_letter_abbreviations(word):
    abbreviations = []

    # Loop through each character of the word to generate three abbreviations
    for second_letter_index in range(1, len(word)):
        for third_letter_index in range(second_letter_index + 1, len(word)):
            abbreviation = f"{word[0]}{word[second_letter_index]}{word[third_letter_index]}"

            if abbreviation not in abbreviations:
                abbreviations.append(abbreviation)

    return abbreviations

def get_abbreviations_point_from_abbreviation(full_word, abbreviations):
    letter_points = {
        "Q,Z": 1,
        "J,X": 3,
        "K": 6,
        "F,H,V,W,Y": 7,
        "B,C,M,P": 8,
        "D,G": 9,
        "L,N,R,S,T": 15,
        "O,U": 20,
        "A,I": 25,
        "E": 35,
    }

    abbr_points = {}

    for abbr in abbreviations:
        letter_positions = {}
        point = 0

        for i in range(1, len(abbr)):
            current_abbreviation_char = abbr[i]

            if any(word.startswith(current_abbreviation_char) for word in full_word):
                continue

            if current_abbreviation_char.islower():
                if current_abbreviation_char == 'e':
                    point += 20
                else:
                    point += 5
                continue

            for word in full_word:
                index_of_char = word.find(current_abbreviation_char)

                if current_abbreviation_char in letter_positions:
                    if letter_positions[current_abbreviation_char] > 0:
                        letter_positions[current_abbreviation_char] = i
                    else:
                        letter_positions[current_abbreviation_char] = 1
                else:
                    letter_positions[current_abbreviation_char] = index_of_char

                position_in_word = letter_positions[current_abbreviation_char]

                if position_in_word > 0:
                    if position_in_word < 3:
                        point += position_in_word
                    else:
                        point += 3
                    break

            for entry in letter_points:
                if current_abbreviation_char in entry:
                    point += letter_points[entry]

        abbreviation = abbr.upper()
        if abbreviation not in abbr_points:
            abbr_points[abbreviation] = point

    return abbr_points

print(get_abbreviations_point_from_abbreviation(["GLORY"], ['GLO', 'GLR', 'GLY', 'GOR', 'GOY', 'GRY']))