from contextlib import ExitStack
from io import BytesIO
import pytest
from pypdf import PdfReader


class TestFileUploads:
    @pytest.mark.parametrize("sample_pdf_files", [["Hello", "World"]], indirect=True)
    def test_file_upload(self, sample_pdf_files, test_client):
        with ExitStack() as stack:
            files = [
                ("files", stack.enter_context(open(fname.as_posix(), "rb")))
                for fname in sample_pdf_files
            ]
            response = test_client.post("/merge", files=files)
        assert response.status_code == 200
        assert (
            response.headers["content-disposition"] == 'inline; filename="merged.pdf"'
        )
        assert response.headers["content-type"] == "application/pdf"
        bytes_stream = BytesIO(response.read())
        pdf_reader = PdfReader(bytes_stream)
        assert len(pdf_reader.pages) == 2
        assert [page.extract_text().strip() for page in pdf_reader.pages] == [
            "Hello",
            "World",
        ]
