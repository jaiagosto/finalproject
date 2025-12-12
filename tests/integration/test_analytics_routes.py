import pytest


class TestAnalyticsRoutes:
    """Integration tests for analytics routes"""
    
    def test_get_analytics_summary_empty(self, client, auth_headers):
        """Test getting analytics with no calculations"""
        response = client.get("/analytics/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_calculations"] == 0
        assert data["operations_breakdown"] == []
        assert data["most_used_operation"] is None
    
    def test_get_analytics_summary_with_data(self, client, auth_headers, test_calculations):
        """Test getting analytics with calculations"""
        response = client.get("/analytics/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_calculations"] == 3
        assert len(data["operations_breakdown"]) == 3
        assert data["most_used_operation"] is not None
        assert data["average_result"] is not None
    
    def test_get_calculation_history(self, client, auth_headers, test_calculations):
        """Test getting calculation history"""
        response = client.get("/analytics/history", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] == 3
        assert len(data["items"]) == 3
    
    def test_get_calculation_history_with_filter(self, client, auth_headers, test_calculations):
        """Test getting filtered calculation history"""
        response = client.get(
            "/analytics/history?operation=add",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["operation"] == "add"
    
    def test_get_calculation_history_pagination(self, client, auth_headers, test_calculations):
        """Test pagination in history"""
        response = client.get(
            "/analytics/history?limit=2&offset=0",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["limit"] == 2
        assert data["offset"] == 0
        assert data["has_more"] is True
    
    def test_clear_calculation_history(self, client, auth_headers, test_calculations):
        """Test clearing all calculation history"""
        response = client.delete("/analytics/history", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["deleted_count"] == 3
        
        # Verify history is empty
        response = client.get("/analytics/history", headers=auth_headers)
        data = response.json()
        assert data["total"] == 0