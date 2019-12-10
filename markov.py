import random
from collections import Counter,defaultdict

def create_markov_high_model(data,order = 2):
    markov_model = defaultdict(Counter)
    for i in range(len(data)-order):
        window = tuple(data[i:i+order])
        markov_model[window][data[i+order]]+=1
    return markov_model

def update_markov_high_model(model,
                             data,
                             order = 2):
    for i in range(len(data)-order):
        window = tuple(data[i:i+order])
        model[window][data[i+order]]+=1
    return model

def generate_random_start(model):
    return random.choice(list(model.keys()))

def generate_random_sentence(model):
    # init start
    current_words = generate_random_start(model)
    # init sentence
    sentence = list(current_words)
    # loop while not logic end
    while current_words[-1] != ('<END>'):
        # sort by weights for weighted random choice
        rev_weighted_words = sorted(model[current_words].items(),key = lambda item: item[1],reverse = True)
        words = [word for word,weight in rev_weighted_words]
        weights = [weight for word,weight in rev_weighted_words]
        next_word = random.choices(words,weights, k = 1)[0]
        # appending next word to sentence
        sentence.append(next_word)
        # shifting the window
        current_words = list(current_words)[1:]
        current_words.append(next_word)
        current_words = tuple(current_words)
    # Popping <END> from the end of sentence? because it is
    sentence.pop()
    return ' '.join(sentence)

