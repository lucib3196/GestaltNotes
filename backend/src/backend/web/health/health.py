import firebase_admin
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from starlette import status
from backend.web.dependencies import SessionDep

router = APIRouter(tags=["Health"], prefix="/health")


@router.get("/live", status_code=status.HTTP_200_OK)
def startup_connection():
    return {"message": "The API is LIVE!!", "status": "ok", "service": "backend"}


@router.get("/db", status_code=status.HTTP_200_OK)
def database_health(session: SessionDep):
    try:
        result = session.execute(text("SELECT 1")).scalar_one()
        return {
            "status": "ok",
            "database": "connected",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {e}",
        ) from e


@router.get("/firebase")
def firebase_health():
    try:
        app = firebase_admin.get_app()
        return {
            "status": "ok",
            "firebase": "initialized",
            "project_id": app.project_id,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Firebase Admin app is not initialized",
        ) from e


