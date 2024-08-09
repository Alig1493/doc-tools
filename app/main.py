from enum import Enum
import io
from fastapi import FastAPI, HTTPException, Response, UploadFile
from pypdf import PdfMerger


app = FastAPI()


class Extensions(Enum):
    PDF = "application/pdf"

    def __str__(self):
        return self.value


@app.get("/")
async def root():
    return {"status": "OK"}


@app.post("/merge/")
async def merge_pdfs(files: list[UploadFile]):
    pdf_merger = PdfMerger()
    with io.BytesIO() as merged_file_object:
        for upload_file in files:
            if not upload_file.content_type == Extensions.PDF.value:
                raise HTTPException(400, detail="Invalid document type")
            pdf_merger.append(upload_file.file)
        pdf_merger.write(merged_file_object)
        merged_file_buffer = merged_file_object.getvalue()
    return Response(content=merged_file_buffer, media_type=Extensions.PDF.value)
