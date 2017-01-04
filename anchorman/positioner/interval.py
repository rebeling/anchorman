# -*- coding: utf-8 -*-
from intervaltree import IntervalTree
from anchorman.positioner.slices import unit_slices, element_slices


def intervals(text, elements, config):
    """From the slices of elements and units create an intervaltree.

    :param text:
    :param elements:
    :param config:
    """
    units, forbidden = unit_slices(text, config)
    tree = to_intervaltree(forbidden)

    # create interval tree for units and forbidden areas
    # get possible element slices based on the interval tree
    # check if they are possible in units or not allowed! by from, to
    slices = element_slices(text, elements, config)
    tree = to_intervaltree(slices, tree=tree, elements=True)
    tree = cleanup_tree(tree)

    return units, tree


def to_intervaltree(data, tree=None, elements=None):
    """Create an intervaltree for units and forbidden.

    :param data:
    :param tree:
    :param elements:
    """
    tree = IntervalTree() if tree is None else tree

    if elements is True:
        # check if the elements can be placed in the tree
        for token, slices, _type in data:
            _from, _to = slices
            appliable = True
            for x in tree[_from:_to]:
                x_data = x.data
                if x_data == 'insidetag' or x_data == 'forbidden':
                    appliable = False

            if appliable:
                tree[_from:_to] = (token, _type)
    else:
        # data is the forbidden areas in this case
        for token, slices, _type in data:
            _from, _to = slices
            tree[_from:_to] = _type[0]

    return tree


def cleanup_tree(tree):
    """Remove forbidden area intervals from tree."""
    rm = [x for x in tree if x.data in ['insidetag', 'forbidden']]
    for interval in rm:
        tree.remove(interval)
    return tree
