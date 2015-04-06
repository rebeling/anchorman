# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# from codecs import open
# import json
# import anchorman
# import time

# ALLTIME = []
# ALLTIME_APPEND = ALLTIME.append
# TXTLEN = []
# TXTLEN_APPEND = TXTLEN.append
# RPLACEMENTS = []
# RPLACEMENTS_APPEND = RPLACEMENTS.append

# def timing(f):
#     def wrap(*args, **kwargs):
#         time1 = time.time()
#         ret = f(*args, **kwargs)
#         time2 = time.time()
#         ALLTIME_APPEND((time2-time1)*1000.0)
#         # print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
#         return ret
#     return wrap

# DATADIR = "/Users/rebel/Documents/spark-1.2.1-bin-hadoop2.4/data/texte/Vorbericht-Korpora"
# with open('/Users/rebel/Documents/spark-1.2.1-bin-hadoop2.4/data/texte/Vorbericht-Korpora-filenames.txt', 'r', 'utf-8') as f:
#     FILENAMES = f.read().split('\n')


# def get_json_document(DATADIR, filename):
#     with open('%s/%s' % (DATADIR, filename), 'r', 'utf-8') as f:
#         document = json.loads(f.read())
#     return document



# for i,filename in enumerate((FILENAMES*2)[:1000]):

#     @timing
#     def anchorman_it(text, links, markup_format=None):
#         if markup_format:
#             a = anchorman.add(text, links, markup_format=markup_format)
#         else:
#             a = anchorman.add(text, links)
#         return a.result, a.counts

#     links = [
#         {'Wochenende': {'value': '/wiki/fox'}},
#         {'Samstag': {'value': '/wiki/fox'}},
#         {'Mannschaften': {'value': '/wiki/fox'}},
#         {'Mannschaft': {'value': '/wiki/fox'}},
#         {'belegt': {'value': '/wiki/fox'}},
#         {'Bereits': {'value': '/wiki/fox'}},
#         {'der': {'value': '/wiki/fox'}},
#         {'Spieltag': {'value': '/wiki/fox'}},
#         {'Vergangene Woche': {'value': '/wiki/fox'}},
#         {'Spieler': {'value': '/wiki/fox'}},
#         {u'schön': {'value': '/wiki/fox'}},
#         {'Spieler': {'value': '/wiki/fox'}},
#         {'Tor': {'value': '/wiki/fox'}},
#         {'Tabelle': {'value': '/wiki/fox'}},
#         {'Ergebnis': {'value': '/wiki/fox'}}
#         ]

#     markup_format = {
#             'tag': 'a',
#             'value_key': 'href', # attribute for the value (see links in add)
#             'attributes': [
#                 ('style', 'color:blue;cursor:pointer;'),
#                 ('class', 'anchorman')
#                 ],
#             'rm-identifier': 'anchorman-link', # identifier for specific rm
#         }

#     # markup_format = {
#     #     'highlighting': {
#     #         'pre': '${{',
#     #         'post': '}}'
#     #         }
#     #     }



#     f = get_json_document(DATADIR, filename)
#     text = f['body']*3

#     TXTLEN_APPEND(len(text))
#     r, c = anchorman_it(text, links, markup_format=markup_format)
#     RPLACEMENTS_APPEND(sum([y for (x,y) in c]))

#     # break

# def mean(l):
#     return (reduce(lambda x, y: x + y, l) / len(l))


# print "processed items %s" % len(ALLTIME)

# print "mean txt len %s" % mean(TXTLEN)
# print "mean repl per text %s" % mean(RPLACEMENTS)


# print "min  %.5f s" % (min(ALLTIME)/1000)
# print "max  %.5f s" % (max(ALLTIME)/1000)
# print "mean %.5f s" % (mean(ALLTIME)/1000)




# # # without markup

# # mean txt len 1766
# # mean repl per text 11
# # min  0.00060 s
# # max  0.00891 s
# # mean 0.00152 s
# # [Finished in 1.7s]


# # # with markup

# # processed items 1000
# # mean txt len 1766
# # mean repl per text 11
# # min  0.00061 s
# # max  0.00929 s
# # mean 0.00158 s
# # [Finished in 1.8s]


# # # highlight context

# # processed items 1000
# # mean txt len 1766
# # mean repl per text 11
# # min  0.00057 s
# # max  0.00783 s
# # mean 0.00117 s
# # [Finished in 1.4s]




# # processed items 1000
# # mean txt len 1766
# # mean repl per text 11
# # min  0.00092 s
# # max  0.01398 s
# # mean 0.00253 s
# # [Finished in 2.8s]

# # processed items 1000
# # mean txt len 1766
# # mean repl per text 11
# # min  0.00083 s
# # max  0.01216 s
# # mean 0.00186 s
# # [Finished in 2.1s]


# # processed items 1000
# # mean txt len 1766
# # mean repl per text 11
# # min  0.00062 s
# # max  0.01047 s
# # mean 0.00146 s
# # [Finished in 1.7s]

# # processed items 1000
# # mean txt len 1766
# # mean repl per text 1
# # min  0.00030 s
# # max  0.00406 s
# # mean 0.00069 s
# # [Finished in 0.9s]
