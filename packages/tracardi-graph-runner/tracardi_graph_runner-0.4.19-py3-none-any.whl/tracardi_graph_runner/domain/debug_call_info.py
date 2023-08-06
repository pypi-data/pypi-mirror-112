from typing import List, Optional

from pydantic import BaseModel

from tracardi_graph_runner.domain.entity import Entity
from tracardi_graph_runner.domain.input_params import InputParams
from tracardi_graph_runner.domain.action_result import ActionResult


class DebugInput(BaseModel):
    edge: Optional[Entity] = None
    params: Optional[InputParams] = None


class DebugOutput(BaseModel):
    edge: Optional[Entity] = None
    results: Optional[List[ActionResult]] = None


class Profiler(BaseModel):
    startTime: float
    runTime: float
    endTime: float


class DebugCallInfo(BaseModel):
    node: Entity
    number: int
    profiler: Profiler
    input: DebugInput
    output: DebugOutput
    # input_edge: Optional[Entity] = None
    # output_edge: Optional[Entity] = None
    init: Optional[dict] = None
    # input: Optional[InputParams] = None
    # output: Optional[List[ActionResult]] = None
    profile: Optional[dict] = {}
    event: Optional[dict] = {}
    session: Optional[dict] = {}
    error: Optional[str] = None
