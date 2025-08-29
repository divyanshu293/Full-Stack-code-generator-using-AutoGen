"""File upload endpoint (skeleton)."""


import shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from utils.doc_parser import parse_file
import os
router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file to a temporary location
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    # Parse the file using your parser
    raw_text, sections = parse_file(file_path)


    # Optionally, clean up the temp file
    os.remove(file_path)


    # Return results (or pass to next stage)
    return {
        "raw_text": raw_text,
        "sections": sections
    }
