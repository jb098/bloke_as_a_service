"""
Credit to the below fot the code that this is based on.
http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
"""

import random

class Markov(object):

    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()

    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return words


    def triples(self):
        """ Generates triples from the given data string. So if our string were
                "What a lovely day", we'd generate (What, a, lovely) and then
                (a, lovely, day).
        """

        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (str(self.words[i]), str(self.words[i+1]), str(self.words[i+2]))

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def start_criteria(self):
        seed = random.randint(0, self.word_size-3)
        if self.words[seed][0].isupper():
            return self.words[seed], self.words[seed+1]
        else:
            return self.start_criteria()

    def generate_markov_text(self):
        w1, w2  = self.start_criteria()
        gen_words = []
        while "." not in w2:
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w1)
        gen_words.append(w2)
        return ' '.join(gen_words)

if __name__ == "__main__":
    with open("quotes.txt") as quotes:
        markov = Markov(quotes)
    print(markov.generate_markov_text())
