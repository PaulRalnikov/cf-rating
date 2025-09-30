from objects.cf.Standings import *
from yattag import Doc
from collections import defaultdict
from objects.my.SoloHandleStandings import *
from objects.my.ContestEssentialTasks import *
from objects.my.Mapping import *

def standings_cell(problemResult : ProblemResult) -> str:
    # generates standings cell (+, -1, +5 etc)  by ProblemResult
    solved = problemResult.points > 0
    if not solved:
        if problemResult.rejectedAttemptCount == 0:
            return ""
        return f"-{problemResult.rejectedAttemptCount}"
    if problemResult.rejectedAttemptCount == 0:
        return "+"
    return f"+{problemResult.rejectedAttemptCount}"

class GroupStandings:
    class StandingsRow:
        def __init__(self, handle : str, standings_list : list[SoloHandleStandings]):
            self.handle = handle
            self.totalSolved = sum(
                round(problemResult.points)
                for standings in standings_list
                for problemResult in standings.problemResults
            )

            self.contestsInfo = {
                standings.contest.id : dict(
                    list(
                        zip(
                            [problem.index for problem in standings.problems],
                            map(standings_cell, standings.problemResults)
                        )
                    )
                )
                for standings in standings_list
            }

        def __str__(self):
            return f"Row(handle={self.handle}, total_solved={self.totalSolved}, contests_info={self.contestsInfo})"

        def __repr__(self):
            return self.__str__()


    def __init__(self, standings_list : list[Standings]):
        self.standings_list = standings_list
        self.essential_tasks_by_contest = None
        self.mapping = None
        problem_results_by_handle_and_contest = defaultdict(dict)
        contest_problems = defaultdict(list)
        contest_by_id = dict()
        for standings in sorted(standings_list, key = lambda standings : standings.contest.startTimeSeconds):
            for row in standings.rows:
                contest_id = standings.contest.id
                contest_problems[contest_id] = standings.problems
                contest_by_id[contest_id] = standings.contest
                handle = row.get_handle()

                if contest_id not in problem_results_by_handle_and_contest[handle]:
                    problem_results_by_handle_and_contest[handle][contest_id] = row.problemResults
                else:
                    for i in range(len(row.problemResults)):
                        problem_results_by_handle_and_contest[handle][contest_id][i] += row.problemResults[i]
        self.rows = sorted(list(
            self.StandingsRow(
                    handle,
                    list(
                        SoloHandleStandings(
                            contest_by_id[contest_id],
                            contest_problems[contest_id],
                            problemResults
                        )
                        for contest_id, problemResults in contest_results.items()
                    )
                )
                for handle, contest_results in problem_results_by_handle_and_contest.items()
            ),
            key = lambda row : row.totalSolved,
            reverse=True
        )

    def add_essential_tasks(self, essential_tasks : list[ContestEssentialTasks]):
        self.essential_tasks_by_contest = {
            item.contestId : item.essential_tasks
            for item in essential_tasks
        }

    def add_mapping(self, mapping : Mapping):
        self.mapping = mapping


    def get_places(self) -> dict[str, str]:
        """
        Returns mapping handles to its places
        """
        # all rows in [curr_start_idx, curr_end_idx) have same totalSolved
        curr_start_idx = -1
        curr_end_idx = -1
        place_by_handle = dict()
        for i, item in enumerate(self.rows):
            handle, solved = item.handle, item.totalSolved
            if i >= curr_end_idx:
                curr_start_idx = i
                curr_end_idx = i
                while curr_end_idx < len(self.rows) and self.rows[curr_end_idx].totalSolved == solved:
                    curr_end_idx += 1
            if curr_start_idx == curr_end_idx - 1:
                place_by_handle[handle] = f"{curr_start_idx + 1}"
            else:
                place_by_handle[handle] = f"{curr_start_idx + 1}-{curr_end_idx}"
        return place_by_handle

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
                                    # Contest name
                                    text(standings.contest.name)

                        # Row with problem indexes
                        with tag('tr', style="display: table-row"):
                            for standings in self.standings_list:
                                for problem in standings.problems:
                                    with tag('th'):
                                        with tag('span'):
                                            # Problem symbol (A, B, C etc)
                                            text(problem.index)

                    place_by_handle = self.get_places()
                    with tag("tbody"):
                        for row in self.rows:
                            with tag("tr", style="display: table-row"):
                                # place
                                with tag("td", klass="left"):
                                    text(place_by_handle[row.handle])
                                # handle
                                with tag('td'):
                                    handle = row.handle
                                    view_name = handle
                                    if self.mapping is not None:
                                        if handle in self.mapping.name_by_handle:
                                            view_name += f" ({self.mapping.name_by_handle[handle]})"
                                    text(view_name)
                                # total solved
                                with tag('td'):
                                    text(row.totalSolved)
                                for standings in self.standings_list:
                                    # delimeter
                                    with tag('td', klass="_OverallCustomRatingFrame_delimiter"):
                                        pass
                                    contest_id = standings.contest.id
                                    contest_essential_tasks = self.essential_tasks_by_contest.get(contest_id, dict())
                                    for problem in standings.problems:
                                        problem_result : str = row.contestsInfo.get(contest_id, dict()).get(problem.index, "")
                                        klass = "overall-custom-rating-cell overall-custom-rating-user "
                                        if not problem_result.startswith('+') and problem.index in contest_essential_tasks.get(row.handle, list()):
                                            klass+="essential-task "
                                        # Problem result
                                        with tag("td", klass=klass):
                                            text(problem_result)



        return doc.getvalue()
