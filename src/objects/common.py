
CODEFORCES_URL = "https://codeforces.com"

def get_contest_url(group_code : str, contest_id : str):
    return f"{CODEFORCES_URL}/group/{group_code}/contest/{contest_id}"

def get_problem_url(group_code : str, contest_id : str, problem_id : str):
    return f"{get_contest_url(group_code, contest_id)}/problem/{problem_id}"

def get_link_to_profile(handle : str):
    return f"{CODEFORCES_URL}/profile/{handle}"
