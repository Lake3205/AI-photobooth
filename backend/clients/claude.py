from dotenv import load_dotenv
from os import environ
from anthropic import Anthropic
from base64 import b64encode

from models.assumptions import AssumptionsResponse
from constants.prompt import SYSTEM_PROMPT, USER_PROMPT
from services.image_service import ImageService

class ClaudeClient:
    load_dotenv()
    
    def __init__(self):
        self.api_key = environ.get("CLAUDE_API_KEY")
        self.max_tokens = 1000
        self.tools = [
            {
                "name": "analyse_the_image",
                "description": "build the image analysis object according to the input schema",
                "input_schema": AssumptionsResponse.model_json_schema()
            }
        ]
        
    async def generate_response(self, image, version) -> dict:
        original_bytes = await image.read()

        resized_bytes = ImageService().resize_image(original_bytes)

        base64_image = b64encode(resized_bytes).decode("utf-8")
        mime_type = getattr(image, "content_type", "") or ""
        
        self.client = Anthropic(api_key=self.api_key)
        message = self.client.messages.create(
            model = version,
            max_tokens = self.max_tokens,
            tools = self.tools,
            tool_choice = {
                "type": "tool", 
                "name": "analyse_the_image"
            },
            system=SYSTEM_PROMPT,
            messages = [
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime_type,
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            "text": USER_PROMPT
                        }
                    ]
                }
            ]
        )
        
        function_call = None
        
        if getattr(message, "content", None):
            try:
                function_call = message.content[0].input
            except Exception:
                function_call = None

        return function_call or {}
        