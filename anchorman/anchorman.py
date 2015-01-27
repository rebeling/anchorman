#!/usr/bin/env python
# -*- coding: utf-8 -*-

from linkit import linker_format
from linkit import add_links
from linkit import remove_links
from utils import sort_for_longest_match


class Anchorman(object):
    """
    Create the main object for the add_links request.
    """
    def __init__(self, *args, **kwargs):
        self.link_format = None
        self.selector = './/a'
        self.set_link_format(kwargs)
        self.result, self.counts = None, None

    def __str__(self):
        return self.result

    def set_link_format(self, kwargs):
        markup_format = kwargs.get('markup_format', {})
        if markup_format:
            self.markup_format = markup_format
        new_lf, selector = linker_format(markup_format)
        self.link_format = new_lf if new_lf else self.link_format
        self.selector = selector if selector else self.selector

    def add(self, links, html, **kwargs):
        self.set_link_format(kwargs)
        kwargs['link_format'] = self.link_format
        markup_format = kwargs.get('markup_format', {})
        if markup_format:
            self.markup_format = markup_format
        self.result, self.counts = add_links(html,
                                             sort_for_longest_match(links),
                                             **kwargs)
        return self.result

    def remove(self, *args, **kwargs):
        self.set_link_format(kwargs)
        text = args[0] if args else self.result
        self.result = remove_links(text,
            selector=self.selector,
            markup_format=self.markup_format)



if __name__ == '__main__':


    markup_format = {
        'tag': 'a',
        'value_key': 'href',
        'attributes': [
            ('style', 'color:blue;cursor:pointer;'),
            ('class', 'anchorman')
            ],
        'rm-identifier': 'anchorman-link',
        # 'highlighting': {
        #     'pre': '${{',
        #     'post': '}}'
        #     },
        # 'case-sensitive': False,
        }

    links = [
            {'tail': {
                'value': '/tail',
                }
            },
            {'Fox': {
                'value': '/fox',
                }
            },
            {'mammals': {
                'value': '/mammals',
                }
            },
            {'red fox': {
                'value': '/redfox',
                'attributes': [
                    ('class', 'animal'),
                    ('style', 'font-size:23px;background:red'),
                    ('title', 'Fix und Foxi')
                    ]
                }
            }
        ]

    string = (
        """
        <p>Foxes are small-to-medium-sized, omnivorous mammals belonging to several genera of the Canidae family. Foxes are slightly smaller than a medium-size domestic dog, with a flattened skull, upright triangular ears, a pointed, slightly upturned snout, and a long bushy tail (or brush).</p>
        <p>Twelve species belong to the monophyletic group of Vulpes genus of "true foxes". Approximately another 25 current or extinct species are always or sometimes called foxes; these foxes are either part of the paraphyletic group of the South American foxes and the outlying group, which consists of Bat-eared fox, Gray fox, and Island fox.[1] Foxes are found on every continent except Antarctica. By far the most common and widespread species of fox is the red fox (Vulpes vulpes) with about 47 recognized sub-species.[2] The global distribution of foxes, together with their widespread reputation for cunning, has contributed to their prominence in popular culture and folklore in many societies around the world. The hunting of foxes with packs of hounds, long an established pursuit in Europe, especially in the British Isles, was exported by European settlers to various parts of the New World.</p>
        """
        )

    a = Anchorman()

    a.add(
        links,
        string,
        markup_format=markup_format, # default: a, href=value, class="anchorman"
        # replaces_per_item=1          # default: all occurences
        )

    print '\nenriched string'
    print a
    print a.counts
    # print '\n### cleared version: ###'
    # a.remove()
    # print a

    page = "<html><head></head><body>%s</body></html>" % a
    with open('example.html', 'w') as f:
        f.write(page)

