import os
from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel
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


def update_vector_config(streams: list, clean: bool = False) -> None:
    vector_config = get_vector_config()
    if not clean:
        vector_config.load()
    for stream in streams:
        options = stream.data_source.options.to_dict()
        key = stream.db_table.replace('_', '-').replace('.', '-')
        sink = VectorClickHouseSinkConfig(
            key=f"clickhouse-{key}",
            table=stream.db_table,
            auth=VectorClickHouseAuthConfig(**options),
            endpoint=options["url"],
            database=options["dbname"],
        )
        vector_config.add_sink(sink)
        print(sink)
        # print(stream)
        # print(stream.data_source)
        # print(stream.data_source.options.to_dict())
    vector_config.save()


class VectorClickHouseAuthConfig(BaseModel):
    strategy: str = "basic"
    user: str = "default"
    password: str = ""


class VectorClickHouseSinkConfig(BaseModel):
    key: str
    database: str
    table: str
    type: str = "clickhouse"
    auth: VectorClickHouseAuthConfig = VectorClickHouseAuthConfig()
    inputs: list = ["apps_logs"]
    encoding: dict = {"timestamp_format": "rfc3339"}
    endpoint: str = "http://clickhouse:8123"


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

    def add_sink(self, sink: 'VectorClickHouseSinkConfig') -> None:
        sinks = self.config.setdefault("sinks", {})
        parameters = sink.dict()
        key = parameters.pop("key")
        sinks[key] = parameters
