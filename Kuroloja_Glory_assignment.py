from collections import defaultdict

# remove appostrophes and other non-letter characters and
# break apart hyphenated words
def normalise_word(word):
    # Select all the characters that are either letters or hyphen
    select_word = ''.join(c for c in word if c.isalpha() or c.isspace() or c == '-')
    
    # Break them up into words by splitting them by hyphen and spaces
    new_word = select_word.split()

    result_array = [sub_str.upper() for s in new_word for sub_str in s.split('-')]

    #result_string = [w.upper() for w in select_word.split('-')]
    return result_array

# convert the last letter of a word to lowercase to identify the last letter of each word
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

# get total abreviation value using the letter point
def get_abbreviations_point_from_abbreviation(input_words, abbreviations, letter_points: dict):
    result_abbreviation_point = {}

    for abbr in abbreviations:
        # declare a dictionary that stores the position of char of abbreviation in each word
        letter_positions = {}
        point = 0

        for i in range(1, len(abbr)):
            current_abbreviation_char = abbr[i]

            # go to the next iteration if the current_abbreviation chararcter starts any of the words
            if any(word.startswith(current_abbreviation_char) for word in input_words):
                continue
            
            # if the character is lower, that means it is the last letter of a word, so
            if current_abbreviation_char.islower():
                # check if it is letter e
                if current_abbreviation_char == 'e':
                    point += 20
                # or another letter
                else:
                    point += 5
                    # then go to the next iteration
                continue

            for word in input_words:
                # find the index of the current abbreviation in the each word
                index_of_char = word.find(current_abbreviation_char)

                # add the position of the abbreviation char in the word
                if current_abbreviation_char in letter_positions:
                        letter_positions[current_abbreviation_char] = i
                else:
                    letter_positions[current_abbreviation_char] = index_of_char

                position_in_word = letter_positions[current_abbreviation_char]

                if position_in_word > 0:
                    if position_in_word < 3:
                        point += position_in_word
                    else:
                        point += 3
                    break

            point = add_alphabet_values_to_point(point, current_abbreviation_char, letter_points)

        # convert abbrevation to upper case
        abbreviation = abbr.upper()
        # add distinct abbreviation and their points to the result point
        if abbreviation not in result_abbreviation_point:
            result_abbreviation_point[abbreviation] = point

    return result_abbreviation_point


def add_alphabet_values_to_point(point: int, abbreviation_char, letter_points: dict) -> int:
    for entry in letter_points:
        if abbreviation_char in entry:
            point += letter_points[entry]
    return point

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file

# import values.txt and convert to dictionary
def read_alphabet_values_to_dictionary(file_path):
    delimiter = ' '
    file_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = map(str.strip, line.split(delimiter,1))
            file_dict[key] = int(value)
    return file_dict

# import the text file and convert to array
def read_tree_names_to_string_array(file_path):
    with open(file_path, 'r') as file:
        array_file = file.read().splitlines()
        return array_file

# select abbreviation with the minimum total value    
def get_best_value(abbreviation_result):
    # List to store distinct results
    distinct_result = []

    # Check for distinct result based on content
    for d in abbreviation_result:
        if d not in distinct_result:
            distinct_result.append(d)

    #get minimum result point
    min_value = min(distinct_result, key=lambda x: x[1])[1]
    best_per_value = [abbr_result for abbr_result in distinct_result if abbr_result[1] == min_value]
    return best_per_value

def main():
    file_name = str(input("what is your file name? "))
    output_file_name = f'kuroloja_{file_name}_abbrevs.txt'
    output_text = ""
     # read value point
    letter_value_points = read_alphabet_values_to_dictionary("values.txt")
    # import the tree names
    input_file_values = read_tree_names_to_string_array(file_name + ".txt")
    for input_name in input_file_values:
        # clean up each word
        normalised_words = []
        abbreviation_result = []
        abbreviations = defaultdict(int) # use default dict to access possible inexistent dictionary key without throwing error/exception
        normalised_words.extend(normalise_word(input_name))
        name_in_sequence = ''
        for normalised_word in normalised_words:
            word_name = replace_last_word(normalised_word)
            name_in_sequence += word_name
            three_char_abbreviations = get_three_letter_abbreviations(name_in_sequence)
            abbreviation_points = get_abbreviations_point_from_abbreviation(normalised_words, three_char_abbreviations, letter_value_points)
            for key, value in abbreviation_points.items():
                if key not in abbreviations:
                    abbreviations[key] = value
            abbreviation_result.extend(abbreviations.items())
        
        output_text += input_name + "\n"
        if not abbreviation_result:
            output_text += "\n\n"
        else:
            best_per_value = get_best_value(abbreviation_result)
            for best in best_per_value:
                output_text += best[0] + " "
        output_text += "\n"
    with open(output_file_name, 'w') as file:
        file.write(output_text)

if __name__ == "__main__":
    main()
