from typing import Optional, Dict
from src.config import ClientConfig
import requests


def get_alm_settings(config: ClientConfig) -> Optional[Dict]:
    '''
    Returns the list of ALM settings
    Example response:
    {'almSettings': [{'key': 'Gitlab', 'alm': 'gitlab', 'url': 'https://gitlab.com/api/v4'}]}
    '''

    url = f'{config.sonar_url}/api/alm_settings/list'

    response = requests.get(url, auth=(config.sonar_token, ''))

    if response.status_code == 200:
        alm_settings = response.json()
        return alm_settings
    else:
        print(f"ERROR: {response.status_code} - {response.text}")
        return None


def create_sonarqube_project(config: ClientConfig,
                             gitlab_project_key: str,
                             project_name: str,
                             visibility: Optional[str] = 'public') -> Optional[Dict]:
    headers = {
        'Authorization': f'Bearer {config.sonar_token}'
    }

    project_data = {
        'project': gitlab_project_key.replace('/', '-'),
        'name': project_name,
        'visibility': visibility
    }

    response = requests.post(
        f'{config.sonar_url}/api/projects/create', headers=headers, data=project_data)

    if response.status_code == 200:
        print('Project successfully created')
        return response.json()
    else:
        print(f'ERROR: {response.status_code} - {response.text}')
        return None


def count_projects(config: ClientConfig, alm_setting: Optional[str] = 'Gitlab') -> Optional[Dict]:
    '''
    Needs Administer System permission to access this endpoint
    '''

    url = f'{config.sonar_url}/api/alm_settings/count_binding'

    headers = {
        'Authorization': f'Bearer {config.sonar_token}'
    }
    params = {
        'almSetting': alm_setting
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'ERROR: {response.status_code} - {response.text}')
        return None


def components_search(config: ClientConfig,
                      qualifiers: Optional[str] = 'TRK',
                      page: Optional[int] = 1,
                      page_size: Optional[int] = 50) -> Optional[Dict]:
    '''Search for components, page size is 50'''

    url = f'{config.sonar_url}/api/components/search'

    headers = {
        'Authorization': f'Bearer {config.sonar_token}'
    }
    params = {
        'qualifiers': qualifiers,
        'p': page,
        'ps': page_size,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'ERROR: {response.status_code} - {response.text}')
        return None


def get_all_components(config: ClientConfig, qualifiers: Optional[str] = 'TRK') -> Optional[Dict]:
    '''
    Get all components
    Example usage: python3 main.py
    '''

    url = f'{config.sonar_url}/api/components/search'
    all_components = []
    page = 1
    page_size = 50

    while True:
        response = components_search(
            config, qualifiers, page, page_size)

        if response is None:
            break

        all_components.extend(response.get('components', []))
        if len(response['components']) < page_size:
            break

        page += 1

    return all_components


def get_binding(config: ClientConfig, project_key: str) -> Optional[str]:
    '''
    Get repository binding for project
    '''

    url = f'{config.sonar_url}/api/alm_settings/get_binding'
    headers = {
        'Authorization': f'Bearer {config.sonar_token}'
    }
    params = {
        'project': project_key
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'ERROR: {response.status_code} - {response.text}')
        return None


def set_gitlab_binding(config: ClientConfig,
                       almsetting: str,
                       monorepo: bool,
                       project_key: str,
                       repo_url: str) -> Optional[Dict]:
    '''
    Set repository binding for project
    '''

    url = f'{config.sonar_url}/api/alm_settings/set_gitlab_binding'
    headers = {
        'Authorization': f'Bearer {config.sonar_token}'
    }
    data = {
        'almSetting': almsetting,
        'monorepo': monorepo,
        'project': project_key,
        'repository': repo_url
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200 or response.status_code == 204:
        # return response.json()
        return response
    else:
        print(f'ERROR: {response.status_code} - {response.text}')
        return None
