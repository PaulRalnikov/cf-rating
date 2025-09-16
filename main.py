from dotenv import load_dotenv
import sys
from queries.contest_list import *
from queries.contest_standings import *

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
    for contest in contests:
        print(contest)
        standings = get_contest_standings(contest.id)
        print(standings)

    with open(out_file, "w") as f:
        f.write(str(contests))


if __name__ == "__main__":
    main(sys.argv)
