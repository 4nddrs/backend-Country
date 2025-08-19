from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func
from app.supabase_client import Base


class EmployeePosition(Base):
    __tablename__ = "employee_position"

    idPositionEmployee = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    namePosition = Column(String, nullable=False)
