"""Status endpoint (skeleton)."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/status", tags=["Status"])
def check_status():
    """Returns processing status (placeholder)."""
    return {"message": "Status endpoint under construction"}
