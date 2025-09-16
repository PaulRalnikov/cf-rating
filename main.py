from dotenv import load_dotenv
import sys
from queries.contest_list import *
from queries.contest_standings import *
from GroupStandings.GroupStandings import *

def main(args):
    load_dotenv()
    if (len(args) < 2):
        print(f"Passed {len(args) - 1} arguments, expected at least one")
        exit(-1)
    group_code = args[1]
    out_file = f"{group_code}.html"
    if len(args) > 2:
        out_file = args[2]

    contests = get_contest_list(group_code)
    standings_list = [get_contest_standings(contest.id) for contest in contests]

    for el in standings_list:
        print(el)
        print()

    groupStandings = GroupStandings(standings_list)

    html = groupStandings.to_html("GroupStandings\\styles.css")
    with open(out_file, "w", encoding='utf-8') as f:
        f.write(html)


if __name__ == "__main__":
    main(sys.argv)
