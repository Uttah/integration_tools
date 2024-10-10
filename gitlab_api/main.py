import gitlab
import json
from src.config import load_config
from src.params import parse_args
from src.counts import (
    collect_projects_in_group,
    collect_project_paths,
    collect_projects_in_group_json,
    collect_last_activity_date,
    filter_recent_projects
)


def main():
    args = parse_args()

    output_format = args.output
    activity = args.activity
    days = args.since

    config = load_config()
    client = gitlab.Gitlab(
        str(config.gitlab_url), private_token=config.private_token)
    group = client.groups.get(config.group_path)

    if output_format == 'json':  # example: venv/bin/python main.py --output=json
        group_data: Dict[str, Any] = {}
        group_data = collect_projects_in_group_json(group, client)
        json_output: str = json.dumps(group_data, indent=4, ensure_ascii=False)
        print(json_output)

    if output_format == 'string':  # example: venv/bin/python main.py --output=string
        project_info = collect_projects_in_group(group, client)
        print(project_info)

    if output_format == 'simple':  # example: venv/bin/python main.py --output=simple
        project_paths_dict = collect_project_paths(group, client)
        print(project_paths_dict)
        print(len(project_paths_dict))

    if activity:  # example: venv/bin/python main.py --activity=true --since=90
        projects = collect_last_activity_date(group, client)
        filtered_projects = filter_recent_projects(projects, days)
        for k, v in filtered_projects.items():
            print(f"{k}: {v}")
        print(f'Numbers of filetered projects is -- {len(filtered_projects)}')
        print(f'Numbers of all projects in the group is -- {len(projects)}')


if __name__ == '__main__':
    main()
