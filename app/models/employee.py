from sqlalchemy import (
    Column,
    BigInteger,
    String,
    TIMESTAMP,
    func,
    Boolean,
    Date,
    SmallInteger,
    ForeignKey,
    LargeBinary,
)
from app.supabase_client import Base


class Employee(Base):
    __tablename__ = "employee"

    idEmployee = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    fullName = Column(String, nullable=False)
    ci = Column(String, nullable=False)
    phoneNumber = Column(SmallInteger, nullable=False)
    employeePhoto = Column(LargeBinary)
    startContractDate = Column(Date, nullable=False)
    endContractDate = Column(Date, nullable=False)
    startTime = Column(TIMESTAMP, nullable=False)
    exitTime = Column(TIMESTAMP, nullable=False)
    salary = Column(SmallInteger, nullable=False)
    status = Column(Boolean, default=False)
    fk_idRoleEmployee = Column(
        BigInteger, ForeignKey("employee_role.idRoleEmployee"), nullable=False
    )
    fk_idPositionEmployee = Column(
        BigInteger, ForeignKey("employee_position.idPositionEmployee"), nullable=False
    )
