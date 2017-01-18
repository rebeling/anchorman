import re


def fix_bs4_parsing_spaces(text):
    text = re.sub("\n <", "\n<", text)
    text = text.replace('\xc2\xa0', ' ')
    text = text.replace('\xc2', ' ')
    text = text.replace('\n', ' ')
    text = re.sub(" +", " ", text)
    return text


def compare_results(annotated, expected):

    for i, x in enumerate(expected):
        if x != annotated[i]:
            print ">>", [x, annotated[i:10]]
            break

    print "expected ", expected[i-10:i+150]
    print "annotated", annotated[i-10:i+150]
