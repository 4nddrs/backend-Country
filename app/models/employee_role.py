from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func
from app.supabase_client import Base


class EmployeeRole(Base):
    __tablename__ = "employee_role"

    idRoleEmployee = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    nameRole = Column(String, nullable=False)
