from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime


class OperationStats(BaseModel):
    """Statistics for a specific operation"""
    operation: str
    count: int
    percentage: float


class AnalyticsSummary(BaseModel):
    """Summary analytics for calculations"""
    total_calculations: int
    total_users: int = 1
    operations_breakdown: List[OperationStats]
    most_used_operation: Optional[str] = None
    average_result: Optional[float] = None
    latest_calculation: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class HistoryFilter(BaseModel):
    """Filters for calculation history"""
    operation: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 10
    offset: int = 0