import pytest
from app.services.calculator import CalculatorService


class TestCalculatorService:
    """Unit tests for CalculatorService"""
    
    def test_add(self):
        """Test addition operation"""
        assert CalculatorService.add(5, 3) == 8
        assert CalculatorService.add(-5, 3) == -2
        assert CalculatorService.add(0, 0) == 0
        assert CalculatorService.add(1.5, 2.5) == 4.0
    
    def test_subtract(self):
        """Test subtraction operation"""
        assert CalculatorService.subtract(10, 3) == 7
        assert CalculatorService.subtract(5, 10) == -5
        assert CalculatorService.subtract(0, 0) == 0
        assert CalculatorService.subtract(5.5, 2.5) == 3.0
    
    def test_multiply(self):
        """Test multiplication operation"""
        assert CalculatorService.multiply(5, 3) == 15
        assert CalculatorService.multiply(-5, 3) == -15
        assert CalculatorService.multiply(0, 10) == 0
        assert CalculatorService.multiply(2.5, 4) == 10.0
    
    def test_divide(self):
        """Test division operation"""
        assert CalculatorService.divide(10, 2) == 5
        assert CalculatorService.divide(9, 3) == 3
        assert CalculatorService.divide(7, 2) == 3.5
        assert CalculatorService.divide(-10, 2) == -5
    
    def test_divide_by_zero(self):
        """Test division by zero raises error"""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            CalculatorService.divide(10, 0)
    
    def test_power(self):
        """Test power operation"""
        assert CalculatorService.power(2, 3) == 8
        assert CalculatorService.power(5, 2) == 25
        assert CalculatorService.power(10, 0) == 1
        assert CalculatorService.power(4, 0.5) == 2.0
    
    def test_modulus(self):
        """Test modulus operation"""
        assert CalculatorService.modulus(10, 3) == 1
        assert CalculatorService.modulus(15, 4) == 3
        assert CalculatorService.modulus(20, 5) == 0
    
    def test_modulus_by_zero(self):
        """Test modulus by zero raises error"""
        with pytest.raises(ValueError, match="Cannot calculate modulus with zero divisor"):
            CalculatorService.modulus(10, 0)
    
    def test_calculate_all_operations(self):
        """Test calculate method with all operations"""
        assert CalculatorService.calculate("add", 10, 5) == 15
        assert CalculatorService.calculate("subtract", 10, 5) == 5
        assert CalculatorService.calculate("multiply", 10, 5) == 50
        assert CalculatorService.calculate("divide", 10, 5) == 2
        assert CalculatorService.calculate("power", 2, 3) == 8
        assert CalculatorService.calculate("modulus", 10, 3) == 1
    
    def test_calculate_invalid_operation(self):
        """Test calculate with invalid operation"""
        with pytest.raises(ValueError, match="Invalid operation"):
            CalculatorService.calculate("invalid", 10, 5)