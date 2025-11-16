from dotenv import load_dotenv
import argparse

from queries.contest_list import *
from queries.contest_standings import *
from objects.my.GroupStandings import *
from objects.my.ContestEssentialTasks import *
from objects.my.Mapping import *
from common import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

def parse_arguments():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-g", "--group", help="Id of codeforces group", required=True)
    parser.add_argument("-o", "--output_directory",
                        help="Output directory (html and css files). Default - value of codeforces group code")
    parser.add_argument("-e", "--essential_tasks_config",
                        help="Path to essential tasks config. See its format in configs/essential_tasks/README.md")
    parser.add_argument("-i", "--ignored_contests",
                        help="Path to file with list of ignored contests ids. Ids should be written by one in line")

    parser.add_argument("-m", "--mapping",
                        help="Path to file with csv table that maps codeforces handles to names")

    return parser.parse_args()

def read_ignored_contests(path : str):
    result = set()
    with open(path, "r") as f:
        try:
            result = set(map(int, f.readlines()))
        except ValueError as e:
            raise ValueError(f"Coudld not interpret one of line in filw with ignored contest ids list: {e}")
    return result
def main():
    load_dotenv()
    args = parse_arguments()
    group_code = args.group
    out_dir = f"{group_code}"
    if args.output_directory is not None:
        out_dir = args.output_directory

    ignored_contests_file = args.ignored_contests
    ignored_contests_ids = read_ignored_contests(ignored_contests_file) if ignored_contests_file is not None else []

    logger.info(f"Ignored contests list: {ignored_contests_ids}")

    contests = list(
        filter(
            lambda contest : contest.id not in ignored_contests_ids,
            get_contest_list(group_code)
        )
    )
    standings_list = list(
        filter(
            lambda x : x is not None,
            [get_contest_standings(contest.id) for contest in contests]
        )
    )

    groupStandings = GroupStandings(group_code, standings_list)

    essential_tasks_config = args.essential_tasks_config
    if essential_tasks_config is not None:
        essential_tasks_list = parse_essential_tasks_config(essential_tasks_config)
        logger.info(f"Parsed essential tasks: {essential_tasks_list}")
        groupStandings.add_essential_tasks(essential_tasks_list)

    mapping_path = args.mapping
    if mapping_path is not None:
        mapping = parse_mapping_from_csv(mapping_path)
        logger.info(f"Parsed mapping {mapping}")
        groupStandings.add_mapping(mapping)

    copy_file(os.path.join(PROJECT_ROOT, "configs", "styles.css"), out_dir)
    css_out_path = "styles.css"

    html = groupStandings.to_html(css_out_path)

    html_out_path = os.path.join(out_dir, "index.html")
    with open(html_out_path, "w", encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    main()
