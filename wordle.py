file = open('reduced-words.txt', 'r')
lines = file.readlines()
frequency_list = [l.split(' ') for l in lines]
frequency_list = [w for w in frequency_list if len(w[0]) == 5]

possible_words = [f[0] for f in frequency_list]

unknown_ixs = list(range(5))

for i in range(6):
    # Make sure the first two guesses use 5 distinct letters
    if i < 2:
        for pw in possible_words:
            guess = pw
            if len(set(guess)) == 5:
                break
    else:
        guess = possible_words[0]

    print(f'Guess: {guess} ({len(possible_words)} possible)')
    val = input("Wordle response (b y g): ")

    if val == 'ggggg':
        print("You did it. You successfully cheated at a stupid word game.")
        break

    # start with greens/blacks
    for j1, v1 in enumerate(val):
        if v1 == 'g':
            possible_words = [w for w in possible_words if w[j1] == guess[j1]]
            if j1 in unknown_ixs:
                unknown_ixs.remove(j1)
        elif v1 == 'b':
            possible_words = [w for w in possible_words if guess[j1] not in w]

    # Handle yellows
    for j2, v2 in enumerate(val):
        if v2 == 'y':
            possible_words = [w for w in possible_words if w[j2] != guess[j2]]
            # possible_words = [w for w in possible_words if any(w[k] == guess[j2] for k in unknown_ixs)]
            possible_words = [w for w in possible_words if guess[j2] in w]

    if len(possible_words) == 0:
        print("There are no possible words left. The bot has failed :(")
        break