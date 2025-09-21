import os
import pandas as pd
from collections import defaultdict

class EssentialTasks:
    def __init__(self, contestId : int, essential_tasks : dict[str, list[str]]):
        self.contestId = contestId
        # Gives problem ids by handle
        self.essential_tasks = essential_tasks


def essential_tasks_from_csv(path : str, contestId = None) -> EssentialTasks:
    """
    Returns EssentialTasks object, parsed from given path
    If contestId is none, name of file will be used
    """
    if contestId is None:
        contestId = int(os.path.splitext(os.path.basename(path))[0])
    essential_tasks = defaultdict(list)
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        handle = str(row[0])
        for task_id, value in list(zip(df.columns, row))[1:]:
            if pd.notna(value):
                essential_tasks[handle].append(str(task_id))
    return EssentialTasks(contestId, essential_tasks)
