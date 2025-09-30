import pandas as pd

class Mapping:
    def __init__(self, name_by_handle : dict[str, str] = dict()):
        self.name_by_handle = name_by_handle

    def __str__(self):
        return self.name_by_handle.__str__()

    def __repr__(self):
        return self.name_by_handle.__repr__()

def parse_mapping_from_csv(path : str) -> Mapping:
    df = pd.read_csv(path)
    name_by_handle = dict()
    if len(df.columns) != 2:
        print(f"Strange mapping table with {len(df.columns)} columns; excepted 2")
        return Mapping()
    for _, row in df.iterrows():
        handle = str(row[0]).replace(" ", "")
        name = str(row[1])
        if handle in name_by_handle:
            print(f"Copy of handle (old value `{name_by_handle[handle]}`, new one - `{name}`); ignored")
        else:
            name_by_handle[handle] = name
    return Mapping(name_by_handle)

