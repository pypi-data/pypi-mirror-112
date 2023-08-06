from typing import List, Dict
from pydantic import BaseModel
from tracardi_graph_runner.domain.debug_call_info import DebugCallInfo, Profiler
from tracardi_graph_runner.domain.entity import Entity
from tracardi_graph_runner.domain.flow_debug_info import FlowDebugInfo


class DebugNodeInfo(BaseModel):
    id: str
    sequenceNumber: int = 0
    calls: List[DebugCallInfo] = []
    profiler: Profiler


class DebugInfo(BaseModel):
    timestamp: float
    event: Entity
    flow: FlowDebugInfo
    nodes: Dict[str, DebugNodeInfo] = {}
