from contextlib import ExitStack
from io import BytesIO
import pytest
from pypdf import PdfReader
from src.exceptions import IncorrectExtension


class TestFileMerge:
    @pytest.mark.parametrize(
        "sample_pdf_files",
        [
            ["Hello", "World"],
            ["Hello"],
        ],
        indirect=True,
    )
    def test_file_upload(self, sample_pdf_files, test_client):
        expected_output = [
            PdfReader(pdf_file.as_posix()).pages[0].extract_text()
            for pdf_file in sample_pdf_files
        ]
        expected_pages_length = len(sample_pdf_files)

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
        assert len(pdf_reader.pages) == expected_pages_length
        assert [page.extract_text() for page in pdf_reader.pages] == expected_output

    def test_non_pdf_files(self, test_client):
        filename = "sample.txt"
        with BytesIO() as upload_file:
            upload_file.write(b"some content")
            upload_file.seek(0)
            files = [("files", (filename, upload_file.getvalue(), "text/plain"))]
            response = test_client.post("/merge", files=files)
            assert response.status_code == 422
            assert response.json() == {
                "detail": {
                    "0": {"filename": filename, "message": IncorrectExtension.message}
                }
            }
