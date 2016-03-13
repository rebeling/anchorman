
# data for testing schema.org annotation

# s_text: Angela Merkel, CDU, Bundeskanzlerin

# s1_elements:
#     - Angela Merkel, CDU, Bundeskanzlerin:
#         itemtype: http://schema.org/Person
#         itemscope: !!python/none

# expected_result1: <div itemscope itemtype="http://schema.org/Person">Angela Merkel, CDU, Bundeskanzlerin</div>

# expected_result2: <div itemscope itemtype="http://schema.org/Person">Angela Merkel, <div itemscope itemtype="http://schema.org/Organization">CDU</div>, Bundeskanzlerin</div>

# expected_result3: <div itemscope itemtype="http://schema.org/Person"><span itemprop="name">Angela Merkel</span>, <div itemscope itemtype="http://schema.org/Organization"><span itemprop="name">CDU</span></div>, <span itemprop="jobtitle">Bundeskanzlerin</span></div>


# s11_elements:
#     - CDU:
#         itemtype: http://schema.org/Organization
#         itemscope: !!python/none

# s2_elements:
#     - Angela Merkel:
#         itemprop: name
#     - "CDU":
#         itemprop: name
#     - "Bundeskanzlerin":
#         itemprop: jobtitle




# def test_schema_dot_org():
#     """Test annotate tag with schema dot org specs config."""

#     cfg = get_config()
#     unit = {'key': 't', 'name': 'text'}

#     cfg['setting']['text_unit'].update(unit)
#     cfg['markup'] = {'tag': {'tag': 'div'}}


#     annotated1 = annotate(DATA['text'], DATA['s1_elements'], config=cfg)
#     assert annotated1 == DATA['expected_result1']

#     annotated2 = annotate(annotated1, DATA['s11_elements'], config=cfg)
#     assert annotated2 == DATA['expected_result2']

#     cfg3 = cfg.copy()
#     cfg3['markup'] = {'tag': {'tag': 'span'}}
#     annotated3 = annotate(annotated2, s2_elements, config=cfg3)
#     assert annotated3 == DATA['expected_result3']

#     success, cleared_text = clean(annotated3, config=cfg3)
#     assert success
#     assert DATA['expected_result2'] == cleared_text

#     success, cleared_text = clean(cleared_text, config=cfg)
#     assert success
#     assert s_text == cleared_text












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






# def test_annotate_not_implemented_mode():
#     """Test annotate with not implemented mode coreferencer."""

#     cfg = get_config()
#     cfg['setting'].update({'mode': 'coreferencer'})
#     two_paragraphs = DATA['two_paragraphs'].encode('utf-8')
#     link_elements = DATA['elements']

#     try:
#         _ = annotate(two_paragraphs, link_elements, config=cfg)
#     except Exception, e:
#         assert type(e) == NotImplementedError
