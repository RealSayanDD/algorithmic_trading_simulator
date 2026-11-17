from fastapi import FastAPI

from src.api.auth import router as auth_router
from src.core.config import get_settings

app = FastAPI(title=get_settings().app_name)
app.include_router(auth_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
