import pandas as pd

df = pd.read_csv('unigram_freq.csv')
five_letters = df[df.word.str.len() == 5]

save_file = list(zip(five_letters.word.to_list(), five_letters.counts.to_list()))

textfile = open("unigram_5.txt", "w")
for element in save_file:
    textfile.write(" ".join(map(str, element)) + "\n")
textfile.close()