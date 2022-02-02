def get_word_to_pronounce(voweled_word):
    """
    Create a word with sukuun on the end of the word that can be pronounced by the Google text to speech API without tanween damma on the end

        U+0652 sukuun
        U+064B tanween fatha
    """

    acceptable_endings = [
        "\u0650", # kesra
        "\u064F", # damma
        "\u064E", # fatha
        "\u0652", # sukuun
        "\u064B", # tanween fatha
        "\u0627", # alif
        "\u0649" # alif maqsuura
        ]
    
    if voweled_word[-1] == "\u0629": # taa marbuuta
        # if ends in taa marbuuta, remove, add fatha to the end, and return it
        return voweled_word[:-1] + "\u064E"

    if voweled_word[-1] not in acceptable_endings:
        # append sukuun to the word and return it
        return voweled_word + "\u0652"

    return voweled_word