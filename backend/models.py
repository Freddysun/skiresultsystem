# 数据库模型定义
from sqlalchemy import Column, String, Float, Integer, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class GenderEnum(str, enum.Enum):
    """性别枚举"""
    MALE = "男"
    FEMALE = "女"

class EventTypeEnum(str, enum.Enum):
    """项目类型枚举"""
    DOWNHILL = "滑降"
    SLALOM = "回转"
    GIANT_SLALOM = "大回转"
    SUPER_G = "超级大回转"
    COMBINED = "全能"

class CategoryNameEnum(str, enum.Enum):
    """组别名称枚举"""
    U8 = "U8"
    U10 = "U10"
    U11 = "U11"
    U12 = "U12"
    U13 = "U13"
    U14 = "U14"
    U15 = "U15"
    U16 = "U16"
    U18 = "U18"
    GROUP_A = "甲组"
    GROUP_B = "乙组"
    GROUP_C = "丙组"
    GROUP_D = "丁组"
    YOUTH = "青年组"
    ADULT = "成年组"

class ResultStatusEnum(str, enum.Enum):
    """成绩状态枚举"""
    COMPLETED = "完成"
    DNF = "DNF"
    DSQ = "DSQ"

class Organization(Base):
    """组织/俱乐部"""
    __tablename__ = "organizations"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    athletes = relationship("Athlete", back_populates="organization")

class Athlete(Base):
    """运动员"""
    __tablename__ = "athletes"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    gender = Column(SQLEnum(GenderEnum), nullable=False)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    organization = relationship("Organization", back_populates="athletes")
    results = relationship("Result", back_populates="athlete")

class Competition(Base):
    """比赛"""
    __tablename__ = "competitions"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String, nullable=True)
    season = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    events = relationship("Event", back_populates="competition")
    results = relationship("Result", back_populates="competition")

class Event(Base):
    """项目"""
    __tablename__ = "events"
    
    id = Column(String, primary_key=True)
    competition_id = Column(String, ForeignKey("competitions.id"), nullable=False)
    name = Column(SQLEnum(EventTypeEnum), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    competition = relationship("Competition", back_populates="events")
    categories = relationship("Category", back_populates="event")
    results = relationship("Result", back_populates="event")

class Category(Base):
    """组别"""
    __tablename__ = "categories"
    
    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    name = Column(SQLEnum(CategoryNameEnum), nullable=False)
    gender = Column(SQLEnum(GenderEnum), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    event = relationship("Event", back_populates="categories")
    results = relationship("Result", back_populates="category")

class Result(Base):
    """成绩"""
    __tablename__ = "results"
    
    id = Column(String, primary_key=True)
    athlete_id = Column(String, ForeignKey("athletes.id"), nullable=False)
    competition_id = Column(String, ForeignKey("competitions.id"), nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    run1_time = Column(String, nullable=True)
    run2_time = Column(String, nullable=True)
    total_time = Column(String, nullable=True)
    rank = Column(Integer, nullable=True)
    time_behind_leader = Column(String, nullable=True)
    status = Column(SQLEnum(ResultStatusEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    athlete = relationship("Athlete", back_populates="results")
    competition = relationship("Competition", back_populates="results")
    event = relationship("Event", back_populates="results")
    category = relationship("Category", back_populates="results")