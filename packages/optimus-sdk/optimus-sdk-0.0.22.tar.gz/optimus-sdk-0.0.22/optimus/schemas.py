import enum
import re

from pydantic import BaseModel, constr, validator
from typing import List, Any


class TrialStatus(enum.Enum):
    """Status of trials"""

    STARTED = "Started"
    PENDING = "Pending"
    SUCCEED = "Succeed"
    TERMINATED = "Terminated"
    FAILED = "Failed"


class ExperimentStatus(enum.Enum):
    INITIAL = "Initial"
    RUNNING = "Running"
    PAUSED = "Paused"
    SUCCEED = "Succeed"
    FAILED = "Failed"
    ARCHIVED = "Archived"


class Evaluation(BaseModel):
    name: str
    value: float


class Assignment(BaseModel):
    name: str
    value: Any


class TrialFailed(BaseModel):
    reason: str
    detail: constr(max_length=256) = None


class RespMetric(BaseModel):
    name: str
    value: float
    objective: str


class Trial(BaseModel):
    id: str
    sequence: int
    experimentId: str
    status: TrialStatus
    createdAt: str = None
    updatedAt: str = None
    StartedAt: str = None
    source: str = None
    evaluations: List[Evaluation] = None
    assignments: List[Assignment] = None
    failedDetail: TrialFailed = None
    metrics: List[RespMetric] = None

    @staticmethod
    def _is_number(num):
        try:
            num = float(num) if "." in num else int(num)
            return num
        except ValueError:
            return False

    @property
    def assignment(self):
        tmp = {}
        if not self.assignments:
            return None
        for assignment in self.assignments:
            if isinstance(assignment.value, str):
                num = self._is_number(assignment.value)
                value = num if num else assignment.value
            else:
                value = assignment.value
            tmp.update({assignment.name: value})
        return tmp


class Trials(BaseModel):
    trials: List[Trial]


class ObjectId(BaseModel):
    obj: str

    @validator("obj")
    def is_object_id(cls, obj):
        if len(obj) != 24:
            raise ValueError("is not a objectID")
        if re.match("^(?:(?=.*[a-f])(?=.*[0-9])).*$", obj) is None:
            raise ValueError("is not a objectID")
        return obj


class Metric(BaseModel):
    name: str
    objective: str
    strategy: str
    target: float
    range: List[float] = None


class Parameter(BaseModel):
    name: str
    type: str = "r"
    range: Any
    scale: str = ""
    precision: int = 0
    step: int = 0


class FocusedParameter(BaseModel):
    name: str
    value: Any


class Constraint(BaseModel):
    expr: str
    operator: str
    value: float


class BaseInfo(BaseModel):
    name: str
    description: str = None
    parallelCount: int = 3


class Experiment(BaseModel):
    id: str
    name: str
    description: str = None
    parallelCount: int = None
    status: ExperimentStatus = ExperimentStatus.INITIAL
    createdAt: str = None
    updatedAt: str = None
    completed: bool = False
    completedAt: str = None
    initialized: bool = False
    metrics: List[Metric] = None
    parameters: List[Parameter] = None
    focusedParameters: List[FocusedParameter] = None
    constraints: List[Constraint] = None


class Experiments(BaseModel):
    experiments: List[Experiment]