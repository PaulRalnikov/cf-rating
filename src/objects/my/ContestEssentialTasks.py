import pandas as pd
import os
from collections import defaultdict
from common import *

class ContestEssentialTasks:
    def __init__(self, contestId : int, essential_tasks : dict[str, list[str]]):
        self.contestId = contestId
        # Gives list of problem ids by handle
        self.essential_tasks = essential_tasks


def essential_tasks_from_csv(path : str, contestId) -> ContestEssentialTasks:
    """
    Returns ContestEssentialTasks object, parsed from given path
    """
    essential_tasks = defaultdict(list)
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        handle = str(row[0]).replace(" ", "")
        for task_id, value in list(zip(df.columns, row))[1:]:
            if pd.isna(value):
                continue
            str_value = str(value).replace(" ", "")
            if str_value == '+':
                essential_tasks[handle].append(str(task_id))
    return ContestEssentialTasks(contestId, essential_tasks)

def parse_essential_tasks_config(config_path : str) -> list[ContestEssentialTasks]:
    """
    Reads essential tasks config by given path and returns list of EssentialTasks
    """
    config = load_yaml(config_path)
    config_dir = os.path.dirname(config_path)
    return [
        essential_tasks_from_csv(os.path.join(config_dir, essential_tasks), contest_id)
        for contest_id, essential_tasks
        in config.items()
    ]
