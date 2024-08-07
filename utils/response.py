from fastapi import HTTPException
from typing import Any, Dict


def create_response(
    status_code: int, success: bool, message: str, data: Any = None
) -> Dict[str, Any]:
    return {
        "status_code": status_code,
        "success": success,
        "message": message,
        "data": data,
    }


def raise_http_exception(status_code: int, message: str):
    raise HTTPException(
        status_code=status_code, detail=create_response(status_code, False, message)
    )
