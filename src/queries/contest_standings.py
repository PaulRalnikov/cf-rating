from queries.cf_request import *
from objects.cf.Standings import *
import logging

logger = logging.getLogger(__name__)

def get_contest_standings(contest_id : str) -> Standings:
    responce = cf_request('contest.standings', {
        "contestId": contest_id,
        "asManager": True,
        "showUnofficial" : True
    })
    if (responce.status_code == 429):
        MAX_RETRIES = 3
        for i in range (MAX_RETRIES):
            time.sleep(i * 2) # sleep more and more with every new request
            responce = cf_request('contest.standings', {
                "contestId": contest_id,
                "asManager": True,
                "showUnofficial" : True
            })
            if responce.status_code == 200:
                break

    if (responce.status_code != 200):
        logger.error(f"Can not get standings for contest {contest_id}; returned status code {responce.status_code}")
        return None
    body = responce.json()
    if body["status"] != "OK":
        logger.error(f"Can not get standings for contest {contest_id}; body: {body}")
        return None

    return Standings(body["result"])
