from os import PathLike
from typing import IO, Any
from fastapi import UploadFile
from .configs import Extensions
from .exceptions import IncorrectExtension
from pypdf import PdfReader, PdfWriter


async def check_and_append_pdfs(
    index: int, pdf_merger: PdfWriter, upload_file: UploadFile
):
    if not upload_file.content_type == Extensions.PDF.value:
        raise IncorrectExtension(
            details={
                index: {
                    "filename": upload_file.filename,
                    "message": IncorrectExtension.message,
                }
            },
        )
    pdf_merger.append(upload_file.file)


async def image_quality_and_metadata_compression(
    file: str | IO[Any] | PathLike,
) -> PdfWriter:
    reader = PdfReader(file)
    writer = PdfWriter(clone_from=file)

    for page in writer.pages:
        # reduce image quality if any image exists
        for img in page.images:
            img.replace(img.image, quality=50)

    if reader.metadata is not None:
        writer.add_metadata(reader.metadata)
    return writer


async def lossless_compression(file: str | IO[Any] | PathLike) -> PdfWriter:
    writer = PdfWriter(clone_from="example.pdf")
    for page in writer.pages:
        page.compress_content_streams()  # This is CPU intensive!
    return writer
