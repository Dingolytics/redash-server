from typing import Any
from .vector import VectorIngestConfig, get_vector_config

__all__ = [
    'VectorIngestConfig',
    'get_vector_config',
    'init_app'
]


def init_app(app: Any) -> None:
    # TODO: Add existing streams to vector config
    vector_config = get_vector_config()
    vector_config.save()
