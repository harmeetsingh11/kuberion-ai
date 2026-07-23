"""
Groq LLM client.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class LLM:

    def __init__(self):

        self.client = Groq(
            api_key=os.environ["GROQ_API_KEY"],
        )

        self.model = "llama-3.3-70b-versatile"

    def ask(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content
