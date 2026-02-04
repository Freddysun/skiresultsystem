# Pydantic 模式定义
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum

class GenderEnum(str, Enum):
    MALE = "男"
    FEMALE = "女"

class EventTypeEnum(str, Enum):
    DOWNHILL = "滑降"
    SLALOM = "回转"
    GIANT_SLALOM = "大回转"
    SUPER_G = "超级大回转"
    COMBINED = "全能"

class ResultStatusEnum(str, Enum):
    COMPLETED = "完成"
    DNF = "DNF"
    DSQ = "DSQ"

class QueryParams(BaseModel):
    athlete_name: Optional[str] = None
    event_type: Optional[str] = None
    category: Optional[str] = None
    organization: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    season: Optional[str] = None
    page: int = 1
    page_size: int = 20

class ResultResponse(BaseModel):
    id: str
    athlete_name: str
    organization_name: Optional[str]
    competition_name: str
    competition_date: date
    event_name: str
    category_name: str
    gender: str
    run1_time: Optional[str]
    run2_time: Optional[str]
    total_time: Optional[str]
    rank: Optional[int]
    time_behind_leader: Optional[str]
    status: str

    class Config:
        from_attributes = True

class QueryResponse(BaseModel):
    results: List[ResultResponse]
    total: int
    page: int
    page_size: int
    total_pages: int