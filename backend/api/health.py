"""Health check endpoint."""


from fastapi import APIRouter


router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    """Returns API health status."""
    return {"status": "ok"}
