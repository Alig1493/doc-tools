import asyncio
from enum import Enum
import io
from fastapi import FastAPI, HTTPException, Response, UploadFile
from pypdf import PdfWriter


app = FastAPI()


class Extensions(Enum):
    PDF = "application/pdf"

    def __str__(self):
        return self.value


async def check_and_append_pdfs(pdf_merger: PdfWriter, upload_file: UploadFile):
    if not upload_file.content_type == Extensions.PDF.value:
        raise HTTPException(400, detail="Invalid document type")
    pdf_merger.append(upload_file.file)


@app.get("/")
async def root():
    return {"status": "OK"}


@app.post("/merge/")
async def merge_pdfs(files: list[UploadFile]):
    pdf_merger = PdfWriter()
    with io.BytesIO() as merged_file_object:
        async with asyncio.TaskGroup() as tg:
            for upload_file in files:
                tg.create_task(check_and_append_pdfs(pdf_merger, upload_file))
        pdf_merger.write(merged_file_object)
        merged_file_buffer = merged_file_object.getvalue()
    headers = {"Content-Disposition": 'inline; filename="merged.pdf"'}
    return Response(
        content=merged_file_buffer, headers=headers, media_type=Extensions.PDF.value
    )
