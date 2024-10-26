import random
import string
from typing import List

from fastapi import FastAPI, Query

app = FastAPI()


def generate_password(length: int, special: bool, uppercase: bool, digits: bool) -> str:
    characters: str = string.ascii_lowercase
    password: List[str] = []

    if uppercase:
        characters += string.ascii_uppercase
        password.append(random.choice(string.ascii_uppercase))
    if digits:
        characters += string.digits
        password.append(random.choice(string.digits))
    if special:
        characters += string.punctuation
        password.append(random.choice(string.punctuation))

    remaining_length = length - len(password)
    password.extend(random.choice(characters) for _ in range(remaining_length))
    random.shuffle(password)

    final_password = "".join(password)
    return final_password


@app.get("/generate_passwords/", response_model=List[str])  # type: ignore
def create_passwords(
    length: int = Query(default=12, ge=5, le=21),
    special: bool = Query(default=False),
    uppercase: bool = Query(default=False),
    digits: bool = Query(default=False),
    count: int = Query(default=10, le=100),
) -> List[str]:
    passwords: List[str] = [
        generate_password(length, special, uppercase, digits) for _ in range(count)
    ]
    return passwords
