import requests
import json
import config
import base64

from constants.prompt import USER_PROMPT, SYSTEM_PROMPT
from models.assumptions import AssumptionsResponse
from openai.types.chat import ChatCompletionFunctionToolParam, ChatCompletionUserMessageParam, \
    ChatCompletionContentPartTextParam, ChatCompletionContentPartImageParam
from services.image_service import ImageService
from openai import OpenAI

base_url = "https://api.openai.com/v1"

class OpenAIClient:
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        if not self.api_key or self.api_key == "None":
            return
        self.client = OpenAI(
            base_url=base_url,
            default_headers={'Authorization': f'Bearer {self.api_key}'}
        )
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

    async def generate_openai_response(self, image_bytes: bytes, filename: str, content_type: str, version) -> dict:
        # Resize image to reduce token usage
        resized_bytes = ImageService().resize_image(image_bytes)
        
        # Convert image to base64 data URL
        base64_image = base64.b64encode(resized_bytes).decode('utf-8')
        data_url = f"data:{content_type};base64,{base64_image}"
        
        messages = [
            ChatCompletionUserMessageParam(
                    role="user",
                    content=[
                        ChatCompletionContentPartTextParam(
                            type="text",
                            text=USER_PROMPT
                        ),
                        ChatCompletionContentPartImageParam(
                            type="image_url",
                            image_url={"url": data_url}
                        )
                    ]
            )]

        response = self.client.chat.completions.create(
            model=version,
            tools=self.tools,
            messages=messages,
            tool_choice="auto"
        )

        function_call = None

        if hasattr(response, "choices") and response.choices:
            try:
                tool_calls = response.choices[0].message.tool_calls
                if tool_calls:
                    arguments = tool_calls[0].function.arguments
                    function_call = json.loads(arguments)
            except Exception as e:
                print(f"Error extracting function call: {e}")
                function_call = None

        return function_call or {}
