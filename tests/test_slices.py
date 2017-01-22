# # -*- coding: utf-8 -*-
# from anchorman.positioner.slices_utils import token_regexes


# def test_unit_slices_utils():
#     """Find items and its positions with regexes."""
#     element1 = {u'dog': {'score': 12.0}}
#     element2 = {u'Angela M.': {'score': 12.0}}
#     element3 = {u'überätzend': {'score': 12.0}}

#     # case_sensitive
#     regex = token_regexes([element1, element2, element3], True)
#     assert regex == r'\bdog\b|\bAngela M.\b|\büberätzend\b'

#     # case_insensitive
#     regex2 = token_regexes([element1, element2, element3], False)
#     assert regex2 == r'\bdog\b|\bDog\b|\bDOG\b|\bAngela M.\b|\bANGELA M.\b|\bangela m.\b|\büBeräTzend\b|\büBERäTZEND\b|\büberätzend\b'
