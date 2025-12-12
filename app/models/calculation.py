from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Calculation(Base):
    """Calculation model for storing calculation history"""
    
    __tablename__ = "calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    operation = Column(String, nullable=False, index=True)
    operand1 = Column(Float, nullable=False)
    operand2 = Column(Float, nullable=False)
    result = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship to user
    user = relationship("User", back_populates="calculations")
    
    def __repr__(self):
        return f"<Calculation(id={self.id}, operation='{self.operation}', result={self.result})>"
    
    def to_dict(self):
        """Convert calculation to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "operation": self.operation,
            "operand1": self.operand1,
            "operand2": self.operand2,
            "result": self.result,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }