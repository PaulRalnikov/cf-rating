from objects.Standings import *
from yattag import Doc

class GroupStandings:
    def __init__(self, standings_list : list):
        self.standings_list : list[Standings] = sorted(standings_list, key = lambda standings : standings.contest.startTimeSeconds)

    def add_standings(self, standings : Standings):
        self.standings_list.append(standings)

    class StandingsRow:
        def __init__(self, handle : str, place : str = "", total_solved : int = 0, contests_info = dict()):
            self.handle = handle
            self.place = place
            self.totalSolved = total_solved
            self.contestsInfo = contests_info.copy()

        def __str__(self):
            return f"Row(handle={self.handle}, place={self.place}, total_solved={self.totalSolved}, contests_info={self.contestsInfo})"

        def __repr__(self):
            return self.__str__()
    '''
    Returns list of StandingsRow sorted by total_solved
    '''
    def get_rating(self) -> list:

        rating = dict()
        for standings in self.standings_list:
            contest_id = standings.contest.id
            for row in standings.rows:
                handle = row.party.members[0].handle
                problems_solved = round(row.points)

                if handle not in rating:
                    rating[handle] = self.StandingsRow(handle, total_solved=problems_solved)
                else:
                    rating[handle].totalSolved += problems_solved

                def standings_cell(problemResult : ProblemResult):
                    # generates standings cell (+, -1, +5 etc)  by ProblemResult
                    solved = problemResult.points > 0
                    if not solved:
                        if problemResult.rejectedAttemptCount == 0:
                            return ""
                        return f"-{problemResult.rejectedAttemptCount}"
                    if problemResult.rejectedAttemptCount == 0:
                        return "+"
                    return f"+{problemResult.rejectedAttemptCount}"

                problem_names = map(lambda problem : problem.index, standings.problems)
                real_problem_results = map(standings_cell, row.problemResults)
                zipped = list(zip(problem_names, real_problem_results))
                rating[handle].contestsInfo[contest_id] = dict(zipped).copy()

        rating_list = sorted(rating.values(), key = lambda row : row.totalSolved, reverse=True)

        curr_start_idx = -1
        curr_end_idx = -1
        # all rows in [curr_start_idx, curr_end_idx) have same totalSolved
        for i, row in enumerate(rating_list):
            if i >= curr_end_idx:
                curr_start_idx = i
                curr_end_idx = i
                while curr_end_idx < len(rating_list) and rating_list[curr_end_idx].totalSolved == rating_list[curr_start_idx].totalSolved:
                    curr_end_idx += 1
            if curr_start_idx == curr_end_idx - 1:
                row.place=f"{curr_start_idx + 1}"
            else:
                row.place=f"{curr_start_idx + 1}-{curr_end_idx}"

        # returns tabls sorted by total_solved
        return rating_list

    def to_html(self, styles_path) -> str:
        print(self.get_rating())
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

                    rating = self.get_rating()
                    with tag("tbody"):
                        for row in rating:
                            with tag("tr", style="display: table-row"):
                                # place
                                with tag("td", klass="left"):
                                    text(row.place)
                                # handle
                                with tag('td'):
                                    text(row.handle)
                                # total solved
                                with tag('td'):
                                    text(row.totalSolved)
                                for standings in self.standings_list:
                                    # delimeter
                                    with tag('td', klass="_OverallCustomRatingFrame_delimiter"):
                                        pass
                                    contest_id = standings.contest.id
                                    for problem in standings.problems:
                                        problem_result : str = row.contestsInfo.get(contest_id, dict()).get(problem.index, "")
                                        klass = "overall-custom-rating-cell overall-custom-rating-user"
                                        if (problem_result == ""):
                                            klass += "overall-custom-rating-no-attempts "
                                        elif (problem_result.startswith('+')):
                                            klass += "overall-custom-rating-accepted "
                                        elif (problem_result.startswith('-')):
                                            klass += "overall-custom-rating-rejected "
                                        with tag("td", klass=klass):
                                            text(problem_result)



        return doc.getvalue()
