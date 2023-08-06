from dataclasses import dataclass, field
from typing import Any, List, Mapping


@dataclass(frozen=True)
class KubeCluster:
    name: str
    cluster: Mapping[str, str]


@dataclass(frozen=True)
class KubeUser:
    name: str
    user: Mapping[str, Any]


@dataclass(frozen=True)
class KubeContext:
    name: str
    context: Mapping[str, str]


@dataclass(frozen=True)
class KubeConfig:
    apiVersion: str = "v1"
    kind: str = "Config"
    preferences: Mapping[str, str] = {}
    clusters: List[KubeCluster] = field(default_factory=list)
    users: List[KubeUser] = field(default_factory=list)
    contexts: List[KubeContext] = field(default_factory=list)
