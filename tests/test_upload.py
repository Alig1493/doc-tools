from io import BytesIO
import pytest
from pypdf import PdfReader
from reportlab.pdfgen.canvas import Canvas


class TestFileUploads:
    sample_text = "Hello, World!"
    sample_pdf_filename = "hello.pdf"

    @pytest.fixture
    def sample_pdf_file(self, tmp_path):
        # The default page size is A4, which isn’t the same as the standard US letter page size.
        # The font family defaults to Helvetica with a size of 12 points.
        pdf_posix = tmp_path / self.sample_pdf_filename
        canvas = Canvas(pdf_posix.as_posix())
        # The values passed to .drawString() are measured in user space points.
        # Since a point equals 1/72 of an inch,
        # the below code draws the string "Hello, World!"
        # one inch from the left and one inch from the bottom of the page.
        canvas.drawString(72, 72, self.sample_text)
        canvas.save()
        return pdf_posix

    def test_file_upload(self, test_client, sample_pdf_file):
        pdf_reader = PdfReader(sample_pdf_file)
        assert len(pdf_reader.pages) == 1
        assert pdf_reader.pages[0].extract_text().strip() == self.sample_text
        # uplaod file to /uploadfiles endpoint
        files = [
            ("files", open(sample_pdf_file.as_posix(), "rb")),
            ("files", open(sample_pdf_file.as_posix(), "rb")),
        ]
        response = test_client.post("/merge", files=files)
        assert response.status_code == 200
        bytes_stream = BytesIO(response.read())
        pdf_reader = PdfReader(bytes_stream)
        assert len(pdf_reader.pages) == 2
        assert [page.extract_text().strip() for page in pdf_reader.pages] == [
            self.sample_text
        ] * 2
