from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.analytics import AnalyticsSummary
from app.schemas.calculation import CalculationResponse
from app.services.analytics import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics & History"])


@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analytics summary for current user"""
    
    return AnalyticsService.get_user_statistics(db, current_user.id)


@router.get("/history", response_model=dict)
def get_calculation_history(
    operation: Optional[str] = Query(None, description="Filter by operation type"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get filtered calculation history with pagination"""
    
    calculations, total = AnalyticsService.get_calculation_history(
        db=db,
        user_id=current_user.id,
        operation=operation,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset
    )
    
    # Convert to response format
    calc_responses = [
        CalculationResponse(
            id=calc.id,
            user_id=calc.user_id,
            operation=calc.operation,
            operand1=calc.operand1,
            operand2=calc.operand2,
            result=calc.result,
            created_at=calc.created_at
        )
        for calc in calculations
    ]
    
    return {
        "items": calc_responses,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": (offset + limit) < total
    }


@router.delete("/history", status_code=200)
def clear_calculation_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear all calculation history for current user"""
    
    deleted_count = AnalyticsService.delete_calculation_history(db, current_user.id)
    
    return {
        "message": "Calculation history cleared successfully",
        "deleted_count": deleted_count
    }