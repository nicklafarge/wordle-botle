import csv
import itertools
import logging

# file = open('wikipedia-frequencies5.txt', 'r')
file = open('unigram_5.txt', 'r')
lines = file.readlines()
frequency_list = [l.split(' ') for l in lines]
frequency_dict = {v[0]: int(v[1]) for v in frequency_list}

most_common_letters = list('etainoshrdlum')

with open('wordlewords.csv', newline='') as f:
    reader = csv.reader(f)
    scrabble_words = list(reader)[0]


def feedback_byhand(guess, actual_word):
    return input("Wordle response (b y g): ")


def feedback_auto(guess, actual_word):
    response = list('-----')
    for i, gl1 in enumerate(list(guess)):
        if actual_word[i] == gl1:
            response[i] = 'g'

    for j, gl2 in enumerate(list(guess)):
        if response[j] != '-':
            continue
        if gl2 in actual_word and response[actual_word.find(gl2)] != 'g':
            response[j] = 'y'
        else:
            response[j] = 'b'

    resp = ''.join(response)
    logging.info(f"Response: {resp}")
    return resp


def run_botle(possible_words, auto_word=None, user_select=False):
    word = list('-----')
    all_guesses = []

    feedback_fn = feedback_auto if auto_word else feedback_byhand

    if auto_word:
        auto_word = auto_word.lower()

    for i in range(20):
        guess_options = []

        if len(possible_words) == 0:
            logging.info("There are no possible words left. The bot has failed :(")
            return False

        if i == 0:
            guess_options = ["adieu", "react", "anime", "tears", "alone"]
            prompt = [f"{i + 1}. {guess_options[i]}" for i in range(min(5, len(guess_options)))]
        elif i == 1:
            for five_set in itertools.combinations(most_common_letters, 5):
                ay = 1
                for x in itertools.permutations(five_set, 5):
                    possible_word = "".join(x)
                    if possible_word in possible_words:
                        guess_options.append(possible_word)
                        break

            guess_options = sorted(guess_options, key=lambda g: frequency_dict.get(g, 0), reverse=True)
            prompt = [f"{i + 1}. {guess_options[i]}" for i in range(min(5, len(guess_options)))]

        if not guess_options:
            guess_options = possible_words
            freqs = [frequency_dict.get(w, 0) for w in possible_words[0:5]]
            sum_freqs = sum(freqs)
            if sum_freqs > 0:
                freqs = [f / sum_freqs for f in freqs]
            prompt = [f"{i + 1}. {guess_options[i]} ({freqs[i]:.2f})" for i in range(min(5, len(guess_options)))]

        logging.info(f'Options: {{{", ".join(prompt)}}}.')
        while user_select and True:
            selection = input("Select Word (1-5) [6. Input custom]: ")
            if selection.isdigit() and int(selection) in list(range(1, 6)):
                guess = guess_options[int(selection) - 1]
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
        logging.info(f'Guess: {guess} ({len(possible_words)} possible)')
        all_guesses.append(guess)
        val = feedback_fn(guess, auto_word)

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

            if guess[j] in word:  # Dane's edge case
                possible_words = [w for w in possible_words if w[j] != guess[j] and guess[j] in w]
            else:
                possible_words = [w for w in possible_words if guess[j] not in w]

        logging.info("\n")
        if val == 'ggggg':
            n_guesses = len(all_guesses)
            if n_guesses <= 6:
                logging.info("You did it. You successfully cheated at a stupid word game.")
            else:
                logging.info(f"Solved but took too long! {n_guesses}/6")

            logging.info(f"Guesses: {n_guesses}/6")
            logging.info(" -> ".join(all_guesses))
            logging.info(f'The word is: {"".join(word)}')
            return n_guesses



if __name__ == '__main__':
    # w = 'point'
    # print(f"Word={w}")
    # loglevel = logging.WARNING
    loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel)
    logger = logging.getLogger()
    logger.setLevel(loglevel)


    possible_words = sorted(scrabble_words,
                            key=lambda w: 0 if w not in frequency_dict else frequency_dict[w],
                            reverse=True)

    # n_guesses = run_botle(possible_words, auto_word='waves', user_select=False)
    # ng = run_botle(possible_words, user_select=False)
    if 0:
        gt_six = []
        failures = []
        guesses = []
        out = dict()
        # for ii, w in enumerate(possible_words[:2000]):
        for ii, w in enumerate(possible_words):
            if ii % 100 == 0:
                print(f"{ii}/{len(possible_words)}")

            # print(w)
            n_guesses = run_botle(possible_words, auto_word=w, user_select=False)
            out[w] = n_guesses
            if not n_guesses:
                failures.append(w)
            elif n_guesses > 6:
                gt_six.append(w)
            else:
                guesses.append(n_guesses)

        failures = sorted(failures,
                                key=lambda w: 0 if w not in frequency_dict else frequency_dict[w],
                                reverse=True)