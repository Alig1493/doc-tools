import asyncio
import io
from fastapi import FastAPI, Response, UploadFile
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from pypdf import PdfWriter
from .utils import check_and_append_pdfs, image_quality_and_metadata_compression
from .configs import Extensions


app = FastAPI()


@app.exception_handler(ExceptionGroup)
async def validation_exception_handler(request, exception_group: ExceptionGroup):
    errors = {}
    for exception in exception_group.exceptions:
        errors.update(exception.details())
    exc = RequestValidationError(
        errors=errors, body=f"{ExceptionGroup.__name__} errors"
    )
    return await request_validation_exception_handler(request, exc)


@app.get("/")
async def root():
    return {"status": "OK"}


@app.post("/merge/")
async def merge_pdfs(files: list[UploadFile]):
    pdf_merger = PdfWriter()
    with io.BytesIO() as merged_file_object:
        # The await is implicit when the context manager exits.
        # We wait for tasks to complete on exit
        async with asyncio.TaskGroup() as tg:
            for index, upload_file in enumerate(files):
                tg.create_task(check_and_append_pdfs(index, pdf_merger, upload_file))
        # TaskGroup raises ExceptionGroup when handling tasks
        # the real exception raised from one or more tasks is in exception.exceptions
        pdf_merger.write(merged_file_object)
        merged_file_buffer = merged_file_object.getvalue()
    headers = {"Content-Disposition": 'inline; filename="merged.pdf"'}
    return Response(
        content=merged_file_buffer, headers=headers, media_type=Extensions.PDF.value
    )


@app.post("/compress/")
async def compress_pdf(file: UploadFile):
    writer = await image_quality_and_metadata_compression(file.file)
    with io.BytesIO() as fp:
        writer.write(fp)
        compressed_file_buffer = fp.getvalue()
    headers = {"Content-Disposition": 'inline; filename="compressed.pdf"'}
    return Response(
        content=compressed_file_buffer, headers=headers, media_type=Extensions.PDF.value
    )
