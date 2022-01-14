file = open('enwiki-20190320-words-frequency.txt', 'r')
lines = file.readlines()
frequency_list = [l.split(' ') for l in lines]
frequency_list = {v[0]: int(v[1]) for v in frequency_list if len(v[0]) == 5 and "'" not in v[0]}
# TODO remove accented words (can check with word.encode("ascii"))

possible_words = frequency_list.keys()

word = list('-----')
# "resin house shoes"
for i in range(6):

    if i > 0:
        guess_options = possible_words
        freqs = [frequency_list[w] for w in possible_words[0:5]]
        freqs = [f / sum(freqs) for f in freqs]
        prompt = [f"{i + 1}. {guess_options[i]} ({freqs[i]:.2f})" for i in range(min(5, len(guess_options)))]
    else:
        guess_options = ["adieu", "react", "anime", "tears", "alone"]
        prompt = [f"{i + 1}. {guess_options[i]}" for i in range(min(5, len(guess_options)))]

    print(f'Options: {{{", ".join(prompt)}}}')
    while True:
        selection = input("Select Word (1-5): ")
        if selection.isdigit() and int(selection) in list(range(1, 6)):
            guess = guess_options[int(selection)-1]
            break
        else:
            print(f"Please select a number 1-5")


    print(f'Guess: {guess} ({len(possible_words)} possible)')
    val = input("Wordle response (b y g): ")

    for j, ryg_val in enumerate(val):
        if ryg_val == 'g':
            possible_words = [w for w in possible_words if w[j] == guess[j]]
            word[j] = guess[j]
        elif ryg_val == 'y':
            possible_words = [w for w in possible_words if w[j] != guess[j] and guess[j] in w]

    for j, ryg_val in enumerate(val):
        if ryg_val != 'b':
            continue

        if guess[j] in word: # Dane's edge case
            possible_words = [w for w in possible_words if w[j] != guess[j] and guess[j] in w]
        else:
            possible_words = [w for w in possible_words if guess[j] not in w]

    if val == 'ggggg':
        print("You did it. You successfully cheated at a stupid word game.")
        print(f'The word is: {"".join(word)}')
        break

    if len(possible_words) == 0:
        print("There are no possible words left. The bot has failed :(")
        break
