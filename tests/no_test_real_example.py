# -*- coding: utf-8 -*-
from anchorman import annotate, clean, get_config
from tests.utils import fix_bs4_parsing_spaces, compare_results
# css from here http://codepen.io/explosion/pen/ALxpQO


def test_news_article():

    links = [
        {"MacBook Pro": {
            "data-entity": "product", "score": 14.001, "form": "MacBook Pro", "href": "/macBook-pro"}},
        {"Mac Pro": {
            "data-entity": "product", "score": 13.001, "form": "Mac Pro", "href": "/mac-pro"}},
        {"Fliegende Autos": {
            "data-entity": "product", "score": 12.001, "form": "Fliegendes Auto", "href": "/autos"}},
        {"Autonome Autos": {
            "data-entity": "product", "score": 13.001, "form": "autonomen Autos", "href": "/autoauto"}},
        {"iPhone": {
            "data-entity": "product", "score": 42.001, "form": "iPhone", "href": "/iphone"}},

        {"Gigafactory": {
            "data-entity": "facility", "score": 42.001, "form": "Gigafactory", "href": "/gigafactory"}},

        {"Florida": {
            "data-entity": "gpe", "score": 42.001, "form": "Florida", "href": "/florida"}},
        {"Silicon Valley": {
            "data-entity": "gpe", "score": 42.001, "form": "Silicon Valley", "href": "/silicon-valley"}},

        {u"US-Sicherheitsbehörden": {
            "data-entity": "org", "score": 42.001, "form": "US-Sicherheitsbehörden", "href": "/us-sicherheitsbehoerden"}},
        {"Tesla": {
            "data-entity": "org", "score": 42.001, "form": "Tesla", "href": "/tesla"}},
        {"Apple": {
            "data-entity": "org", "score": 42.001, "form": "Apple", "href": "/apple"}},
        {"Volvo": {
            "data-entity": "org", "score": 42.001, "form": "Volvo", "href": "/volvo"}},

        {"Chris Lattner": {
            "data-entity": "person", "score": 7.033, "form": "Chris Lattner", "href": "/chris-lattner"}},
        {"Matt Casebold": {
            "data-entity": "person", "score": 8.002, "form": "Matt Casebold", "href": "/matt-casebold"}},
        {"Elon Musk": {
            "data-entity": "person", "score": 42., "form": "Elon Musk", "href": "/elon-musk"}},
        {"Elon Musks": {
            "data-entity": "person", "score": 42., "form": "Elon Musk", "href": "/elon-musk"}},
        {"Doug Field": 
            {"data-entity": "person", "score": 18., "form": "Doug Field", "href": "/doug-field"}},

        {"Autopilot": {
            "data-entity": "keyword", "score": 42.001, "form": "Autopilot", "href": "/autopiloten"}},
        {"Batterieproduktion": {
            "data-entity": "keyword", "score": 42.001, "form": "Batterieproduktion", "href": "/batterieproduktion"}},
        {"Zukunftsforscher": {
            "data-entity": "keyword", "score": 9.099, "form": "Zukunftsforschung", "href": "/zukunftsforschung"}},
        {"Design": {
            "data-entity": "keyword", "score": 9.077, "form": "Design", "href": "/design"}},
        {"Software": {
            "data-entity": "keyword", "score": 9.0101, "form": "Software", "href": "/software"}}
    ]

    # http://www.automobilwoche.de/article/20170112/NACHRICHTEN/170119979/musk-arbeitet-am-tesla-friedhof-apple-

    text = """<div itemprop="articleBody">
        <p style="margin-top: 0;">Tesla hat den Software-Spezialisten Chris Lattner und sowie den Hardware-Ingenieur Matt Casebold von Apple verpflichtet. Lattner soll den Elektroautobauer bei der Verbesserung seiner Software zum <a href="http://www.automobilwoche.de/apps/pbcs.dll/search?q=autonomes+fahren&amp;daterange=&amp;BuildNavigators=1" target="_blank">autonomen Fahren</a> namens "Autopilot" unterstützen.</p><p style="margin-top: 1em;">Matt Casebold arbeitet in Elon Musks Truppe als Entwicklungschef für "Schließelemente und Mechanismen".</p><p style="margin-top: 1em;">Intern gilt Apple als "Tesla-Friedhof". Das verriet Elon Musk bereits 2015. Der iPhone-Konzern aus dem Silicon Valley stelle nämlich vermehrt Mitarbeiter an, die Tesla gefeuert habe. Die, jedoch, die gut seien, werbe Musk erfolgreich ab. So ging es auch mit dem einstigen Mac-Hardware-Entwicklungschef Doug Field, der seit 2013 an der Entwicklung neuer Tesla-Autos arbeitet.</p>
        <br>
        <h3 style="color: black; font-weight: bold; font-size: 18px;">Lattner und Casebolt neue Tesla-Entwickler</h3>
        <p style="margin-top: 10px;">Chris Lattner arbeitete seit mehr als einem Jahrzehnt für Apple. In einer Nachricht sagte Lattner zu Apple-Entwicklern, dass er "Apple später in diesem Monat verlassen werde", um eine berufliche Chance in einem anderen Bereich zu ergreifen. Lattner selbst nannte Tesla nicht als neuen Arbeitgeber.&nbsp;</p><p style="margin-top: 1em;">Dies übernahm später Tesla, als es verkündete, man habe Lattner als Vizepräsidenten für das Projekt <a href="http://www.automobilwoche.de/apps/pbcs.dll/search?q=autopilot+tesla&amp;BuildNavigators=1" target="_blank">"Autopilot"</a>-Software verpflichtet.</p><p style="margin-top: 1em;">Nach Informationen des <a href="https://9to5mac.com/2017/01/11/matt-casebolt-touchbar-macbook/" target="_blank">Blogs <em>9to5Mac</em></a> arbeitet der ehemals für die Mac-Entwicklung zuständige Senior Director of Design, Matt Casebolt<em> <br></em>schon seit Dezember 2016 als Entwicklungschef für "Schließelemente und Mechanismen". Zuletzt hat Casebold die Entwicklung des neuen MacBook Pro mit Touch Bar geleitet und war zuvor am 2013 neu eingeführten 
         beteiligt.</p>
        <br>
        <h3 style="color: black; font-weight: bold; font-size: 18px;">Apple und die Zukunftsforscher</h3>
        <div class="header_category box_border_bottom_orange box_border_top_lightgray box_border_left_lightgray box_border_right_lightgray" style="padding-top: 2px;">
            <div class="text_center">Daten und Fakten</div>
        </div>
        <div class="factBox0 larger bold">
            Zu diesem Beitrag empfiehlt die Redaktion:<br>
            <p><a href="http://www.automobilwoche-datencenter.de/shop/index/product/Umfrage-von-Oktober-2016-Sollte-der-Einsatz-des-Tesla-Autopiloten-in-seiner-jetzigen-Form-verboten-werden_2792/sed/o7RiFveJ8eNEsutVKjFtHba6mXt8djXseBBJXFgSKT" target="_blank">Umfrage:&nbsp;<span>Sollte der Einsatz des Tesla-Autopiloten in seiner jetzigen Form verboten werden?</span></a></p>
        </div>
        <br>
        <h3 style="color: black; font-weight: bold; font-size: 18px;">Tödlicher Unfall</h3>
        <p style="margin-top: 10px;">Bei "Autopilot" handelt es sich um ein System in Tesla-Fahrzeugen, das in bestimmten Situationen selbständig fahren kann. Der Fahrer muss aber eigentlich trotzdem immer die Hände am Steuer haben. Im vergangenen Jahr hatte es <a href="http://www.automobilwoche.de/article/20160701/AGENTURMELDUNGEN/307019994/erster-todlicher-unfall-mit-autopilot" target="_blank">einen tödlichen Unfall</a> im US-Bundesstaat Florida gegeben, bei dem der "Autopilot" aktiv war. US-Sicherheitsbehörden untersuchen den Vorfall immer noch.</p><p style="margin-top: 1em;">Es gab auch weitere Unfälle mit "Autopilot"-Beteiligung, unter anderem <a href="http://www.automobilwoche.de/article/20160929/AGENTURMELDUNGEN/309299870/tesla-mit-autopilot-fahrt-auf-bus-auf" target="_blank">auch in Deutschland.</a></p><p style="margin-top: 1em;"><strong>Lesen Sie auch:</strong></p><p style="margin-top: 1em;"><a href="http://www.automobilwoche.de/article/20170104/NACHRICHTEN/170109962/tesla-nimmt-gigafactory-ans-netz" target="_blank">Batterieproduktion: Tesla nimmt Gigafactory ans Netz</a></p><p style="margin-top: 1em;"><a href="http://www.automobilwoche.de/article/20170111/NACHRICHTEN/170119977/fliegende-autos-kommen-vor-autonomen-autos" target="_blank">Volvo Zukunftsforscher: Fliegende Autos kommen vor autonomen Autos</a></p><p style="margin-top: 1em;"><a href="http://www.automobilwoche.de/article/20170104/AGENTURMELDUNGEN/301039931/tesla-verfehlt-sein-ehrgeiziges-absatzziel" target="_blank">Tesla verfehlt sein ehrgeiziges Absatzziel</a></p><p style="margin-top: 1em;"></p>
        </div>"""

    # annotated result
    expected = """<div itemprop="articleBody">
<p style="margin-top: 0;"><a class="anchorman" data-entity="org" form="Tesla" href="/tesla" score="42.001">Tesla</a> hat den <a class="anchorman" data-entity="keyword" form="Software" href="/software" score="9.0101">Software</a>-Spezialisten <a class="anchorman" data-entity="person" form="Chris Lattner" href="/chris-lattner" score="7.033">Chris Lattner</a> und sowie den Hardware-Ingenieur <a class="anchorman" data-entity="person" form="Matt Casebold" href="/matt-casebold" score="8.002">Matt Casebold</a> von <a class="anchorman" data-entity="org" form="Apple" href="/apple" score="42.001">Apple</a> verpflichtet. Lattner soll den Elektroautobauer bei der Verbesserung seiner <a class="anchorman" data-entity="keyword" form="Software" href="/software" score="9.0101">Software</a> zum <a href="http://www.automobilwoche.de/apps/pbcs.dll/search?q=autonomes+fahren&amp;daterange=&amp;BuildNavigators=1" target="_blank">autonomen Fahren</a> namens "<a class="anchorman" data-entity="keyword" form="Autopilot" href="/autopiloten" score="42.001">Autopilot</a>" unterstützen.</p><p style="margin-top: 1em;"><a class="anchorman" data-entity="person" form="Matt Casebold" href="/matt-casebold" score="8.002">Matt Casebold</a> arbeitet in <a class="anchorman" data-entity="person" form="Elon Musk" href="/elon-musk" score="42.0">Elon Musks</a> Truppe als Entwicklungschef für "Schließelemente und Mechanismen".</p><p style="margin-top: 1em;">Intern gilt <a class="anchorman" data-entity="org" form="Apple" href="/apple" score="42.001">Apple</a> als "<a class="anchorman" data-entity="org" form="Tesla" href="/tesla" score="42.001">Tesla</a>-Friedhof". Das verriet <a class="anchorman" data-entity="person" form="Elon Musk" href="/elon-musk" score="42.0">Elon Musk</a> bereits 2015. Der <a class="anchorman" data-entity="product" form="iPhone" href="/iphone" score="42.001">iPhone</a>-Konzern aus dem <a class="anchorman" data-entity="gpe" form="Silicon Valley" href="/silicon-valley" score="42.001">Silicon Valley</a> stelle nämlich vermehrt Mitarbeiter an, die <a class="anchorman" data-entity="org" form="Tesla" href="/tesla" score="42.001">Tesla</a> gefeuert habe. Die, jedoch, die gut seien, werbe Musk erfolgreich ab. So ging es auch mit dem einstigen Mac-Hardware-Entwicklungschef <a class="anchorman" data-entity="person" form="Doug Field" href="/doug-field" score="18.0">Doug Field</a>, der seit 2013 an der Entwicklung neuer <a class="anchorman" data-entity="org" form="Tesla" href="/tesla" score="42.001">Tesla</a>-Autos arbeitet.</p>
<br/>
<h3 style="color: black; font-weight: bold; font-size: 18px;">Lattner und Casebolt neue Tesla-Entwickler</h3>
<p style="margin-top: 10px;"><a class="anchorman" data-entity="person" form="Chris Lattner" href="/chris-lattner" score="7.033">Chris Lattner</a> arbeitete seit mehr als einem Jahrzehnt für <a class="anchorman" data-entity="org" form="Apple" href="/apple" score="42.001">Apple</a>. In einer Nachricht sagte Lattner zu <a class="anchorman" data-entity="org" form="Apple" href="/apple" score="42.001">Apple</a>-Entwicklern, dass er "<a class="anchorman" data-entity="org" form="Apple" href="/apple" score="42.001">Apple</a> später in diesem Monat verlassen werde", um eine berufliche Chance in einem anderen Bereich zu ergreifen. Lattner selbst nannte <a class="anchorman" data-entity="org" form="Tesla" href="/tesla" score="42.001">Tesla</a> nicht als neuen Arbeitgeber. </p><p style="margin-top: 1em;">Dies übernahm später <a class="anchorman" data-entity="org" form="Tesla" href="/tesla" score="42.001">Tesla</a>, als es verkündete, man habe Lattner als Vizepräsidenten für das Projekt <a href="http://www.automobilwoche.de/apps/pbcs.dll/search?q=autopilot+tesla&amp;BuildNavigators=1" target="_blank">"<a class="anchorman" data-entity="keyword" form="Autopilot" href="/autopiloten" score="42.001">Autopilot</a>"</a>-<a class="anchorman" data-entity="keyword" form="Software" href="/software" score="9.0101">Software</a> verpflichtet.</p><p style="margin-top: 1em;">Nach Informationen des <a href="https://9to5mac.com/2017/01/11/matt-casebolt-touchbar-macbook/" target="_blank">Blogs <em>9to5Mac</em></a> arbeitet der ehemals für die Mac-Entwicklung zuständige Senior Director of <a class="anchorman" data-entity="keyword" form="Design" href="/design" score="9.077">Design</a>, Matt Casebolt<em> <br/></em>schon seit Dezember 2016 als Entwicklungschef für "Schließelemente und Mechanismen". Zuletzt hat Casebold die Entwicklung des neuen <a class="anchorman" data-entity="product" form="MacBook Pro" href="/macBook-pro" score="14.001">MacBook Pro</a> mit Touch Bar geleitet und war zuvor am 2013 neu eingeführten
         beteiligt.</p>
<br/>
<h3 style="color: black; font-weight: bold; font-size: 18px;">Apple und die Zukunftsforscher</h3>
<div class="header_category box_border_bottom_orange box_border_top_lightgray box_border_left_lightgray box_border_right_lightgray" style="padding-top: 2px;">
<div class="text_center">Daten und Fakten</div>
</div>
<div class="factBox0 larger bold">
            Zu diesem Beitrag empfiehlt die Redaktion:<br/>
<p><a href="http://www.automobilwoche-datencenter.de/shop/index/product/Umfrage-von-Oktober-2016-Sollte-der-Einsatz-des-Tesla-Autopiloten-in-seiner-jetzigen-Form-verboten-werden_2792/sed/o7RiFveJ8eNEsutVKjFtHba6mXt8djXseBBJXFgSKT" target="_blank">Umfrage: <span>Sollte der Einsatz des <a class="anchorman" data-entity="org" form="Tesla" href="/tesla" score="42.001">Tesla</a>-Autopiloten in seiner jetzigen Form verboten werden?</span></a></p>
</div>
<br/>
<h3 style="color: black; font-weight: bold; font-size: 18px;">Tödlicher Unfall</h3>
<p style="margin-top: 10px;">Bei "<a class="anchorman" data-entity="keyword" form="Autopilot" href="/autopiloten" score="42.001">Autopilot</a>" handelt es sich um ein System in <a class="anchorman" data-entity="org" form="Tesla" href="/tesla" score="42.001">Tesla</a>-Fahrzeugen, das in bestimmten Situationen selbständig fahren kann. Der Fahrer muss aber eigentlich trotzdem immer die Hände am Steuer haben. Im vergangenen Jahr hatte es <a href="http://www.automobilwoche.de/article/20160701/AGENTURMELDUNGEN/307019994/erster-todlicher-unfall-mit-autopilot" target="_blank">einen tödlichen Unfall</a> im US-Bundesstaat <a class="anchorman" data-entity="gpe" form="Florida" href="/florida" score="42.001">Florida</a> gegeben, bei dem der "<a class="anchorman" data-entity="keyword" form="Autopilot" href="/autopiloten" score="42.001">Autopilot</a>" aktiv war. <a class="anchorman" data-entity="org" form="US-Sicherheitsbehörden" href="/us-sicherheitsbehoerden" score="42.001">US-Sicherheitsbehörden</a> untersuchen den Vorfall immer noch.</p><p style="margin-top: 1em;">Es gab auch weitere Unfälle mit "<a class="anchorman" data-entity="keyword" form="Autopilot" href="/autopiloten" score="42.001">Autopilot</a>"-Beteiligung, unter anderem <a href="http://www.automobilwoche.de/article/20160929/AGENTURMELDUNGEN/309299870/tesla-mit-autopilot-fahrt-auf-bus-auf" target="_blank">auch in Deutschland.</a></p><p style="margin-top: 1em;"><strong>Lesen Sie auch:</strong></p><p style="margin-top: 1em;"><a href="http://www.automobilwoche.de/article/20170104/NACHRICHTEN/170109962/tesla-nimmt-gigafactory-ans-netz" target="_blank"><a class="anchorman" data-entity="keyword" form="Batterieproduktion" href="/batterieproduktion" score="42.001">Batterieproduktion</a>: <a class="anchorman" data-entity="org" form="Tesla" href="/tesla" score="42.001">Tesla</a> nimmt <a class="anchorman" data-entity="facility" form="Gigafactory" href="/gigafactory" score="42.001">Gigafactory</a> ans Netz</a></p><p style="margin-top: 1em;"><a href="http://www.automobilwoche.de/article/20170111/NACHRICHTEN/170119977/fliegende-autos-kommen-vor-autonomen-autos" target="_blank"><a class="anchorman" data-entity="org" form="Volvo" href="/volvo" score="42.001">Volvo</a> <a class="anchorman" data-entity="keyword" form="Zukunftsforschung" href="/zukunftsforschung" score="9.099">Zukunftsforscher</a>: <a class="anchorman" data-entity="product" form="Fliegendes Auto" href="/autos" score="12.001">Fliegende Autos</a> kommen vor autonomen Autos</a></p><p style="margin-top: 1em;"><a href="http://www.automobilwoche.de/article/20170104/AGENTURMELDUNGEN/301039931/tesla-verfehlt-sein-ehrgeiziges-absatzziel" target="_blank"><a class="anchorman" data-entity="org" form="Tesla" href="/tesla" score="42.001">Tesla</a> verfehlt sein ehrgeiziges Absatzziel</a></p><p style="margin-top: 1em;"></p>
</div>"""

    # use default settings
    annotated = annotate(text, links)

    # compare_results(fix_bs4_parsing_spaces(annotated), fix_bs4_parsing_spaces(expected))
    assert fix_bs4_parsing_spaces(annotated) == fix_bs4_parsing_spaces(expected)

    content = open('test/data/index.tmpl', 'r').read()
    open('test/data/real_example.html', 'w').write(content + annotated)

    cleaned = clean(annotated)
    assert 'class="anchorman"' not in cleaned
