from abc import ABC, abstractmethod
from google import genai

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, text: str) -> str: ...

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-3.1-flash-lite"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def generate(self, text):
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=text,
        )
        return response.text