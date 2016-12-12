from anchorman import annotate, get_config, clean

TEXT_IN = """
<div xmlns=\"http://www.coremedia.com/2003/richtext-1.0\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">
    <p><img title="Celine Dion 2"/>Celine Dion hat einen neuen BMW. Celine Dion BMW </p>
    <p><figure href="Celine Dion">Celine Dion</figure> Celine Dion hat ein neues iPad. </p>
</div>
"""

links = [
    {u'iPad': {
        'lookup': ('product', u'iPad'),
        'xcolonhref': 'taxonomy:product:90946881t',
        'type': 'simple'}},
    {u'BMW': {
        'lookup': ('organization', u'BMW'),
        'xcolonhref': 'taxonomy:organization:90247565t',
        'type': 'simple'}},
    {u'Celine Dion': {
        'lookup': ('person', u'Celine Dion'),
        'xcolonhref': 'taxonomy:person:90281420t',
        'type': 'simple'}}
]


cfg = get_config()
projectcfg = {
    'markup': {
        'tag': {
            'tag': 'a',
            'value_key': "xcolonhref"
        }
    }
}

cfg.update(projectcfg)

setting = {
    'replaces_per_item': 10,
    'replaces_at_all': 5,
    'longest_match_first': False
}

cfg['settings'].update(setting)


annotated = annotate(TEXT_IN, links, config=cfg)

print annotated

print clean(annotated, config=cfg)
