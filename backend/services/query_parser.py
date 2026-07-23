import re 
class QueryParser:

    Blood_Groups = [ 
        "A+",
        "A-",
        "B+",
        "B-",
        "AB+",
        "AB-",
        "O+",
        "O-",
    ]

    def parse(self, query):

        filters = {}
        semantic_query = query

        for blood_group in self.Blood_Groups:

            if blood_group.lower() in query.lower():

                filters["blood_group"] = blood_group

                semantic_query = re.sub(
                    re.escape
                    (blood_group),
                    "",
                    semantic_query,
                    flags=re.IGNORECASE,
                )

        return {
            "filters": filters,
            "semantic_query": semantic_query.strip(),
        }