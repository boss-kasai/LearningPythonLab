from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Prefecture(Base):
    __tablename__ = "prefecture"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    sales = Column(Integer, nullable=False)
    prefecture_id = Column(Integer, ForeignKey("prefecture.id"))

    prefecture = relationship("Prefecture", backref="companies")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)


class JTagCompany(Base):
    __tablename__ = "j_tag_company"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))

    company = relationship("Company")
    tag = relationship("Tag")
