from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal


class CalculationBase(BaseModel):
    """Base calculation schema"""
    operation: Literal["add", "subtract", "multiply", "divide", "power", "modulus"]
    operand1: float = Field(..., description="First operand")
    operand2: float = Field(..., description="Second operand")
    
    @field_validator("operand2")
    @classmethod
    def validate_division(cls, v, info):
        """Validate division by zero"""
        if info.data.get("operation") == "divide" and v == 0:
            raise ValueError("Cannot divide by zero")
        if info.data.get("operation") == "modulus" and v == 0:
            raise ValueError("Cannot calculate modulus with zero divisor")
        return v


class CalculationCreate(CalculationBase):
    """Schema for creating a calculation"""
    pass


class CalculationUpdate(BaseModel):
    """Schema for updating a calculation"""
    operation: Literal["add", "subtract", "multiply", "divide", "power", "modulus"] = None
    operand1: float = None
    operand2: float = None


class CalculationResponse(CalculationBase):
    """Schema for calculation response"""
    id: int
    user_id: int
    result: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class CalculationResult(BaseModel):
    """Schema for calculation result"""
    operation: str
    operand1: float
    operand2: float
    result: float
    message: str = "Calculation completed successfully"