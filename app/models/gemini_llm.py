from langchain.llms.base import LLM
import google.generativeai as genai
import os
from typing import Optional, List
from pydantic import BaseModel, Field


class GeminiLLM(LLM):
    model_name: str = Field(default="gemini-2.0-flash")
    temperature: float = Field(default=0.0)

    def __init__(self, model_name: Optional[str] = None, temperature: float = 0.0):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        values = {
            "model_name": model_name or "gemini-2.0-flash",
            "temperature": temperature,
        }

        super().__init__(**values)

    @property
    def _llm_type(self) -> str:
        return "gemini-2.0-flash"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        model = genai.GenerativeModel(self.model_name)
        config = {"temperature": self.temperature}
        if stop:
            config["stop_sequences"] = stop

        response = model.generate_content(
            prompt,
            generation_config=config
        )

        try:
            return response.text
        except:
            return str(response)
