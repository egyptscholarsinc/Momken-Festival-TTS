from typing import List, Tuple
import re

class ArNode:
    def __init__(self, content:str) -> None:
        self.content = content
        self.children:List[ArNode] = []
    def append_node(self, node):
        self.children.append(node)
        return self
    def get_words(self):
        words = []
        if len(self.children) == 0:
            words.append(self.content)
        else:
            for child in self.children:
                child_words = child.get_words()
                for child_word in child_words:
                    words.append(self.content + child_word)
        return words





class Rule:
    def __init__(self, rule_tuple:Tuple[List[str], List[str], List[str], List[str]]) -> None:
        self.left_context, self.replacable_context, self.right_context, self.op_phones = rule_tuple
    
    def reverse_apply(self, phones:List[str], start_position:int):
        for char in self.op_phones:
            if start_position >= len(phones) or char != phones[start_position]:
                return None, None
            else:
                start_position += 1
        node = ArNode("".join(self.left_context + self.replacable_context +self.right_context))
        return (node, start_position)

    def apply_to(self, word:List[str], left_context_start_poosition:int):
        start_position  = left_context_start_poosition
        removed_indices = []
        for char in self.left_context:
            if start_position >= len(word) or char != word[start_position]:
                return None, None
            else:
                start_position += 1
        for char in self.replacable_context:
            if start_position >= len(word) or char != word[start_position]:
                return None, None
            else:
                removed_indices.append(start_position)
                start_position += 1
        for char in self.right_context:
            if start_position >= len(word) or char != word[start_position]:
                return None, None
            else:
                start_position += 1
        letters_indices = list(enumerate(word))
        new_word = [letter[1] for letter in letters_indices if letter[0] not in removed_indices]
        return self.op_phones, new_word


class LetterToSoundRules:
    def __init__(self) -> None:
        self.allowables()
        self.define_rules()

    def allowables(self):
        self.allowable_letters = set([
            "ا", "آ", "ج", "ث", "ڤ", "ظ", "ى", "أ", "ؤ", "ر", "ط", "ه", "ق",
            "ئ", "ف", "ٱ", "ن", "ص", "ض", "إ", "ت", "خ", "ل", "غ", "ي", "ح",
            "ك", "س", "ذ", "ش", "ب", "ز", "ع", "ء", "م", "د", "ة", "و"
        ])
        self.allowable_phones = set([
                "$" , "A" , "n" , "t" , "w" , "m" , "l" , "q" , "y" , "p" , "i" , "a" ,
                "h" , "u" , "r" , "E" , "G" , "k" , "V" , "b" , "f" , "Z" , "s" , "x" ,
                "d" , "z" , "H" , "T" , "S" , "j" , "g" , "v" , "D" , "I" , "U"
            ])
        self.diacritic_regex = re.compile('[\u064B-\u0650]')
    def word_to_phones(self, word:List[str]) -> List[str]:
        phones = []
        if len(word) == 0:
            return phones
        for rule in self.rules:
            result_phones, new_word = rule.apply_to(word, 0)
            if result_phones is not None:
                phones.extend(result_phones)
                phones.extend(self.word_to_phones(new_word))
                return phones
        return phones

    
    def phones_to_word(self, phones:List[str]) -> ArNode:
        if len(phones) == 0:
            return ArNode("")
        words = ArNode("")
        for rule in self.rules:
            result_letters, new_begin = rule.reverse_apply(phones, 0)
            if result_letters:
                result_letters.append_node(self.phones_to_word(phones[new_begin:]))
                words.append_node(result_letters)
        return words

    def normalize_word(self, word:str):
        return re.sub(self.diacritic_regex, "", word)
        
    def define_rules(self):
        self.rules = [
            Rule(([], ['\u064f', 'و', "ا"], [], ['U'])),   # 064c dammatan  ُُ
            Rule(([], ['\u064f', 'و'], [], ['U'])),   # 064c dammatan  ُُ
            Rule(([], ['\u064E', 'ا'], [], ['A'])),   # 064c dammatan  ُُ
            Rule(([], ['\u0650', 'ي'], [], ['y'])),   # 064c dammatan  ُُ
            Rule(([], ['\u064c'], [], ["u", "n"])),   # 064c dammatan  ُُ
            Rule(([], ['\u064f', '\u064f'], [], ["u", "n"])),   # double damma
            Rule(([], ['ا', '\u064B'], [], ["a", "n"])),   # 064E Fathatan   ً
            Rule(([], ['\u064B'], [], ["a", "n"])),   # 064E Fathatan   ً
            Rule(([], ['\u064E', '\u064E'], [], ["a", "n"])),   # double Fatha
            Rule(([], ['\u064D'], [], ["i", "n"])),   # 064D Kasratan  ٍ
            Rule(([], ['\u0650', '\u0650'], [], ["i", "n"])),   # double kasra  ٍ
            Rule(([], ['\u064f'], [], ["u"])),   # 064f damma  ُ
            Rule(([], ['\u064E'], [], ["a"])),   # 064E Fatha  َ
            Rule(([], ['\u0650'], [], ["i"])),   # 064E Kasra  ِ
            Rule(([], ["ا", "ل", "ش"], [], ["A", "$"])), # TO DO add word boundaries
            Rule(([], ["ا", "ل", "ش"], [], ["A", "$"])), # TO DO add word boundaries
            Rule(( [], ['ش'], [], ['$'] )),
            Rule(( [], ['ا'], [], ['A'] )),
            Rule(( [], ['ن'], [], ['n'] )),
            Rule(( [], ['ت'], [], ['t'] )),
            Rule(( [], ['و'], [], ['w'] )),
            Rule(( [], ['م'], [], ['m'] )),
            Rule(( [], ['ل'], [], ['l'] )),
            Rule(( [], ['ق'], [], ['q'] )),
            Rule(( [], ['ي'], [], ['y'] )),
            Rule(( [], ['ة'], [], ['p'] )), #check
            Rule(( [], ['ة'], [], ['t'] )), #check
            Rule(( [], ['ة'], [], ['h'] )), #check
            Rule(( [], ['ه'], [], ['h'] )),
            Rule(( [], ['ر'], [], ['r'] )),
            Rule(( [], ['ع'], [], ['E'] )),
            Rule(( [], ['ء'], [], ['G'] )),
            Rule(( [], ['أ'], [], ['G'] )),
            Rule(( [], ['إ'], [], ['G'] )),
            Rule(( [], ['ؤ'], [], ['G'] )),
            Rule(( [], ['ئ'], [], ['G'] )),
            Rule(( [], ['ك'], [], ['k'] )),
            Rule(( [], ['ذ'], [], ['V'] )),
            Rule(( [], ['ب'], [], ['b'] )),
            Rule(( [], ['ف'], [], ['f'] )),
            Rule(( [], ['ظ'], [], ['Z'] )),
            Rule(( [], ['س'], [], ['s'] )),
            Rule(( [], ['خ'], [], ['x'] )),
            Rule(( [], ['د'], [], ['d'] )),
            Rule(( [], ['ز'], [], ['z'] )),
            Rule(( [], ['ح'], [], ['H'] )),
            Rule(( [], ['ط'], [], ['T'] )),
            Rule(( [], ['ص'], [], ['S'] )),
            Rule(( [], ['ج'], [], ['j'] )),
            Rule(( [], ['غ'], [], ['g'] )),
            Rule(( [], ['ث'], [], ['v'] )),
            Rule(( [], ['ض'], [], ['D'] )),
            Rule(( [], ['ي'], [], ['I'] )),  # check add Haraka
            Rule(( [], ['و'], [], ['U'] )),  # check add Haraka
            Rule(( [], ['آ'], [], ['G', 'A'] )),
        ]


if __name__ == "__main__":
    lts = LetterToSoundRules()
    words_arabic = [
        'الله',
        'قُل',
        'سلام',
        'سلاماً',
        'الشاعر',
        "الشَمسِي"
    ]
    # www = ['َاشماً', 'َاشمً', 'َاشمََ', 'َاشمَن', 'الشماً', 'الشمً', 'الشمََ', 'الشمَن', 'الشماً', 'الشمً', 'الشمََ', 'الشمَن', 'اشماً', 'اشمً', 'اشمََ', 'اشمَن']
    phones = [
        # ["q", "u", "l"],
        # ["s", "l", "A", "m"],
        # ["s", "l", "A", "m", "a", "n"],
        # ["a", "n"]
        ["q", "i", "b", "l", "i", "y", "i", "n"],
        # ["G", "i", "f", "r", "A", "z", "u", "h", "A"]

    ]
    # with open("test.txt", 'w', encoding="utf-8") as test_file:
    #     for word in words_arabic:
    #         phones = lts.word_to_phones(list(word))
    #         phones_concat = " ".join(phones)
    #         print(f'{word}: {phones_concat}')
    with open("test.txt", 'w', encoding="utf-8") as test_file:
        for phon_str in phones:
            words = lts.phones_to_word(phon_str)
            words = words.get_words()
            normalized_words = map(lambda x: lts.normalize_word(x), words)
            # handled = lts.handle_entry(words)
            print(words, file=test_file)

    # root_node = ArNode("")
    # a_node = ArNode("ل")
    # b_node = ArNode("س")
    # c_node = ArNode("ش")
    # root_node.append_node(a_node)
    # a_node.append_node(b_node)
    # a_node.append_node(c_node.append_node(ArNode("م")))
    # ss  = root_node.get_words()
    # print(ss)
    