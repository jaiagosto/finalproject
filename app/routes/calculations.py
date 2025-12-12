from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.calculation import Calculation
from app.schemas.calculation import (
    CalculationCreate,
    CalculationResponse,
    CalculationResult,
    CalculationUpdate
)
from app.services.calculator import CalculatorService

router = APIRouter(prefix="/calculations", tags=["Calculations"])


@router.post("/", response_model=CalculationResult, status_code=status.HTTP_201_CREATED)
def create_calculation(
    calc_data: CalculationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create and perform a new calculation (Browse + Add)"""
    
    try:
        # Perform calculation
        result = CalculatorService.calculate(
            calc_data.operation,
            calc_data.operand1,
            calc_data.operand2
        )
        
        # Save to database
        calculation = Calculation(
            user_id=current_user.id,
            operation=calc_data.operation,
            operand1=calc_data.operand1,
            operand2=calc_data.operand2,
            result=result
        )
        
        db.add(calculation)
        db.commit()
        db.refresh(calculation)
        
        return CalculationResult(
            operation=calc_data.operation,
            operand1=calc_data.operand1,
            operand2=calc_data.operand2,
            result=result,
            message="Calculation completed and saved successfully"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[CalculationResponse])
def get_all_calculations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all calculations for current user (Browse)"""
    
    calculations = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).order_by(
        Calculation.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return calculations


@router.get("/{calculation_id}", response_model=CalculationResponse)
def get_calculation(
    calculation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific calculation by ID (Read)"""
    
    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    return calculation


@router.put("/{calculation_id}", response_model=CalculationResponse)
def update_calculation(
    calculation_id: int,
    calc_data: CalculationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a calculation (Edit)"""
    
    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    # Update fields if provided
    if calc_data.operation:
        calculation.operation = calc_data.operation
    if calc_data.operand1 is not None:
        calculation.operand1 = calc_data.operand1
    if calc_data.operand2 is not None:
        calculation.operand2 = calc_data.operand2
    
    # Recalculate result
    try:
        calculation.result = CalculatorService.calculate(
            calculation.operation,
            calculation.operand1,
            calculation.operand2
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    db.commit()
    db.refresh(calculation)
    
    return calculation


@router.delete("/{calculation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(
    calculation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a calculation (Delete)"""
    
    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    db.delete(calculation)
    db.commit()
    
    return None