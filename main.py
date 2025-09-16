from dotenv import load_dotenv
from cf_request import *

def main():
    load_dotenv()
    r = cf_request('contest.hacks', {
        "contestId": "566",
        "asManager": "false"
    })
    print(r.status_code)
    print(r.json())

if __name__ == "__main__":
    main()
