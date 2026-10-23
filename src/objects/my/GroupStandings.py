from objects.cf.Standings import *
from yattag import Doc
from collections import defaultdict
from objects.my.SoloHandleStandings import *
from objects.my.ContestEssentialTasks import *
from objects.my.Mapping import *
from objects.common import *

# Participant types whose submissions count as made during the contest itself
# (practice and virtual participations are excluded)
IN_CONTEST_PARTICIPANT_TYPES = ("CONTESTANT", "OUT_OF_COMPETITION")

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
        def __init__(self, handle : str, all_standings_list : list[SoloHandleStandings],
                     coffins_by_contest : dict[int, set[str]], banned_problems : dict[int, set[str]]):
            self.handle = handle
            self.bannedProblems = banned_problems
            # Banned results are shown in the table but not counted in totals
            standings_list = []
            for standings in all_standings_list:
                contest_banned_problems = banned_problems.get(standings.contest.id, set())
                counted = [
                    (problem, problemResult)
                    for problem, problemResult in zip(standings.problems, standings.problemResults)
                    if problem.index not in contest_banned_problems
                ]
                standings_list.append(SoloHandleStandings(
                    standings.contest,
                    [problem for problem, _ in counted],
                    [problemResult for _, problemResult in counted]
                ))
            self.totalSolved = sum(
                round(problemResult.points)
                for standings in standings_list
                for problemResult in standings.problemResults
            )

            # Total number of wrong (rejected) submissions across all contests,
            # counted only for problems that were eventually solved
            self.totalPenalty = sum(
                problemResult.rejectedAttemptCount or 0
                for standings in standings_list
                for problemResult in standings.problemResults
                if (problemResult.points or 0) > 0
            )

            # Number of upsolved problems: solved after the end of the contest (e.g. in practice mode)
            self.totalUpsolved = sum(
                1
                for standings in standings_list
                for problemResult in standings.problemResults
                if (problemResult.points or 0) > 0
                and problemResult.bestSubmissionTimeSeconds is not None
                and standings.contest.durationSeconds is not None
                and problemResult.bestSubmissionTimeSeconds > standings.contest.durationSeconds
            )

            # Number of solved "coffins": problems that nobody solved before the end of the contest
            self.totalCoffins = len([
                problem
                for standings in standings_list
                for problem, problemResult in zip(standings.problems, standings.problemResults)
                if (problemResult.points or 0) > 0
                and problem.index in coffins_by_contest.get(standings.contest.id, set())
            ])

            self.contestsInfo = {
                standings.contest.id : dict(
                    list(
                        zip(
                            [problem.index for problem in standings.problems],
                            map(standings_cell, standings.problemResults)
                        )
                    )
                )
                for standings in all_standings_list
            }

        def __str__(self):
            return (f"Row(handle={self.handle}, total_solved={self.totalSolved}, "
                    f"total_penalty={self.totalPenalty}, total_upsolved={self.totalUpsolved}, "
                    f"total_coffins={self.totalCoffins}, banned_problems={self.bannedProblems}, "
                    f"contests_info={self.contestsInfo})")

        def __repr__(self):
            return self.__str__()


    def __init__(self, group_id : str, standings_list : list[Standings]):
        self.group_id = group_id
        self.standings_list = standings_list
        self.essential_tasks_by_contest = None
        self.mapping = None
        # Gives banned problem indices by handle and contest id
        self.banned_problems_by_handle = dict()
        problem_results_by_handle_and_contest = defaultdict(dict)
        contest_problems = defaultdict(list)
        contest_by_id = dict()
        # (contest id, problem index) pairs solved by someone during the contest itself
        solved_in_contest = set()

        standings_without_start_time = list(
            filter(
                lambda standings: standings.contest.startTimeSeconds is None,
                standings_list
            )
        )

        if len(standings_without_start_time) == 0:
            logger.info(f"Start time set for all contests; sort them byt it")
            standings_list.sort(key = lambda standings : standings.contest.startTimeSeconds, reverse=True)
        else:
            contest_ids = [standings.contest.id for standings in standings_without_start_time]
            logger.warning(f"Start time does not set for some contests: {contest_ids}); sort contests by id")
            standings_list.sort(key = lambda standings : standings.contest.id, reverse=True)

        for standings in standings_list:
            for row in standings.rows:
                contest = standings.contest
                contest_id = contest.id

                if (contest.type != "ICPC"):
                    logger.warning(f"Found contest {contest_id} with type that differs from ICPC ({contest.type})")

                contest_problems[contest_id] = standings.problems
                contest_by_id[contest_id] = contest
                if row.party.participantType in IN_CONTEST_PARTICIPANT_TYPES:
                    for problem, problem_result in zip(standings.problems, row.problemResults):
                        if (problem_result.points or 0) > 0:
                            solved_in_contest.add((contest_id, problem.index))

                handle = row.get_handle()

                if handle is None:
                    continue

                if contest_id not in problem_results_by_handle_and_contest[handle]:
                    problem_results_by_handle_and_contest[handle][contest_id] = row.problemResults
                else:
                    for i in range(len(row.problemResults)):
                        problem_results_by_handle_and_contest[handle][contest_id][i] += row.problemResults[i]

        self.problem_results_by_handle_and_contest = problem_results_by_handle_and_contest
        self.contest_problems = contest_problems
        self.contest_by_id = contest_by_id

        # "Coffin" is a problem that nobody solved before the end of the contest.
        # While the contest is not finished yet, no problem is considered a coffin
        self.coffins_by_contest = {
            contest_id : {
                problem.index
                for problem in problems
                if (contest_id, problem.index) not in solved_in_contest
            }
            for contest_id, problems in contest_problems.items()
            if contest_by_id[contest_id].phase not in ("BEFORE", "CODING")
        }

        self.build_rows()

    def build_rows(self):
        """
        Computes presenters and standings rows; results in banned contests are not taken into account
        """
        # For each (contest, problem) picks the handle that should present it at the review:
        # the one who solved it with the fewest wrong attempts, and on a tie, the one who solved it first
        self.presenter_by_contest_and_problem = defaultdict(dict)
        for contest_id, problems in self.contest_problems.items():
            for problem_idx, problem in enumerate(problems):
                best_handle = None
                best_key = None
                for handle, contest_results in self.problem_results_by_handle_and_contest.items():
                    problem_results = contest_results.get(contest_id)
                    if problem_results is None:
                        continue
                    if problem.index in self.banned_problems_by_handle.get(handle, dict()).get(contest_id, set()):
                        continue
                    problem_result = problem_results[problem_idx]
                    if (problem_result.points or 0) <= 0:
                        continue
                    key = (
                        problem_result.rejectedAttemptCount or 0,
                        problem_result.bestSubmissionTimeSeconds
                        if problem_result.bestSubmissionTimeSeconds is not None
                        else float("inf"),
                    )
                    if best_key is None or key < best_key:
                        best_key = key
                        best_handle = handle
                self.presenter_by_contest_and_problem[contest_id][problem.index] = best_handle

        self.rows = sorted(list(
            self.StandingsRow(
                    handle,
                    list(
                        SoloHandleStandings(
                            self.contest_by_id[contest_id],
                            self.contest_problems[contest_id],
                            problemResults
                        )
                        for contest_id, problemResults in contest_results.items()
                    ),
                    self.coffins_by_contest,
                    self.banned_problems_by_handle.get(handle, dict())
                )
                for handle, contest_results in self.problem_results_by_handle_and_contest.items()
            ),
            # More solved is better; on a tie, less penalty is better;
            # on a further tie, fewer upsolved (post-contest) problems is better
            key = lambda row : (-row.totalSolved, row.totalPenalty, row.totalUpsolved)
        )

    def add_essential_tasks(self, essential_tasks : list[ContestEssentialTasks]):
        self.essential_tasks_by_contest = {
            item.contestId : item.essential_tasks
            for item in essential_tasks
        }

    def has_unclosed_essential_tasks(self, handle : str, contest_id : int) -> bool:
        """
        Returns True if handle has at least one not solved essential task in given contest
        """
        essential_tasks = self.essential_tasks_by_contest.get(contest_id, dict()).get(handle, list())
        problem_results = self.problem_results_by_handle_and_contest[handle].get(contest_id, list())
        solved = {
            problem.index
            for problem, problem_result in zip(self.contest_problems[contest_id], problem_results)
            if (problem_result.points or 0) > 0
        }
        return any(task not in solved for task in essential_tasks)

    def submission_time(self, contest_id : int, problem_result : ProblemResult) -> int | None:
        """
        Returns absolute time (unix seconds) of the best submission; falls back to contest start time
        if submission time is unknown (e.g. problem is not solved)
        """
        start_time = self.contest_by_id[contest_id].startTimeSeconds
        if start_time is None:
            return None
        return start_time + (problem_result.bestSubmissionTimeSeconds or 0)

    def ban_after_unclosed_essential_tasks(self, since_seconds : int | None = None):
        """
        If handle has unclosed essential task in some contest, all its results in subsequent contests are banned:
        they are not counted in totals and are shown black. Submissions to essential tasks are never banned.
        If since_seconds is set, only submissions made at this time (unix seconds) or later are banned
        """
        if self.essential_tasks_by_contest is None:
            logger.warning("Essential tasks are not set; nothing to ban")
            return

        # standings_list is sorted from the newest contest to the oldest one
        contest_ids = [standings.contest.id for standings in reversed(self.standings_list)]
        self.banned_problems_by_handle = dict()
        for handle, contest_results in self.problem_results_by_handle_and_contest.items():
            for i, contest_id in enumerate(contest_ids):
                if not self.has_unclosed_essential_tasks(handle, contest_id):
                    continue
                banned_problems = dict()
                for banned_contest_id in contest_ids[i + 1:]:
                    problem_results = contest_results.get(banned_contest_id, list())
                    essential_tasks = self.essential_tasks_by_contest.get(banned_contest_id, dict()).get(handle, list())
                    banned_problems[banned_contest_id] = set()
                    for problem, problem_result in zip(self.contest_problems[banned_contest_id], problem_results):
                        if standings_cell(problem_result) == "":
                            continue
                        # upsolving of essential tasks is always counted
                        if problem.index in essential_tasks:
                            continue
                        time = self.submission_time(banned_contest_id, problem_result)
                        # submission with unknown time is banned
                        if since_seconds is None or time is None or time >= since_seconds:
                            banned_problems[banned_contest_id].add(problem.index)
                self.banned_problems_by_handle[handle] = banned_problems
                break
        logger.info(f"Banned problems: {self.banned_problems_by_handle}")

        self.build_rows()

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
                    text('Сводная таблица')
                with tag('link', rel='stylesheet', href=styles_path):
                    pass

            with tag('body'):
                with tag('h1', style="text-align: center"):
                    text('Сводная таблица ')

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
                            with tag('th', rowspan=2):
                                text("Штраф")
                            with tag('th', rowspan=2):
                                text("Дорешано")

                            for standings in self.standings_list:
                                with tag('th', klass="_OverallCustomRatingFrame_delimiter top", rowspan=2):
                                    pass
                                with tag('th', klass="top", colspan=len(standings.problems)):
                                    # Contest name
                                    contest = standings.contest
                                    with tag('a', href=get_contest_url(self.group_id, contest.id), klass = "fancy-link"):
                                        text(contest.name)

                        # Row with problem indexes
                        with tag('tr', style="display: table-row"):
                            for standings in self.standings_list:
                                contest = standings.contest
                                contest_coffins = self.coffins_by_contest.get(contest.id, set())
                                for problem in standings.problems:
                                    with tag('th', klass="coffin" if problem.index in contest_coffins else ""):
                                        with tag('a', href = get_problem_url(self.group_id, contest.id, problem.index), klass = "fancy-link"):
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
                                            view_name += (f" ({self.mapping.name_by_handle[handle]})")

                                    with tag('a', href=get_link_to_profile(handle), klass = "fancy-link"):
                                        text(view_name)
                                    # one coffin per solved coffin (problem nobody solved during the contest)
                                    if row.totalCoffins > 0:
                                        with tag('span', klass="coffins-badge", title=f"Решено гробов: {row.totalCoffins}"):
                                            text("⚰️" * row.totalCoffins)
                                # total solved
                                with tag('td', style="font-weight: bold; text-align : center"):
                                    text(row.totalSolved)
                                # total penalty (wrong submissions count)
                                with tag('td', style="text-align : center"):
                                    text(row.totalPenalty)
                                # total upsolved problems (solved after contest end)
                                with tag('td', style="text-align : center"):
                                    text(row.totalUpsolved)
                                for standings in self.standings_list:
                                    # delimeter
                                    with tag('td', klass="_OverallCustomRatingFrame_delimiter"):
                                        pass
                                    contest_id = standings.contest.id
                                    contest_essential_tasks = self.essential_tasks_by_contest.get(contest_id, dict())
                                    contest_coffins = self.coffins_by_contest.get(contest_id, set())
                                    for problem in standings.problems:
                                        problem_result : str = row.contestsInfo.get(contest_id, dict()).get(problem.index, "")
                                        klass = "overall-custom-rating-cell "

                                        is_essential = problem.index in contest_essential_tasks.get(row.handle, list())
                                        is_accepted = problem_result.startswith('+')
                                        is_coffin = problem.index in contest_coffins
                                        is_presenter = self.presenter_by_contest_and_problem.get(contest_id, dict()).get(problem.index) == row.handle
                                        is_banned = problem.index in row.bannedProblems.get(contest_id, set())

                                        if is_banned:
                                            # submissions after unclosed essential task are not counted
                                            klass += "banned "
                                        elif is_coffin:
                                            # coffin column is black; solved coffin is shown with a bold black plus
                                            klass += "coffin-accepted " if is_accepted else "coffin "
                                        elif is_essential:
                                            if is_accepted:
                                                klass += "essential-accepted "
                                            else:
                                                klass += "essential-not-accepted "
                                        elif is_accepted:
                                            klass += "not-essential-accepted "

                                        if is_presenter:
                                            klass += "presenter-cell "

                                        # Problem result
                                        with tag("td", klass=klass):
                                            text(problem_result)
                                            if is_presenter:
                                                with tag("span", klass="presenter-icon", title="Рассказывает эту задачу"):
                                                    text("🎤")



        return doc.getvalue()
