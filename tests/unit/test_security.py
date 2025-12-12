import pytest
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    blacklist_token,
    is_token_blacklisted
)
from jose import jwt
from app.core.config import settings
from datetime import timedelta


class TestSecurity:
    """Unit tests for security functions"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        plain_password = "testpassword123"
        hashed = get_password_hash(plain_password)
        
        assert hashed != plain_password
        assert verify_password(plain_password, hashed)
        assert not verify_password("wrongpassword", hashed)
    
    def test_create_access_token(self):
        """Test JWT token creation"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        
        # Decode and verify
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert payload["sub"] == "testuser"
        assert "exp" in payload
    
    def test_create_access_token_with_expiry(self):
        """Test token creation with custom expiry"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=5)
        token = create_access_token(data, expires_delta)
        
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert "exp" in payload
    
    def test_token_blacklisting(self):
        """Test token blacklisting"""
        token = "test_token_123"
        
        # Token should not be blacklisted initially
        assert not is_token_blacklisted(token)
        
        # Blacklist the token
        blacklist_token(token, expires_in=60)
        
        # Token should now be blacklisted
        assert is_token_blacklisted(token)