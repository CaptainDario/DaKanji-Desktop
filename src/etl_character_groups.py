from enum import Enum

class ETLCharacterGroups(Enum):

    all      = r".*"

    kanji    = r"[一-龯]"
    katakana = r"[ァ-ン]"
    hiragana = r"[ぁ-ん]"
    number   = r"[0-9]"
    roman    = r"[A-Za-z]"
    #if it is none of the above, it has to be a symbol 
    symbols  = r"^(?!" + "|".join([kanji, katakana, hiragana, number, roman]) + ")"