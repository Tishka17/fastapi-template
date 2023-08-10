from dataclasses import dataclass, field


@dataclass
class User:
    id: int = field(init=False)
    name: str
