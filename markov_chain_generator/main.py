import re
import json
import random


with open("characters.json", "r") as file:
    characters = json.load(file)
    #dwight_lines = characters["Dwight"]
    #all_lines = []
    #for character in characters:
    #    all_lines.extend(characters[character])

"""
punctuation = {}
for line in dwight_lines:
    line = re.sub(r"\[.*\]", "", line)
    line = line.replace("...", " ")
    line = "".join([c for c in line if c not in punctuation]).strip()
    words = line.split(" ")
    print(words)
"""



choices = ["Dwight"]
for i in range(10):
    character_name = random.choice(choices)
    lines = characters[character_name]
    n = 3
    model = {}
    n_grams = {}
    for line in lines:
        line = re.sub(r"\[.*\]", "", line)
        
        for i in range(0, len(line)-n):
            gram = line[i:i+n]
            if gram not in n_grams:
                n_grams[gram] = {}
            next_character = line[i+n]
            if next_character not in n_grams[gram]:
                n_grams[gram][next_character] = 0
            n_grams[gram][next_character] += 1

    gram = random.choice([gram for gram in n_grams.keys()])
    while not gram[0].isupper():
        gram = random.choice([gram for gram in n_grams.keys()])
    print(gram)

    result = gram
    for i in range(150):
        if character_data := n_grams.get(gram):
            total = sum([occurences for occurences in character_data.values()])
            next_character = random.choices(
                population=[c for c in character_data.keys()],
                weights=[occurences/total for occurences in character_data.values()],
                k=1,
            )[0]
            result += next_character
            gram = result[-n:]
        else:
            break

    print(f"{character_name}: {result}")

quote = "I love catching people in the act. That's why I always whip open doors."
n = 3
n_grams = []
for i in range(0, len(quote)-n):
    gram = quote[i:i+n]
    n_grams.append(gram)
print(n_grams)