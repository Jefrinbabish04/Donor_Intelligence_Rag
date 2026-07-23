class ContextBuilder:

    def build(
        self,
        search_results,
    ):

        sections = []

        for position, result in enumerate(
            search_results,
            start=1,
        ):

            donor = result["donor"]

            distance = result["distance"]

            section = f"""
Donor {position}

Name: {donor.name}
Blood Group: {donor.blood_group}
City: {donor.city}
Hospital: {donor.hospital}
Donation Count: {donor.donation_count}
Similarity Distance: {distance:.4f}
"""

            sections.append(
                section.strip()
            )

        return "\n\n--------------------\n\n".join(
            sections
        )