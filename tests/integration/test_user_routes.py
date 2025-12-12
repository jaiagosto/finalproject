import pytest


class TestUserRoutes:
    """Integration tests for user profile routes"""
    
    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_get_profile(self, client, auth_headers, test_user):
        """Test getting user profile"""
        response = client.get("/users/profile", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email
    
    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_update_profile_username(self, client, auth_headers, test_user):
        """Test updating username"""
        response = client.put(
            "/users/profile",
            headers=auth_headers,
            json={"username": "updateduser"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "updateduser"
    
    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_update_profile_email(self, client, auth_headers, test_user):
        """Test updating email"""
        response = client.put(
            "/users/profile",
            headers=auth_headers,
            json={"email": "newemail@example.com"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newemail@example.com"
    
    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_change_password_success(self, client, auth_headers, test_user):
        """Test successful password change"""
        response = client.post(
            "/users/change-password",
            headers=auth_headers,
            json={
                "current_password": "testpass123",
                "new_password": "newpass456"
            }
        )
        
        assert response.status_code == 200
        assert "Password changed successfully" in response.json()["message"]
    
    @pytest.mark.skip(reason="Redis token validation issue in CI")
    def test_change_password_wrong_current(self, client, auth_headers, test_user):
        """Test password change with wrong current password"""
        response = client.post(
            "/users/change-password",
            headers=auth_headers,
            json={
                "current_password": "wrongpassword",
                "new_password": "newpass456"
            }
        )
        
        assert response.status_code == 400
        assert "Current password is incorrect" in response.json()["detail"]