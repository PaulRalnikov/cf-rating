from objects.Standings import *
from yattag import Doc

class GroupStandings:
    def __init__(self, standings_list : list):
        self.standings_list = standings_list

    def add_standings(self, standings : Standings):
        self.standings_list.append(standings)

    def to_html(self, css_path = "styles.css") -> str:
        doc, tag, text = Doc().tagtext()
        with tag('html', lang='ru'):
            with tag('head'):
                doc.stag('meta', charset='UTF-8')
                doc.stag('meta', **{
                    'name': 'viewport',
                    'content': 'width=device-width, initial-scale=1'
                })
                with tag('title'):
                    text('Рейтинг')
                # link to the external CSS file
                doc.stag('link', rel='stylesheet', href=css_path)

            with tag('body'):
                with tag('div', klass="datatable"):
                    with tag('div', klass="datatable-heading"):
                        text(self.standings_list[1].contest.name)

            #     <div style="position:absolute;right:0.25em;top:0.35em;">
            #         <span style="padding:0;position:relative;bottom:2px;" class="rowCount"></span>

            #         <img class="closed" src="//codeforces.org/s/38057/images/icons/control.png">

            #         <span class="filter" style="display:none;">
            #             <img class="opened" src="//codeforces.org/s/38057/images/icons/control-270.png">
            #             <input style="padding:0 0 0 20px;position:relative;bottom:2px;border:1px solid #aaa;height:17px;font-size:1.3rem;">
            #         </span>
            #     </div>
            # </div>
        return doc.getvalue()
