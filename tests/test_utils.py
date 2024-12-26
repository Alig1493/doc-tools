import asyncio
import time
import pytest
import pytest_asyncio
from src.utils import image_quality_and_metadata_compression, lossless_compression


class TestCompression:
    @pytest_asyncio.fixture
    async def tag_functions(self):
        async def tag(function, *args, **kwargs):
            start = time.time()
            function(*args, **kwargs)
            difference = time.time() - start
            # print(f"Returning function {function.__name__} and took {time.time() - start} seconds")
            return function.__name__, difference

        return tag

    @pytest.mark.asyncio
    async def test_image_compression(self, sample_pdf_image_file, tag_functions):
        async def test_run():
            tasks = [
                tag_functions(
                    image_quality_and_metadata_compression, sample_pdf_image_file
                ),
                tag_functions(lossless_compression, sample_pdf_image_file),
            ]
            responses = {}
            for future in asyncio.as_completed(tasks, timeout=5):
                function_name, time_taken = await future
                responses[function_name] = time_taken

            assert (
                responses[lossless_compression.__name__]
                > responses[image_quality_and_metadata_compression.__name__]
            )

        # run test an averae of 10 times and check if lossless compression takes more time more than 50% of the time
        success = 0
        failure = 0
        total = 10
        for _ in range(total):
            try:
                await test_run()
                success += 1
            except AssertionError:
                failure += 1
        success_percent = ((total - success) / total) * 100
        assert success_percent > 50
