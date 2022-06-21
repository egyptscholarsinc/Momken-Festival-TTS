import os

from LTSRules import LetterToSoundRules


input_file_path = os.path.join("cleaned_dictionary_in_arabic.txt")
op_dir = os.path.join("output")
matching_words_file_path = os.path.join(op_dir, "matching_words.txt")
non_matching_words_file_path = os.path.join(op_dir, "non_matching_words.txt")

lts = LetterToSoundRules()
matching_words_count = 0
non_matching_words_count = 0
line_count = 0

with open(input_file_path, 'r', encoding="utf-8") as ip_dict_file:
    with open(matching_words_file_path, 'w', encoding="utf-8") as matching_words_file:
        with open(non_matching_words_file_path, 'w', encoding="utf-8") as non_matching_words_file:
            for line in ip_dict_file:
                line_count += 1
                stripped_line = line.strip()
                word_phones = stripped_line.split(" ")
                if len(word_phones) > 0:
                    word = word_phones[0]
                    phones = word_phones[1:]
                    possible_words = lts.phones_to_word(phones).get_words()
                    words_normalized = map(lambda x: lts.normalize_word(x), possible_words)
                    if word in words_normalized:
                        print(stripped_line, file=matching_words_file)
                        matching_words_count += 1
                    else:
                        print(stripped_line, file=non_matching_words_file)
                        non_matching_words_count += 1
                if line_count % 100 == 0:
                    print(f"Reached line: {line_count}")


print(f"Matching words: {matching_words_count}")
print(f"Non matching words: {non_matching_words_count}")