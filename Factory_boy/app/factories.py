import factory
from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from .database import SessionLocal
from .models import Company, JTagCompany, Prefecture, Tag


class BaseFactory(SQLAlchemyModelFactory):
    """他のFactoryが継承するベースクラス。"""

    class Meta:
        abstract = True
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = "commit"


class PrefectureFactory(BaseFactory):
    class Meta:
        model = Prefecture

    name = Faker("city")


class CompanyFactory(BaseFactory):
    class Meta:
        model = Company

    name = Faker("company")
    sales = Faker("random_int", min=100, max=10000)
    prefecture = factory.SubFactory(PrefectureFactory)


class TagFactory(BaseFactory):
    class Meta:
        model = Tag

    name = Faker("word")


class JTagCompanyFactory(BaseFactory):
    class Meta:
        model = JTagCompany

    company = factory.SubFactory(CompanyFactory)
    tag = factory.SubFactory(TagFactory)
