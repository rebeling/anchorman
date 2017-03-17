# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
from tests.utils import fix_bs4_parsing_spaces
from tests.data.dummy import LINKS


def test_remove_decoration():

    annotated = """<div><p id="1">lala <span type="letterA"><a class="anchorman">A</a></span> la lala <span type="letterA"><a class="anchorman">AA</a></span> <span type="letterB"><a class="anchorman">BB</a></span> <span type="letterB"><a class="anchorman">B</a></span> la <span type="letterC"><a class="anchorman">C</a></span> lalala <span type="letterD">DDD</span> <span type="letterD">D</span> <span type="letterE">E</span></p> <p id="2">la <span type="letterE">E</span> <span type="letterE">EE</span> <span type="letterA">AA</span> lal <span type="letterC">CC</span> <span type="letterC">C</span> la la <span type="letterB">BB</span> la <span type="letterD">DD</span> <span type="letterD">D</span> lala <span type="letterE">EE</span> la</p> <p id="3"><span type="letterB">B</span> la <span type="letterB">BB</span> <span type="letterE">EEE</span> <span type="letterA">A</span> la <span type="letterC">CCC</span> <span type="letterB">B</span> la <span type="letterD">DDD</span> <span type="letterC">C</span> lala <span type="letterA">AAA</span> <span type="letterD">D</span> la <span type="letterB">BBB</span> <span type="letterE">E</span></p></div>"""

    cleaned = """<div><p id="1">lala A la lala AA BB B la C lalala DDD D E</p><p id="2">la E EE AA lal CC C la la BB la DD D lala EE la</p><p id="3">B la BB EEE A la CCC B la DDD C lala AAA D la BBB E</p></div>"""



