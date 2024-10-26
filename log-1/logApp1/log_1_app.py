import logging
import random
import string
from typing import List

from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

# ロガーの設定
logging.basicConfig(
    filename="log-1/logApp1/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode="a",
)
logger = logging.getLogger(__name__)


def generate_password(length: int, special: bool, uppercase: bool, digits: bool) -> str:
    characters: str = string.ascii_lowercase
    password: List[str] = []

    logger.info(
        f"Generating password with length={length}, special={special}, uppercase={uppercase}, digits={digits}"
    )

    if uppercase:
        characters += string.ascii_uppercase
        password.append(random.choice(string.ascii_uppercase))
        logger.debug("Added uppercase character")
    if digits:
        characters += string.digits
        password.append(random.choice(string.digits))
        logger.debug("Added digit character")
    if special:
        characters += string.punctuation
        password.append(random.choice(string.punctuation))
        logger.debug("Added special character")

    remaining_length = length - len(password)
    password.extend(random.choice(characters) for _ in range(remaining_length))
    random.shuffle(password)

    final_password = "".join(password)
    logger.info(f"Generated password: {final_password}")
    return final_password


@app.get("/generate_passwords/", response_model=List[str])  # type: ignore
def create_passwords(
    length: int = Query(default=12, ge=5, le=21),
    special: bool = Query(default=False),
    uppercase: bool = Query(default=False),
    digits: bool = Query(default=False),
    count: int = Query(default=10, le=100),
) -> List[str]:
    logger.info(
        f"Request to generate {count} passwords with length={length}, special={special}, uppercase={uppercase}, digits={digits}"
    )

    try:
        passwords: List[str] = [
            generate_password(length, special, uppercase, digits) for _ in range(count)
        ]
    except Exception:
        logger.error("Error generating passwords", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    logger.info("Generated passwords successfully")
    return passwords
