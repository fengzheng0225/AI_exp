from typing import List, Dict, Optional, Union
from pydantic import BaseModel

class TimeRange(BaseModel):
    type: str  # relative/absolute
    value: str

class StructuredRequirement(BaseModel):
    metrics: List[str]
    dimensions: List[str]
    time_range: TimeRange
    filters: List[str] = []

class TextToSQLRequest(BaseModel):
    text: str
    context: Optional[Dict] = None

class ClarificationQuestion(BaseModel):
    field: str
    message: str

class SQLResponse(BaseModel):
    sql: str
    explanation: str
    performance_hints: List[str]

class TextToSQLResponse(BaseModel):
    status: str  # success/clarify/error
    data: Union[SQLResponse, List[ClarificationQuestion], str]

class MetricDefinition(BaseModel):
    formula: str
    dependencies: List[str]
    type: str
    description: str = ""

class DimensionDefinition(BaseModel):
    table: str
    type: str
    joins: List[Dict]
    description: str = ""
