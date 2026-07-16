from abc import ABC, abstractmethod
from google import genai
from mistralai.client import Mistral
import logging

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, text: str, system: str = "") -> str: ...

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-3.1-flash-lite"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def generate(self, text: str, system: str = "" ):
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=text,
            config = genai.types.GenerateContentConfig(system_instruction = system)
        )
        return response.text

class MistralProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "mistral-small-latest"):
        self.client = Mistral(api_key=api_key)
        self.model = model

    async def generate(self, text: str, system: str = ""):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": text})
        
        response = await self.client.chat.complete_async(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content

class FallbackProvider(LLMProvider):
    def __init__(self, providers: list[LLMProvider]):
        self.providers = providers

    async def generate(self, text: str, system: str = ""):
        response = "Unfortunately something went wrong and none of the providers worked correctly"
        for provider in self.providers:
            try:
                content = await provider.generate(text, system)
                if not content:
                    raise ValueError("Text from provider was None!")
            except Exception as e:
                logger.warning(f"{type(provider).__name__} has failed: {e}")
            else:
                logger.info(f"{type(provider).__name__} has successfully responded")
                response = content
                break
        return response