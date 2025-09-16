from dotenv import load_dotenv
import sys
from queries.contest_list import *
from queries.contest_standings import *

def main(args):
    load_dotenv()
    group_codes = args[1:]

    for group_code in group_codes:
        contests = get_contest_list(group_code)
        for contest in contests:
            print(contest)
            standings = get_contest_standings(contest.id)
            print(standings)

        print(contests)


if __name__ == "__main__":
    main(sys.argv)
