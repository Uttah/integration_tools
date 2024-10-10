import yaml
from pydantic import BaseModel
from typing import Optional, Dict


class ClientConfig(BaseModel):
    sonar_url: str
    sonar_token: str

    @classmethod
    def load_config(cls, path: Optional[str] = 'config.yaml') -> 'ClientConfig':
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        return cls(**config)
