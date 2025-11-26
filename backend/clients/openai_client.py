import requests
import json

from os import environ
from dotenv import load_dotenv
from constants.prompt import USER_PROMPT, SYSTEM_PROMPT
from models.assumptions import AssumptionsResponse
from openai.types.chat import ChatCompletionFunctionToolParam, ChatCompletionUserMessageParam, \
    ChatCompletionContentPartTextParam, ChatCompletionContentPartImageParam
from services.image_service import ImageService
from openai import OpenAI

load_dotenv()

async def upload_image(image_bytes: bytes, filename: str, content_type: str) -> str:
    response = requests.post(
        "https://catbox.moe/user/api.php",
        data={"reqtype": "fileupload"},
        files={"fileToUpload": (filename, image_bytes, content_type)}
    )
    if response.status_code == 200:
        return response.text.strip()
    else:
        raise Exception(f"Catbox upload failed: {response.status_code} - {response.text}")

class OpenAIClient:
    def __init__(self):
        self.api_key = environ.get('OPENAI_API_KEY')
        self.client = OpenAI(
            base_url=environ.get('OPENAI_API_BASE_URL'),
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
        image_url = await upload_image(image_bytes, filename, content_type)
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
                            image_url={"url": image_url}
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

        # Extract the function call from the tool_calls
        if hasattr(response, "choices") and response.choices:
            try:
                tool_calls = response.choices[0].message.tool_calls
                if tool_calls:
                    # Get the arguments from the first tool call
                    arguments = tool_calls[0].function.arguments
                    # Parse the JSON string into a dictionary
                    function_call = json.loads(arguments)
            except Exception as e:
                print(f"Error extracting function call: {e}")
                function_call = None

        return function_call or {}
