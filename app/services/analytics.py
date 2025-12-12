from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.calculation import Calculation
from app.schemas.analytics import AnalyticsSummary, OperationStats
from typing import List, Optional
from datetime import datetime


class AnalyticsService:
    """Service class for analytics and history operations"""
    
    @staticmethod
    def get_user_statistics(db: Session, user_id: int) -> AnalyticsSummary:
        """Get analytics summary for a user"""
        
        # Get total calculations
        total_calculations = db.query(Calculation).filter(
            Calculation.user_id == user_id
        ).count()
        
        if total_calculations == 0:
            return AnalyticsSummary(
                total_calculations=0,
                operations_breakdown=[],
                most_used_operation=None,
                average_result=None,
                latest_calculation=None
            )
        
        # Get operations breakdown
        operations_data = db.query(
            Calculation.operation,
            func.count(Calculation.id).label("count")
        ).filter(
            Calculation.user_id == user_id
        ).group_by(
            Calculation.operation
        ).all()
        
        operations_breakdown = [
            OperationStats(
                operation=op,
                count=count,
                percentage=round((count / total_calculations) * 100, 2)
            )
            for op, count in operations_data
        ]
        
        # Sort by count descending
        operations_breakdown.sort(key=lambda x: x.count, reverse=True)
        
        # Get most used operation
        most_used_operation = operations_breakdown[0].operation if operations_breakdown else None
        
        # Get average result
        avg_result = db.query(
            func.avg(Calculation.result)
        ).filter(
            Calculation.user_id == user_id
        ).scalar()
        
        # Get latest calculation timestamp
        latest_calc = db.query(Calculation).filter(
            Calculation.user_id == user_id
        ).order_by(desc(Calculation.created_at)).first()
        
        latest_calculation = latest_calc.created_at if latest_calc else None
        
        return AnalyticsSummary(
            total_calculations=total_calculations,
            operations_breakdown=operations_breakdown,
            most_used_operation=most_used_operation,
            average_result=round(avg_result, 4) if avg_result is not None else None,
            latest_calculation=latest_calculation
        )
    
    @staticmethod
    def get_calculation_history(
        db: Session,
        user_id: int,
        operation: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[List[Calculation], int]:
        """Get filtered calculation history for a user"""
        
        query = db.query(Calculation).filter(Calculation.user_id == user_id)
        
        # Apply filters
        if operation:
            query = query.filter(Calculation.operation == operation)
        
        if start_date:
            query = query.filter(Calculation.created_at >= start_date)
        
        if end_date:
            query = query.filter(Calculation.created_at <= end_date)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination and ordering
        calculations = query.order_by(
            desc(Calculation.created_at)
        ).limit(limit).offset(offset).all()
        
        return calculations, total
    
    @staticmethod
    def delete_calculation_history(db: Session, user_id: int) -> int:
        """Delete all calculation history for a user"""
        deleted_count = db.query(Calculation).filter(
            Calculation.user_id == user_id
        ).delete()
        db.commit()
        return deleted_count