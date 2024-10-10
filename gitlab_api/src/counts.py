from typing import Dict, List, Any
from src.config import ClientConfig
from datetime import datetime, timedelta
import gitlab


def collect_projects_in_group_json(group: 'gitlab.Group', client: 'gitlab.Gitlab') -> Dict[str, Any]:
    '''
    Collects information about projects in a group and its subgroups
    Returns a dictionary with the following structure:
    {
        "group_name": str,
        "projects": List[{
            "id": int,
            "name": str,
            "path_with_namespace": str
        }],
        "subgroups": List[{
            "group_name": str,
            "projects": List[{
                "id": int,
                "name": str,
                "path_with_namespace": str
            }],
            "subgroups": List[{
                "group_name": str,
                "projects": List[{
                    "id": int,
                    "name": str,
                    "path_with_namespace": str
                }],
                "subgroups": ...
            }]
        }]
    }
    '''
    group_info: Dict[str, Any] = {
        "group_name": group.full_path,
        "projects": [],
        "subgroups": []
    }

    page: int = 1
    per_page: int = 100

    while True:
        projects = group.projects.list(page=page, per_page=per_page)
        if not projects:
            break

        for project in projects:
            group_info["projects"].append({
                "id": project.id,
                "name": project.name,
                "path_with_namespace": project.path_with_namespace
            })

        page += 1

    subgroups = group.subgroups.list(all=True)

    for subgroup in subgroups:
        subgroup_detail = client.groups.get(subgroup.id)
        group_info["subgroups"].append(
            collect_projects_in_group_json(subgroup_detail, client))

    return group_info


def collect_projects_in_group(group: 'gitlab.Group', client: 'gitlab.Gitlab', level: int = 0) -> str:
    '''
    Collects information about projects in a group and its subgroups
    Returns a string with the following structure:
    Группа: group_name
      Проекты:
        - ID: project_id, Название: project_name, Путь: project_path
      Подгруппы:
        Группа: subgroup_name
          Проекты:
            - ID: project_id, Название: project_name, Путь: project_path
          Подгруппы:
    '''
    indent = '  ' * level
    output = f"{indent}Группа: {group.full_path}\n"

    projects = group.projects.list(all=True)
    if projects:
        output += f"{indent}Проекты:\n"
        for project in projects:
            output += (
                f"{indent}    - ID: {project.id}, Название: {project.name}, "
                f"Путь: {project.path_with_namespace}\n"
            )

    subgroups = group.subgroups.list(all=True)
    if subgroups:
        output += f"{indent}Подгруппы:\n"
        for subgroup in subgroups:
            subgroup_detail = client.groups.get(subgroup.id)
            output += collect_projects_in_group(
                subgroup_detail, client, level + 1)

    return output


def collect_project_paths(group: 'gitlab.Group', client: 'gitlab.Gitlab') -> Dict[int, str]:
    '''
    Collects all project paths in a GitLab group.
    Returns a dictionary with the following structure:
    {
        project_id: project_path
    }
    '''
    project_paths = {}

    projects = group.projects.list(all=True)
    for project in projects:
        project_paths[project.id] = project.path_with_namespace

    subgroups = group.subgroups.list(all=True)
    for subgroup in subgroups:
        subgroup_detail = client.groups.get(subgroup.id)
        project_paths.update(collect_project_paths(subgroup_detail, client))

    return project_paths


def collect_last_activity_date(group: 'gitlab.Group', client: 'gitlab.Gitlab') -> Dict[str, str]:
    '''
    Collects the last activity date for each project in a GitLab group.
    Returns a dictionary with the following structure:
    {
        project_path: last_activity_at
    }
    '''
    last_activity_dates = {}

    projects = group.projects.list(all=True)
    for project in projects:
        last_activity_dates[project.path_with_namespace] = project.last_activity_at

    subgroups = group.subgroups.list(all=True)
    for subgroup in subgroups:
        subgroup_detail = client.groups.get(subgroup.id)
        last_activity_dates.update(
            collect_last_activity_date(subgroup_detail, client))

    return last_activity_dates


def filter_recent_projects(project_paths: Dict[str, str], days: int = 30) -> Dict[str, str]:
    '''
    Filters projects that have had activity within the last `days` days.
    Returns a dictionary with the following structure:
    {
        project_path: last_activity_date
    }
    '''
    recent_projects = {}
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    for project_path, last_activity in project_paths.items():
        last_activity_date = datetime.strptime(
            last_activity, '%Y-%m-%dT%H:%M:%S.%fZ')

        if last_activity_date > cutoff_date:
            recent_projects[project_path] = last_activity

    return recent_projects
