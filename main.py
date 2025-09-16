from dotenv import load_dotenv
from cf_request import *
import sys

def process_group(group_code : str):
    r = cf_request('contest.list', {
        "gym": "true",
        "groupCode": group_code
    })

    print(r.status_code)
    print(r.json())

def main(args):
    load_dotenv()
    group_codes = args[1:]

    for group_code in group_codes:
        process_group(group_code)


if __name__ == "__main__":
    main(sys.argv)
