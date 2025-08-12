from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func
from app.database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    name = Column(String, nullable=False)
