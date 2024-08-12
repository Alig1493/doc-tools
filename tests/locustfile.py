import io
from reportlab.pdfgen.canvas import Canvas
from locust import HttpUser, task, between


class PDFOperations(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def test_pdf_merge(self):
        with io.BytesIO() as upload_file:
            canvas = Canvas(upload_file)
            canvas.drawString(72, 72, "Some content")
            canvas.save()
            self.client.post(
                "/merge",
                files=[
                    ("files", ("sample.pdf", upload_file.getvalue(), "application/pdf"))
                ],
            )
