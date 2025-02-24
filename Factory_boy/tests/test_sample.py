from app.factories import CompanyFactory, JTagCompanyFactory


def test_create_company():
    company = CompanyFactory()
    assert company.id is not None
    assert company.prefecture is not None


def test_create_jtag_company():
    j_tag_company = JTagCompanyFactory()
    assert j_tag_company.company is not None
    assert j_tag_company.tag is not None
