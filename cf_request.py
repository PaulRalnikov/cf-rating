import requests
import os
import time
import random
import string
import hashlib

def cf_request(methodName : str, params : dict) -> requests.Response:
    apiKey = os.getenv("API_KEY")
    apiSecret = os.getenv("API_SECRET")

    params["apiKey"] = apiKey

    now = round(time.time())
    params["time"] = str(now)

    # Generate rand
    characters = string.ascii_letters + string.digits
    rand = ''.join(random.choice(characters) for _ in range(6))

    # Generate string for sha-512
    sorted_items = sorted(params.items())
    item_to_str = lambda keyvalue : f"{keyvalue[0]}={keyvalue[1]}"
    forShaStr = f"{rand}/{methodName}?" + '&'.join(map(item_to_str, sorted_items)) + f"#{apiSecret}"

    # calc hash
    sha512_hash = hashlib.sha512()
    sha512_hash.update(forShaStr.encode('utf-8'))
    apiSig = rand + str(sha512_hash.hexdigest())

    params["apiSig"] = apiSig

    API_PREFIX = "https://codeforces.com/api/"
    return requests.get(API_PREFIX + methodName, params=params)
