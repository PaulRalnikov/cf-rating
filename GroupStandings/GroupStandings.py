from objects.Standings import *
from yattag import Doc

class GroupStandings:
    def __init__(self, standings_list : list):
        self.standings_list : list[Standings] = standings_list

    def add_standings(self, standings : Standings):
        self.standings_list.append(standings)

    def to_html(self, styles_path) -> str:
        doc, tag, text = Doc().tagtext()

        with tag('html', lang='ru'):
            with tag('head'):
                doc.asis('<meta charset="UTF-8">')
                with tag('title'):
                    text('Результаты участников')
                with tag('link', rel='stylesheet', href=styles_path):
                    pass

            with tag('body'):
                with tag('h1'):
                    text('Результаты участников')

                with tag('table', border='1'):
                    with tag('thead'):
                        # Row with contests names
                        with tag('tr', style="display: table-row"):
                            with tag('th', klass="top-left", rowspan=2):
                                pass # empty cell in top left
                            with tag('th', klass="top", rowspan=2):
                                text("Кто")
                            with tag('th', rowspan=2):
                                text("=")

                            for standings in self.standings_list:
                                with tag('th', klass="_OverallCustomRatingFrame_delimiter top", rowspan=2):
                                    pass
                                with tag('th', klass="top", colspan=len(standings.problems)):
                                    text(standings.contest.name)

                        # Row with problem indexes
                        with tag('tr', style="display: table-row"):
                            for standings in self.standings_list:
                                for problem in standings.problems:
                                    with tag('th'):
                                        with tag('span'):
                                            text(problem.index)



        return doc.getvalue()
