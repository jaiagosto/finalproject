import pytest


class TestCalculationRoutes:
    """Integration tests for calculation routes"""

    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_create_calculation_add(self, client, auth_headers, test_user):
        """Test creating addition calculation"""
        response = client.post(
            "/calculations/",
            headers=auth_headers,
            json={
                "operation": "add",
                "operand1": 10,
                "operand2": 5
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 15
        assert data["operation"] == "add"
    
    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_create_calculation_divide(self, client, auth_headers, test_user):
        """Test creating division calculation"""
        response = client.post(
            "/calculations/",
            headers=auth_headers,
            json={
                "operation": "divide",
                "operand1": 20,
                "operand2": 4
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 5
    
    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_create_calculation_divide_by_zero(self, client, auth_headers):
        """Test division by zero validation"""
        response = client.post(
            "/calculations/",
            headers=auth_headers,
            json={
                "operation": "divide",
                "operand1": 10,
                "operand2": 0
            }
        )
        
        assert response.status_code == 422
    
    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_create_calculation_power(self, client, auth_headers):
        """Test power operation"""
        response = client.post(
            "/calculations/",
            headers=auth_headers,
            json={
                "operation": "power",
                "operand1": 2,
                "operand2": 3
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 8
    
    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_create_calculation_modulus(self, client, auth_headers):
        """Test modulus operation"""
        response = client.post(
            "/calculations/",
            headers=auth_headers,
            json={
                "operation": "modulus",
                "operand1": 10,
                "operand2": 3
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 1
    
    def test_create_calculation_unauthorized(self, client):
        """Test creating calculation without auth"""
        response = client.post(
            "/calculations/",
            json={
                "operation": "add",
                "operand1": 10,
                "operand2": 5
            }
        )
        
        assert response.status_code == 401
    
    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_get_all_calculations(self, client, auth_headers, test_calculations):
        """Test getting all calculations"""
        response = client.get("/calculations/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_get_calculation_by_id(self, client, auth_headers, test_calculations, test_user):
        """Test getting specific calculation"""
        calc_id = test_calculations[0].id
        response = client.get(f"/calculations/{calc_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == calc_id
        assert data["operation"] == "add"
    
    def test_get_calculation_not_found(self, client, auth_headers):
        """Test getting nonexistent calculation"""
        response = client.get("/calculations/99999", headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_update_calculation(self, client, auth_headers, test_calculations):
        """Test updating calculation"""
        calc_id = test_calculations[0].id
        response = client.put(
            f"/calculations/{calc_id}",
            headers=auth_headers,
            json={
                "operation": "multiply",
                "operand1": 5,
                "operand2": 6
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 30
        assert data["operation"] == "multiply"
    
    def test_delete_calculation(self, client, auth_headers, test_calculations):
        """Test deleting calculation"""
        calc_id = test_calculations[0].id
        response = client.delete(f"/calculations/{calc_id}", headers=auth_headers)
        
        assert response.status_code == 204
        
        # Verify deletion
        response = client.get(f"/calculations/{calc_id}", headers=auth_headers)
        assert response.status_code == 404