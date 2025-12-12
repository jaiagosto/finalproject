class CalculatorService:
    """Service class for calculator operations"""
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Add two numbers"""
        return a + b
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtract b from a"""
        return a - b
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers"""
        return a * b
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        """Divide a by b"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    @staticmethod
    def power(a: float, b: float) -> float:
        """Raise a to the power of b"""
        return a ** b
    
    @staticmethod
    def modulus(a: float, b: float) -> float:
        """Calculate a modulo b"""
        if b == 0:
            raise ValueError("Cannot calculate modulus with zero divisor")
        return a % b
    
    @classmethod
    def calculate(cls, operation: str, operand1: float, operand2: float) -> float:
        """Perform calculation based on operation type"""
        operations = {
            "add": cls.add,
            "subtract": cls.subtract,
            "multiply": cls.multiply,
            "divide": cls.divide,
            "power": cls.power,
            "modulus": cls.modulus
        }
        
        if operation not in operations:
            raise ValueError(f"Invalid operation: {operation}")
        
        return operations[operation](operand1, operand2)