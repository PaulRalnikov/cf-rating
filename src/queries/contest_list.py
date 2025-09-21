from queries.cf_request import *
from objects.cf.Contest import *
import logging

logger = logging.getLogger(__name__)

def get_contest_list(group_id : str) -> list:
    responce = cf_request('contest.list', {
        "gym": "true",
        "groupCode": group_id
    })
    if (responce.status_code != 200):
        logger.error(f"Can not get contests for group {group_id}; returned status code {responce.status_code}")
        return []
    body = responce.json()
    if body["status"] != "OK":
        logger.error(f"Can not get contests for group {group_id}; body: {body}")
        return []

    return list(map(Contest, body["result"]))
