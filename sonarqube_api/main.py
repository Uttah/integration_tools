from src.sonarqube_api import (
    get_alm_settings,
    create_sonarqube_project,
    get_all_components,
    get_binding,
    set_gitlab_binding
)
from src.config import ClientConfig
from src.arg_parses import parse_args


def main():
    args = parse_args()
    config = ClientConfig.load_config()

    # ALM setting prints devops integrations settings
    alm_settings = get_alm_settings(config)
    if alm_settings:
        print("ALM:")
        print(alm_settings)

    if args.is_list_all:
        # List all components
        try:
            components = get_all_components(config)
            print("Components:")
            for component in components:
                print(component)
        except Exception as e:
            print(f'Error with fetching components: {e}')

    if args.is_create_project and args.gitlab_project_key:
        sonar_project_name = args.gitlab_project_key.split('/')[-1]

        try:
            response = create_sonarqube_project(
                config,
                args.gitlab_project_key,
                sonar_project_name
            )
            project_key = response.get('project', {}).get('key')
            if project_key and args.is_create_binding:
                print(f'Project key: {project_key}')
                try:
                    # Create binding between sonarqube project and gitlab project
                    # Example usage: python3 main.py --is_create_binding=true --project_key=<your_sonarqube_project_key> --repo_url=<your_gitlab_repo_url>
                    # If successful, returns 204 status code
                    response = set_gitlab_binding(
                        config,
                        args.almsetting,
                        args.monorepo,
                        project_key,
                        args.gitlab_project_key
                    )
                    print('Binding set successfully')
                    response = get_binding(config, project_key)
                    print(response)
                except Exception as e:
                    print(f'Error with binding creation: {e}')
            else:
                print('Project key not found in the response')
        except Exception as e:
            print('Failed to create project')


if __name__ == "__main__":
    main()
