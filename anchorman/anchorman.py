#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import re
import regex as re
from linkit import add_links
from linkit import linker_format
from linkit import re_pattern_of
from linkit import remove_links
from linkit import finditer_result
from utils import sort_longest_match_first
from utils import validate_input


"""
Anchorman is the basic API for the link it request.

    Beside text and links, use markup\_format and replaces\_per\_item
    to describe the core functionality. The links will be specified
    as a list of dicts. Dicts key will be the string in the original
    text to be replaced/augmented.

    links = [
        {'red fox': {
            'value': '/redfox',
            # add or augment the general attributes (see markup)
            # with more specific or extra attribute, value pairs
            'attributes': [
                ('class', 'animal'),
                ('style', 'font-size:23px;background:red'),
                ('title', 'The red fox is red')
                ]
            }
        },
        {'green hornet': { ... }, ...
    ]

    The markup_format object has two options:

    1. link format
    2. context highlighting

    markup_format = {
        'tag': 'a',
        'value_key': 'href', # attribute for the value (see links in add)
        'attributes': [
            ('style', 'color:blue;cursor:pointer;'),
            ('class', 'anchorman')
            ],
        'rm-identifier': 'anchorman-link', # identifier for specific rm

        # --- * ---
        # or highlight the target with a pre- and postfix
        'highlighting': {
            'pre': '${{',
            'post': '}}'
            },

        # --- * ---
        'case-sensitive': False, # works for both, default is True
    }

    Params

    Returns an anchorman class object


    Args (alias of Parameters)
    Arguments (alias of Parameters)
    Attributes
    Example
    Examples
    Keyword Args (alias of Keyword Arguments)
    Keyword Arguments
    Methods

    Notes
    Other Parameters
    Parameters
    Return (alias of Returns)
    Returns
    Raises
    References
    See Also
    Warning
    Warnings (alias of Warning)
    Warns
    Yields


"""


class Anchorman(object):
    """Main module interface object for add and remove annotations.

    Args:
        text (string, optional): The first parameter.

        links (list, optional): The second parameter.
            Second line of description should be indented.


    Keyword Args:

        selector (string)

        replaces_per_item (int): Default 1

        replaces_at_all (int): Default 5555555

        longest_match_first (bool): Default True


    Markup_format in kwargs will update selector when processed.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the class with data from args and kwargs

        """
        self.text = None
        self.links = None
        if args:
            self.text = args[0]
            self.links = args[1]
        self.selector = kwargs.get('selector', './/a')
        self.replaces_per_item = kwargs.get('replaces_per_item', 1)
        self.replaces_at_all = kwargs.get('replaces_at_all', 5555555)
        self.longest_match_first = kwargs.get('longest_match_first', True)
        self._markup_format = {'tag': 'a', 'value_key': 'href'}
        self._update_data(**kwargs)
        self.result = None
        self.counts = None

    def __str__(self):
        if self.result:
            return self.result
        else:
            return "%s" % self.__class__

    @property
    def markup_format(self):
        return self._markup_format

    @markup_format.setter
    def markup_format(self, markup_format):
        """Markup format updates link and selector"""
        _, _selector = linker_format(markup_format)
        if _selector:
            self.selector = _selector
        self._markup_format = markup_format

    def _update_data(self, *args, **kwargs):

        if args:
            try:
                if 'remove' in kwargs:
                    self.text = args[0]
                else:
                    self.text, self.links = args[0], args[1]
            except ValueError, e:
                raise "Args not specified correctly: %s" % e

        if 'replaces_per_item' in kwargs:
            self.replaces_per_item = kwargs['replaces_per_item']

        if 'markup_format' not in kwargs:
            self.markup_format = self.markup_format
        else:
            self.markup_format = kwargs['markup_format']

    def add(self, *args, **kwargs):
        """Add links to text.

        Text and links can be initialized on class level, but also
        reset in here as args.

        Args:
            text: The first parameter.
            links: The second parameter.

        Returns:
            result (String): the enriched text.
        """
        self._update_data(*args, **kwargs)
        if self.longest_match_first:
            self.links = sort_longest_match_first(self.links)

        result = add_links(self.text,
                           self.links,
                           replaces_per_item=self.replaces_per_item,
                           replaces_at_all=self.replaces_at_all,
                           markup_format=self.markup_format)

        self.result, self.counts = result
        return self.result

    def remove(self, *args, **kwargs):
        """Remove links/markup from text based on markup_format.

        Returns:
            result (String): the cleared text.
        """
        kwargs['remove'] = True
        self._update_data(*args, **kwargs)
        self.result = remove_links(kwargs.get('text', self.result),
                                   self.markup_format,
                                   selector=self.selector)
        return self.result

    def positions(self):
        """Get positions of all links in text.

        Returns:
            result (List): list of tuples (match, positions) in text.
        """
        allkeys = map(lambda a: a.keys()[0], self.links)
        result = []
        text = "{}".format(self.text)
        # cs = self.markup_format.get('case_sensitive', True)

        # if cs:
        #     key = '|'.join(allkeys)
        # else:
        def all3forms(k):
            return list(set([k, k.lower(), k.upper(), k.title()]))

        keys = []
        for k in allkeys:
            x = all3forms(k)
            for y in x:
                keys.append(y)
        print keys
        key = '|'.join(keys)


        re_w, re_capture = re_pattern_of(key) #, case_sensitive=cs)
        r = finditer_result(text, None, re_capture)
        for match in r:
            st, en = match.span()
            gr = match.groups()
            st += len(gr[0])
            en -= len(gr[2])
            # result.append((key, (st, en), match.groups()[1]))
            result.append((match.groups()[1], (st, en)))
        return result

def add(text, links, **kwargs):
    """Call class on module level, initialize and return the class.

    Operate on this object instead of the class directly for simplicity.
    If text and links are provided apply them. The returned object
    contains result then already.

    Examples:
        Use it like this::

            import anchorman
            a = anchorman.add(text, links)

    Args:
        text: The first parameter.
        links: The second parameter.

    Returns:
        anchorman (class): the class object with added markup.

    """
    success, values = validate_input((text, links))
    if success:
        text, links = values
    else:
        raise ValueError(values)

    a = Anchorman(text, links, **kwargs)
    a.add()
    return a


if __name__ == '__main__':

    # import cProfile
    # links = [
    #     {'Wochenende': {'value': '/wiki/fox'}},
    #     {'Samstag': {'value': '/wiki/fox'}},
    #     {'Mannschaften': {'value': '/wiki/fox'}},
    #     {'Mannschaft': {'value': '/wiki/fox'}},
    #     {'belegt': {'value': '/wiki/fox'}},
    #     {'Bereits': {'value': '/wiki/fox'}},
    #     {'der': {'value': '/wiki/fox'}},
    #     {'Spieltag': {'value': '/wiki/fox'}},
    #     {'Vergangene Woche': {'value': '/wiki/fox'}},
    #     {'Spieler': {'value': '/wiki/fox'}},
    #     {u'schön': {'value': '/wiki/fox'}},
    #     {'Spieler': {'value': '/wiki/fox'}},
    #     {'Tor': {'value': '/wiki/fox'}},
    #     {'Tabelle': {'value': '/wiki/fox'}},
    #     {'Ergebnis': {'value': '/wiki/fox'}}
    #     ]

    text = """Zweite Bundesliga Wunschtrainer Tuchel sagt RB Leipzig ab <p>Mit Thomas Tuchel auf der Trainerbank wollte RB Leipzig nach ganz oben. Doch daraus wird nichts. Der Wunschkandidat sagt dem Klub aus der zweiten Liga ab. Die Begründung liefert Tuchels Berater. Wohin zieht es Thomas Tuchel? Leipzig ist nicht das Ziel des Trainers Wunschkandidat Thomas Tuchel hat Rasenballsport Leipzig eine Absage erteilt. „Thomas Tuchel wird im Sommer definitiv nicht Trainer von RB Leipzig“, sagte Sportdirektor Ralf Rangnick der „Leipziger Volkszeitung“. Tuchels Berater habe dem Klub-Vorstandsvorsitzenden, Oliver Mintzlaff, mitgeteilt, dass der 41-Jährige nicht in die zweiten Fußball-Bundesliga gehe, schrieb die Zeitung am Montag auf ihrer Internetseite. „RB Leipzig ist unabhängig von Herrn Tuchel und anderen Namen auch nicht bereit, finanzielle Grenzen für einen Zweitliga-Trainer zu überschreiten“, sagte Mintzlaff der „Sport Bild“. „Unser Weg bleibt unbeirrt – wir werden mit unserer A-Lösung auf der Trainerposition in die neue Saison gehen.“ Mehr zum Thema Die aktuelle Tabelle der Fußball-Bundesliga Hamburger SV : Ein Nest für Tuchel</p> Vorwürfe von Torwart Müller: „Tuchel ist ein Diktator“ <p>Rangnick hatte Tuchel stets als einen idealen Kandidaten für die kommende Saison bezeichnet, eine bereits vorliegende Einigung aber immer dementiert. Die Trainerfrage hatte sich gestellt, nachdem Alexander Zorniger im Februar vorzeitig aus seinem Vertrag bei RB ausgestiegen war. Nachwuchscoach Achim Beierlorzer war als Interimstrainer bis zum Saisonende verpflichtet worden.</p><p>Die Leipziger haben sieben Spieltage vor dem Saisonende nur noch theoretische Chancen auf den Durchmarsch in die Bundesliga. Nach dem 2:1-Sieg am Ostersonntag über den 1. FC Nürnberg liegen sie acht Zähler hinter dem Relegationsplatz drei.</p><p>Tuchel, dessen ruhender Vertrag zum Saisonende beim Bundesligaverein FSV Mainz 05 ausläuft, ist bei verschiedenen Vereinen im Gespräch. Der 41-Jährige hatte Mainz im vergangenen Sommer verlassen und war seitdem kein neues Engagement eingegangen.</p>"""

    # cProfile.run('add(text, links)')



    links = [{'red fox': {'value': '/wiki/fox'}}, {'fox': {'value': '/wiki/fox'}}, {'dog': {'value': '/wiki/dog'}}]
    # text = "fox The quick brown fox jumps over the lazy <br> dog and fox. dog"
    text = "fox fox red fox Dog dog Dog"

    # b = Anchorman(text, links, replaces_per_item=100000)
    # print b.positions()

    # markup_format = {
    #     'replace_match_with_value': True,
    #     'tag': "a",
    #     'value_key': "href", # attribute for the value see _get_entity_item
    #     'attributes': [("class", "taxonomy-entity"),
    #                    # ("xCOLONshow", "embed"),
    #                    # ("xCOLONtype", "simple")
    #                    ]
    # }

    # text = "<p>Foxes are small-to-medium-sized, omnivorous mammals belonging to several genera of the Canidae family. Foxes are slightly smaller than a medium-size domestic dog, with a flattened skull, upright triangular ears,<br> a pointed, slightly upturned snout, and a long bushy tail (or brush).</p>"

    text = "Foxes are small-to-medium-sized, omnivorous mammals belonging to several genera of the Canidae family. Foxes are slightly smaller than a medium-size domestic dog, with a flattened skull, upright triangular ears, a pointed, slightly upturned snout, and a long bushy tail (or brush)."

    links = [
        {'Fox': {'value': '/fox'}},
        {'mammals': {'value': '/mammals'}},
        {'red fox': {
            'value': '/redfox',
            'attributes': [
                ('class', 'animal'),
                ('style', 'font-size:23px;background:red'),
                ('title', 'Fix und Foxi')
                ]
            }
        },
        {'a medium-size domestic dog': {'value': '/dog'}}
    ]


    markup_format = {
        # 'case_sensitive': False,
        # 'replace_match_with_value': True,
        # 'highlighting': {
        #     'pre': '${{',
        #     'post': '}}'
        #     }
    }

    # replaces_per_item=1
    # replaces_at_all=1

    a = add(
        text,
        links,
        # replaces_per_item=3,
        # replaces_at_all=1,
        markup_format=markup_format
        )
    print a
    print text
    # print a.positions()
    # a.remove()
    # print a


    # markup_format = {
    #     'tag': "a",
    #     'value_key': "xCOLONhref", # attribute for the value see _get_entity_item
    #     'attributes': [("class", "taxonomy-entity"),
    #                    ("xCOLONshow", "embed"),
    #                    ("xCOLONtype", "simple")]
    # }
    # anchi = Anchorman(markup_format=markup_format, selector='.//a[@class="taxonomy-entity"]', replaces_per_item=1)
    # print anchi.selector
    # print anchi.replaces_per_item
    # anchi.remove('erewvbrg ew fefe')
