# Bu dosya, FastAPI için özel bir HTTP hata işleyicisi tanımlar.
# HTTPException oluştuğunda JSON formatında hata mesajı döndürür.

from fastapi.responses import JSONResponse
from fastapi import HTTPException

async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
