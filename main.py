from dotenv import load_dotenv
import sys
import shutil
from queries.contest_list import *
from queries.contest_standings import *
from GroupStandings.GroupStandings import *

def copy_file(source_file : str, target_dir : str):
    """Copies suorce_file to target_dir"""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    dest: str = os.path.join(target_dir, os.path.basename(source_file))
    shutil.copy(source_file, dest)

def main(args):
    load_dotenv()
    if (len(args) < 2):
        print(f"Passed {len(args) - 1} arguments, expected at least one")
        exit(-1)
    group_code = args[1]
    out_dir = f"{group_code}"
    if len(args) > 2:
        out_dir = args[2]

    contests = get_contest_list(group_code)
    standings_list = [get_contest_standings(contest.id) for contest in contests]

    groupStandings = GroupStandings(standings_list)

    copy_file(os.path.join("GroupStandings", "styles.css"), out_dir)
    css_out_path = os.path.join(out_dir, "styles.css")

    html = groupStandings.to_html(css_out_path)

    html_out_path = os.path.join(out_dir, "index.html")
    with open(html_out_path, "w", encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    main(sys.argv)
