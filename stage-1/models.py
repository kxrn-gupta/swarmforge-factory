"""
Stage 1: Core Foundation & Data Models for SwarmForge Dark Factory.
Standard Library only - Zero external dependencies.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json
import time

@dataclass
class TaskNode:
    id: str
    name: str
    stage: int
    seat: str
    action: str
    dependencies: List[str] = field(default_factory=list)
    status: str = "PENDING"
    output_files: List[str] = field(default_factory=list)
    duration_ms: float = 0.0

@dataclass
class SeatConfig:
    seat_id: str
    role_name: str
    mandate_file: str
    provider_binary: str
    is_active: bool = True

@dataclass
class FactoryState:
    factory_id: str
    project_name: str
    created_at: float = field(default_factory=time.time)
    seats: Dict[str, SeatConfig] = field(default_factory=dict)
    tasks: Dict[str, TaskNode] = field(default_factory=dict)
    active_wave: int = 1
    total_tokens_saved: float = 0.0
    status: str = "INITIALIZED"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
