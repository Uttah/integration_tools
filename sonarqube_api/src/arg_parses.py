import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Sonarqube API')

    parser.add_argument('--gitlab_project_key', type=str,
                        required=False, help='Gitlab project path like wnf/infrastructure/<your_project>')
    parser.add_argument('--is_create_project', type=bool,
                        required=False, help='Create project in sonarqube', default=False)
    parser.add_argument('--is_create_binding', type=bool,
                        required=False, help='Create binding in sonarqube', default=False)
    parser.add_argument('--almsetting', type=str,
                        required=False, help='ALM setting', default='Gitlab')
    parser.add_argument('--monorepo', type=str,
                        required=False, help='Monorepo', default='false')
    parser.add_argument('--project_key', type=str,
                        required=False, help='Project key')
    parser.add_argument('--repo_url', type=str,
                        required=False, help='Repository URL')
    parser.add_argument('--is_list_all', type=bool,
                        required=False, help='List all components', default=False)

    return parser.parse_args()
