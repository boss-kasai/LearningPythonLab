from app.routes import items
from app.routes.func import hey
from app.telemetry.mytelemetry import instrument
from fastapi import FastAPI

app = FastAPI()

# OpenTelemetry を FastAPI に適用
instrument(app)

# ルートを登録
app.include_router(items.router)


@app.get("/")
async def root() -> dict:
    return {"message": "Hello OpenTelemetry"}


@app.get("/factorial/{n}")
def factorial(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


@app.get("/hey")
def heyhey() -> dict:
    hey.hey_granme()
    hey.hey_granpa()
    return {"message": "Hey, Granme and Granpa!"}
