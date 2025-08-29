# from fastapi import FastAPI
# from backend.api import health, upload, status
# from utils.logging import get_logger
# import sys, os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# logger = get_logger(__name__)


# app = FastAPI(
#     title="Multi-Agent Code Generator API",
#     description="Backend for transforming SRC to full-stack apps",
#     version="1.0.0"
# )




# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["http://localhost:8080"],  # Streamlit default port
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )
# # Log startup and shutdown
# @app.on_event("startup")
# async def startup_event():
#     logger.info("FastAPI app has started.")


# @app.on_event("shutdown")
# async def shutdown_event():
#     logger.info("FastAPI app is shutting down.")


# # Include API routes
# app.include_router(health.router)
# app.include_router(upload.router)
# app.include_router(status.router)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import health, upload, status
from utils.logging import get_logger
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = get_logger(__name__)

app = FastAPI(
    title="Multi-Agent Code Generator API",
    description="Backend for transforming SRC to full-stack apps",
    version="1.0.0"
)

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Streamlit
        "http://127.0.0.1:8501", # Streamlit alternate
       
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI app has started.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI app is shutting down.")

# Include API routes
app.include_router(health.router)
app.include_router(upload.router)
app.include_router(status.router)
