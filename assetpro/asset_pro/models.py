from dataclasses import dataclass


@dataclass
class Asset:
    id: str
    name: str
    category: str
    value: float
    status: str = "active"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "value": self.value,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Asset":
        return cls(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            value=float(data["value"]),
            status=data.get("status", "active"),
        )
