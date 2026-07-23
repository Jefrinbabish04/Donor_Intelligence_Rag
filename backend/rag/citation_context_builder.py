class CitationContextBuilder:

    def build(self, results):
        sections = []

        for item in results:
            if item["source"] == "donor":
                donor = item["data"]["donor"]

                sections.append(
                    f"""
=== DONOR ===

Name: {donor.name}

Blood Group: {donor.blood_group}

Hospital: {donor.hospital}

City: {donor.city}

Similarity Score: {item['data']['distance']}
"""
                )

            elif item["source"] == "document":
                document = item["data"]

                sections.append(
                    f"""
=== DOCUMENT ===

Source: {document['filename']}

Page: {document['page']}

Chunk: {document['chunk']}

Similarity Score: {document['score']}

Content:

{document['text']}
"""
                )

        return "\n\n".join(sections)
