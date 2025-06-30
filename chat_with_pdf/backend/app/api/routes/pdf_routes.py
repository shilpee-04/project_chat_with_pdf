from fastapi import APIRouter, UploadFile, File, status, HTTPException
from app.services.pdf_processor import PDFProcessor
from typing import List
import os

router = APIRouter()
pdf_processor = PDFProcessor()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_pdfs(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    try:
        # Create directory for vector stores if not exists
        os.makedirs("vector_stores", exist_ok=True)
        
        # Process each file
        store_ids = []
        for file in files:
            content = await file.read()
            store_id = pdf_processor.process_pdf(content, file.filename)
            store_ids.append(store_id)
        
        return {
            "message": "PDFs processed successfully", 
            "store_ids": store_ids,
            "num_files": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDFs: {str(e)}")
