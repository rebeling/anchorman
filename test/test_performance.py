# # -*- coding: utf-8 -*-
# import random as r
# import string
# from anchorman.main import annotate

# letters = string.ascii_lowercase

# nr_of_sentences = 100
# nr_of_elements = 1000
# nr_of_unknown_token = 100
# nr_of_paragraphs = 100
# nr_of_sentences_per_p = 10

# known_token = []
# unknown_token = []


# def word():
#     token = r.sample(letters, r.randint(2, 12))
#     token = ''.join(token)
#     known_token.append(token)
#     return token


# def sentence():
#     sentence = (word() for i in xrange(r.randint(2, 8)))
#     tokens = ' '.join(sentence) + r.choice('..........................?!')
#     return tokens[0].upper() + tokens[1:]


# def paragraph():
#     s = ' '.join( (sentence() for i in xrange(r.randint(3, nr_of_sentences_per_p)) ))
#     return '<p>%s</p>' % s if nr_of_paragraphs else s


# text = ' '.join((paragraph() for i in xrange(nr_of_paragraphs)))
# links = [{x: {'value': '/wiki/queick', 'score': 0.2, 'type': 'jj'}} for x in known_token[:nr_of_elements]]

# x = annotate(text, links)
# # print x
