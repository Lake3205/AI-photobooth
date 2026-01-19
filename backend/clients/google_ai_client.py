from google import genai
from google.genai import types

from models.assumptions import AssumptionsResponse

from constants.prompt import USER_PROMPT, SYSTEM_PROMPT

from constants.model_version_constants import GEMINI_MODEL_VERSION
import config  # Load environment configuration

from models.face_detection import FaceDetectionResponse


class GoogleAIClient:
    def __init__(self):
        self.API_KEY = config.GEMINI_API_KEY
        self.MODEL = GEMINI_MODEL_VERSION

    async def call_gemini_api(self, image_bytes: bytes, mime_type: str):
        genai_client = genai.Client()
        response = genai_client.models.generate_content(
            model=self.MODEL,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AssumptionsResponse,
                system_instruction=SYSTEM_PROMPT,
                thinking_config=types.ThinkingConfig(include_thoughts=True)
            ),
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type
                ),
                USER_PROMPT
            ],
        )

        thought = None
        for part in response.candidates[0].content.parts:
            if part.thought == False:
                break
            if part.text:
                thought = part.text
                break

        return response.parsed, thought

    async def detect_face(self, image_bytes: bytes, mime_type: str):
        genai_client = genai.Client()
        response = genai_client.models.generate_content(
            model=self.MODEL,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=FaceDetectionResponse,
            ),
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type
                ),
                "Analyze the given image and detect whether there's a human face or not."
            ],
        )

        return response.parsed
