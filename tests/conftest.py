import uuid
import pytest
from fastapi.testclient import TestClient
from reportlab.pdfgen.canvas import Canvas

from src.main import app


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def sample_pdf_files(request, tmp_path):
    file_paths = []
    sample_pdf_filename = "hello.pdf"

    for param in request.param:
        # The default page size is A4, which isn’t the same as the standard US letter page size.
        # The font family defaults to Helvetica with a size of 12 points.
        pdf_posix = tmp_path / (str(uuid.uuid4()) + sample_pdf_filename)
        canvas = Canvas(pdf_posix.as_posix())
        # The values passed to .drawString() are measured in user space points.
        # Since a point equals 1/72 of an inch,
        # the below code draws the string "Hello, World!"
        # one inch from the left and one inch from the bottom of the page.
        canvas.drawString(72, 72, param)
        canvas.save()
        file_paths.append(pdf_posix)
    return file_paths
