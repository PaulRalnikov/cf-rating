from dotenv import load_dotenv
import shutil
from queries.contest_list import *
from queries.contest_standings import *
from GroupStandings.GroupStandings import *
from EssentialTasks.EssentialTasks import *
import argparse

def copy_file(source_file : str, target_dir : str):
    """Copies suorce_file to target_dir"""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    dest: str = os.path.join(target_dir, os.path.basename(source_file))
    shutil.copy(source_file, dest)

def parse_arguments():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-g", "--group", help="Id of codeforces group", required=True)
    parser.add_argument("-o", "--output_directory",
                        help="Output directory (html and css files). Default - value of codeforces group code")
    parser.add_argument("-e", "--essential_tasks_dir", help="Path to directory with essetial tasks tables")

    return parser.parse_args()

def main():
    load_dotenv()
    args = parse_arguments()
    group_code = args.group
    out_dir = f"{group_code}"
    if args.output_directory is not None:
        out_dir = args.output_directory


    contests = get_contest_list(group_code)
    standings_list = [get_contest_standings(contest.id) for contest in contests]

    groupStandings = GroupStandings(standings_list)

    essential_tasks_dir = args.essential_tasks_dir
    if essential_tasks_dir is not None:
        essential_tasks_list = map(
            essential_tasks_from_csv,
            filter(
                lambda item_path : os.path.isfile(item_path) and item_path.endswith(".csv"),
                map(
                    lambda item : os.path.join(essential_tasks_dir, item),
                    os.listdir(essential_tasks_dir)
                )
            )
        )
        groupStandings.add_essential_tasks(essential_tasks_list)

    copy_file(os.path.join("GroupStandings", "styles.css"), out_dir)
    css_out_path = "styles.css"

    html = groupStandings.to_html(css_out_path)

    html_out_path = os.path.join(out_dir, "index.html")
    with open(html_out_path, "w", encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    main()
