import ollama


class LLMService:

    MODEL = "llama3.2"

    def generate(
        self,
        prompt,
    ):

        try:

            response = ollama.chat(
                model=self.MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            return response["message"]["content"]

        except Exception as error:

            raise RuntimeError(
                f"LLM generation failed: {error}"
            )