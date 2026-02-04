# 成绩查询路由
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.query_service import QueryService
from schemas import QueryParams, QueryResponse
from typing import Optional
from datetime import date
import math

router = APIRouter()

@router.get("/search", response_model=QueryResponse)
async def search_results(
    athlete_name: Optional[str] = Query(None, description="运动员姓名"),
    event_type: Optional[str] = Query(None, description="项目类型"),
    category: Optional[str] = Query(None, description="组别"),
    organization: Optional[str] = Query(None, description="所属组织"),
    date_from: Optional[date] = Query(None, description="开始日期"),
    date_to: Optional[date] = Query(None, description="结束日期"),
    season: Optional[str] = Query(None, description="赛季"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """查询成绩"""
    params = QueryParams(
        athlete_name=athlete_name,
        event_type=event_type,
        category=category,
        organization=organization,
        date_from=date_from,
        date_to=date_to,
        season=season,
        page=page,
        page_size=page_size
    )
    
    query_service = QueryService(db)
    results, total = query_service.search_results(params)
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return QueryResponse(
        results=results,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )
