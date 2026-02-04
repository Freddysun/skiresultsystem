# 查询服务
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models import Result, Athlete, Competition, Event, Category, Organization
from schemas import QueryParams, ResultResponse
from typing import List, Tuple

class QueryService:
    def __init__(self, db: Session):
        self.db = db
    
    def search_results(self, params: QueryParams) -> Tuple[List[ResultResponse], int]:
        """根据查询参数搜索成绩"""
        query = self.db.query(Result).join(Athlete).join(Competition).join(Event).join(Category)
        
        filters = []
        
        if params.athlete_name:
            filters.append(Athlete.name.like(f"%{params.athlete_name}%"))
        
        if params.event_type:
            filters.append(Event.name == params.event_type)
        
        if params.category:
            filters.append(Category.name == params.category)
        
        if params.organization:
            query = query.join(Organization, Athlete.organization_id == Organization.id, isouter=True)
            filters.append(Organization.name.like(f"%{params.organization}%"))
        
        if params.date_from:
            filters.append(Competition.date >= params.date_from)
        
        if params.date_to:
            filters.append(Competition.date <= params.date_to)
        
        if params.season:
            filters.append(Competition.season == params.season)
        
        if filters:
            query = query.filter(and_(*filters))
        
        query = query.order_by(Competition.date.desc())
        total = query.count()
        
        offset = (params.page - 1) * params.page_size
        results = query.offset(offset).limit(params.page_size).all()
        
        result_responses = []
        for result in results:
            result_responses.append(ResultResponse(
                id=result.id,
                athlete_name=result.athlete.name,
                organization_name=result.athlete.organization.name if result.athlete.organization else None,
                competition_name=result.competition.name,
                competition_date=result.competition.date,
                event_name=result.event.name.value,
                category_name=result.category.name.value,
                gender=result.category.gender.value,
                run1_time=result.run1_time,
                run2_time=result.run2_time,
                total_time=result.total_time,
                rank=result.rank,
                time_behind_leader=result.time_behind_leader,
                status=result.status.value
            ))
        
        return result_responses, total
