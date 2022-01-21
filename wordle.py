import csv
import itertools

# file = open('wikipedia-frequencies5.txt', 'r')
file = open('unigram_5.txt', 'r')
lines = file.readlines()
frequency_list = [l.split(' ') for l in lines]
frequency_dict = {v[0]: int(v[1]) for v in frequency_list}

most_common_letters = list('etainoshrdlum')

with open('wordlewords.csv', newline='') as f:
    reader = csv.reader(f)
    scrabble_words = list(reader)[0]


possible_words = sorted(scrabble_words,
                        key=lambda w: 0 if w not in frequency_dict else frequency_dict[w],
                        reverse=True)

user_select = False

word = list('-----')

for i in range(6):
    if i > 1:
        guess_options = possible_words
        freqs = [frequency_dict.get(w, 0) for w in possible_words[0:5]]
        freqs = [f / sum(freqs) for f in freqs]
        prompt = [f"{i + 1}. {guess_options[i]} ({freqs[i]:.2f})" for i in range(min(5, len(guess_options)))]
    elif i == 1:
        guess_options = []
        for five_set in itertools.combinations(most_common_letters, 5):
            ay = 1
            for x in itertools.permutations(five_set, 5):
                possible_word = "".join(x)
                if possible_word in possible_words:
                    guess_options.append(possible_word)
                    break

        guess_options = sorted(guess_options, key=lambda g: frequency_dict.get(g, 0), reverse=True)
        prompt = [f"{i + 1}. {guess_options[i]}" for i in range(min(5, len(guess_options)))]
    else:
        guess_options = ["adieu", "react", "anime", "tears", "alone"]
        prompt = [f"{i + 1}. {guess_options[i]}" for i in range(min(5, len(guess_options)))]

    print(f'Options: {{{", ".join(prompt)}}}.')
    while user_select and True:
        selection = input("Select Word (1-5) [6. Input custom]: ")
        if selection.isdigit() and int(selection) in list(range(1, 6)):
            guess = guess_options[int(selection)-1]
            break
        elif selection.isdigit() and int(selection) == 6:
            while True:
                guess = input("You think you're so smart? Input your 5-letter word: ")
                if len(guess) == 5:
                    break
                else:
                    print("Five letters genius....")
            break
        else:
            print(f"Please select a number 1-5")

    if not user_select:
        guess = guess_options[0]
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

        if i == 0:
            if guess[j] in most_common_letters:
                most_common_letters.remove(guess[j])


        if guess[j] in word: # Dane's edge case
            possible_words = [w for w in possible_words if w[j] != guess[j] and guess[j] in w]
        else:
            possible_words = [w for w in possible_words if guess[j] not in w]

    print()
    if val == 'ggggg':
        print("You did it. You successfully cheated at a stupid word game.")
        print(f'The word is: {"".join(word)}')
        break

    if len(possible_words) == 0:
        print("There are no possible words left. The bot has failed :(")
        break
