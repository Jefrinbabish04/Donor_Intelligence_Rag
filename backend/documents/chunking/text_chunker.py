class TextChunker:

    CHUNK_SIZE = 500

    CHUNK_OVERLAP = 100

    def chunk(
        self,
        pages,
    ):

        chunks = []

        for page in pages:

            text = page["text"]

            page_number = page["page"]

            start = 0

            chunk_number = 1

            while start < len(text):

                end = start + self.CHUNK_SIZE

                chunk_text = text[start:end]

                chunks.append(
                    {
                        "page": page_number,
                        "chunk": chunk_number,
                        "text": chunk_text.strip(),
                    }
                )

                start += (
                    self.CHUNK_SIZE
                    - self.CHUNK_OVERLAP
                )

                chunk_number += 1

        return chunks
    