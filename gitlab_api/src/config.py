import yaml
import gitlab
from pydantic import BaseModel, Field, AnyHttpUrl


class ClientConfig(BaseModel):
    gitlab_url: AnyHttpUrl = Field(..., title='GitLab URL',
                                   description='URL of the GitLab instance')
    private_token: str = Field(..., title='Gitlab Private Token',
                               description='Private token for GitLab API')
    group_path: str = Field(..., title='Group Path',
                            description='Path to the GitLab group')


def load_config(file_path: str = 'config.yaml') -> ClientConfig:
    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return ClientConfig(**config_data)
