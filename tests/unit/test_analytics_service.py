import pytest
from app.services.analytics import AnalyticsService
from app.models.calculation import Calculation


class TestAnalyticsService:
    """Unit tests for AnalyticsService"""
    
    def test_get_user_statistics_empty(self, db_session, test_user):
        """Test getting statistics with no calculations"""
        stats = AnalyticsService.get_user_statistics(db_session, test_user.id)
        
        assert stats.total_calculations == 0
        assert stats.operations_breakdown == []
        assert stats.most_used_operation is None
        assert stats.average_result is None
        assert stats.latest_calculation is None
    
    def test_get_user_statistics_with_data(self, db_session, test_user, test_calculations):
        """Test getting statistics with calculations"""
        stats = AnalyticsService.get_user_statistics(db_session, test_user.id)
        
        assert stats.total_calculations == 3
        assert len(stats.operations_breakdown) == 3
        assert stats.most_used_operation in ["add", "subtract", "multiply"]
        assert stats.average_result is not None
        assert stats.latest_calculation is not None
    
    def test_get_calculation_history(self, db_session, test_user, test_calculations):
        """Test getting calculation history"""
        calculations, total = AnalyticsService.get_calculation_history(
            db_session, test_user.id, limit=10, offset=0
        )
        
        assert total == 3
        assert len(calculations) == 3
        # Should be ordered by created_at descending
        assert calculations[0].created_at >= calculations[-1].created_at
    
    def test_get_calculation_history_with_filter(self, db_session, test_user, test_calculations):
        """Test getting filtered calculation history"""
        calculations, total = AnalyticsService.get_calculation_history(
            db_session, test_user.id, operation="add", limit=10, offset=0
        )
        
        assert total == 1
        assert len(calculations) == 1
        assert calculations[0].operation == "add"
    
    def test_get_calculation_history_pagination(self, db_session, test_user, test_calculations):
        """Test pagination in calculation history"""
        # Get first page
        calculations_page1, total = AnalyticsService.get_calculation_history(
            db_session, test_user.id, limit=2, offset=0
        )
        
        assert total == 3
        assert len(calculations_page1) == 2
        
        # Get second page
        calculations_page2, _ = AnalyticsService.get_calculation_history(
            db_session, test_user.id, limit=2, offset=2
        )
        
        assert len(calculations_page2) == 1
    
    def test_delete_calculation_history(self, db_session, test_user, test_calculations):
        """Test deleting all calculation history"""
        deleted_count = AnalyticsService.delete_calculation_history(db_session, test_user.id)
        
        assert deleted_count == 3
        
        # Verify all calculations are deleted
        remaining = db_session.query(Calculation).filter(
            Calculation.user_id == test_user.id
        ).count()
        assert remaining == 0