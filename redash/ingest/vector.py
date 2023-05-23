import os
from functools import lru_cache
from pathlib import Path
import toml

VECTOR_CONFIG_TEMPLATE = '''
data_dir = "/var/lib/vector"

[api]
enabled = true

[sources.apps_logs]
type = "http_server"
address = "0.0.0.0:8180"
method = "POST"
decoding.codec = "json"

[sinks.print]
type = "console"
# inputs = ["parse_logs", "apps_logs"]
inputs = ["apps_logs"]
encoding.codec = "json"
'''


@lru_cache
def get_vector_config() -> 'VectorIngestConfig':
    config_path = os.environ.get('VECTOR_CONFIG_PATH') or 'vector.toml'
    return VectorIngestConfig(config_path)


class VectorIngestConfig:
    def __init__(self, config_path: str) -> None:
        self.config_path = Path(config_path)
        self.config = toml.loads(VECTOR_CONFIG_TEMPLATE)

    def load(self) -> None:
        if self.config_path.exists():
            with open(self.config_path) as f:
                self.config = toml.load(f)

    def save(self) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            toml.dump(self.config, f)
