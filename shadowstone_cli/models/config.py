"""Typed view of shadowstone.yaml. Everything round-trips through plain dicts."""
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Price:
    amount: float = 0.0
    interval: str = "monthly"


@dataclass
class Tier:
    name: str = ""
    prices: List[Price] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tier":
        return cls(name=data.get("name", ""), prices=[Price(**p) for p in data.get("prices", [])])


@dataclass
class OAuth:
    enabled: bool = False
    providers: List[str] = field(default_factory=list)


@dataclass
class Database:
    provider: str = "postgres-docker"  # or "external"


@dataclass
class Billing:
    enabled: bool = False
    provider: Optional[str] = None
    tiers: List[Tier] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Billing":
        return cls(
            enabled=data.get("enabled", False),
            provider=data.get("provider"),
            tiers=[Tier.from_dict(t) for t in data.get("tiers", [])],
        )


@dataclass
class Deployment:
    enabled: bool = False
    provider: str = "coolify"
    description: str = ""


@dataclass
class ProjectConfig:
    project_name: str
    components: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    oauth: OAuth = field(default_factory=OAuth)
    database: Database = field(default_factory=Database)
    billing: Billing = field(default_factory=Billing)
    deployment: Deployment = field(default_factory=Deployment)
    demo: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectConfig":
        return cls(
            project_name=data["project_name"],
            components=dict(data.get("components", {})),
            oauth=OAuth(**data.get("oauth", {})),
            database=Database(**data.get("database", {})),
            billing=Billing.from_dict(data.get("billing", {})),
            deployment=Deployment(**data.get("deployment", {})),
            demo=bool(data.get("demo", False)),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
