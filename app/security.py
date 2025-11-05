from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from config import settings
from secrets import compare_digest

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verifyApiKey(api_key: str = Depends(api_key_header)):
    api_key = api_key if api_key else ''
    if not compare_digest(api_key.encode("utf-8"),settings.API_KEY.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return
