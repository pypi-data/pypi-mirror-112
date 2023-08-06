from typing import List, Dict, Optional
from pydantic import BaseModel
from tracardi_graph_runner.domain.debug_call_info import DebugCallInfo, Profiler
from tracardi_graph_runner.domain.entity import Entity
from tracardi_graph_runner.domain.error_debug_info import ErrorDebugInfo


class FlowDebugInfo(Entity):
    error: List[ErrorDebugInfo] = []


class DebugNodeInfo(BaseModel):
    id: str
    sequenceNumber: int = 0
    calls: List[DebugCallInfo] = []
    profiler: Profiler


class DebugInfo(BaseModel):
    timestamp: float
    flow: FlowDebugInfo
    event: Optional[dict] = {}
    session: Optional[dict] = {}
    nodes: Dict[str, DebugNodeInfo] = {}
