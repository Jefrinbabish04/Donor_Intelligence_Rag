from pathlib import Path

from pypdf import PdfReader


class PDFLoader:

    def load(
        self,
        file_path,
    ):

        file_path = Path(file_path)

        reader = PdfReader(file_path)

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):

            text = page.extract_text() or ""

            pages.append(
                {
                    "page": page_number,
                    "text": text.strip(),
                }
            )

        return pages