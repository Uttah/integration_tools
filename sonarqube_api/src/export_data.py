def extract_name_project_mapping(data):
    return {component['name']: component['project'] for component in data['components']}
