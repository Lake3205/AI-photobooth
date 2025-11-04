from base64 import b64encode
from os import environ
from dotenv import load_dotenv

from constants.prompt import USER_PROMPT, SYSTEM_PROMPT
from models.assumptions import AssumptionsResponse
from openai.types.chat import ChatCompletionFunctionToolParam
from services.image_service import ImageService
from openai import OpenAI


class OpenAIClient:
    load_dotenv()

    def __init__(self):
        self.api_key = environ.get('OPENAI_API_KEY')
        self.tools = [
            ChatCompletionFunctionToolParam(
                type="function",
                function={
                    "name": "analyse_the_image",
                    "description": "Build the image analysis object according to the input schema",
                    "parameters": AssumptionsResponse.model_json_schema()
                }
            )
        ]

    async def generate_openai_response(self, image, version) -> dict:
        original_bytes = await image.read()

        resized_bytes = ImageService().resize_image(original_bytes)

        base64_image = b64encode(resized_bytes).decode("utf-8")
        mime_type = getattr(image, "content_type", "") or ""

        self.client = OpenAI()
        response = self.client.chat.completions.create(
            model=version,
            tools=self.tools,
            messages=[
            ]
        )

        function_call = None

        if getattr(response, "content", None):
            try:
                function_call = response.content[0].input
            except Exception:
                function_call = None

        return function_call or {}
