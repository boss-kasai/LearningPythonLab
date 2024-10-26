import string

from fastapi.testclient import TestClient
from logApp1.log_1_app import app

client = TestClient(app)


def test_generate_passwords_default() -> None:
    response = client.get("/generate_passwords/")
    assert response.status_code == 200
    passwords = response.json()
    assert isinstance(passwords, list)
    assert len(passwords) == 10  # デフォルトで10個のパスワード
    assert all(len(p) == 12 for p in passwords)  # デフォルトで12文字


def test_generate_passwords_with_options() -> None:
    response = client.get(
        "/generate_passwords/",
        params={
            "length": 16,
            "special": True,
            "uppercase": True,
            "digits": True,
            "count": 5,
        },
    )
    assert response.status_code == 200
    passwords = response.json()
    assert isinstance(passwords, list)
    assert len(passwords) == 5  # 指定した5個のパスワード
    assert all(len(p) == 16 for p in passwords)  # 指定した16文字
    # 特殊文字、大文字、数字が含まれているかのチェック
    for password in passwords:
        assert any(c.isupper() for c in password)
        assert any(c.isdigit() for c in password)
        assert any(c in string.punctuation for c in password)


def test_generate_passwords_length_limits() -> None:
    # 最小値（5文字）のチェック
    response = client.get("/generate_passwords/", params={"length": 5})
    assert response.status_code == 200
    passwords = response.json()
    assert all(len(p) == 5 for p in passwords)

    # 最大値（21文字）のチェック
    response = client.get("/generate_passwords/", params={"length": 21})
    assert response.status_code == 200
    passwords = response.json()
    assert all(len(p) == 21 for p in passwords)


def test_generate_passwords_count_limit() -> None:
    # 最大個数（100個）のチェック
    response = client.get("/generate_passwords/", params={"count": 100})
    assert response.status_code == 200
    passwords = response.json()
    assert len(passwords) == 100
