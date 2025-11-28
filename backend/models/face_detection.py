from pydantic import BaseModel

class FaceDetectionResponse(BaseModel):
    face_detected: bool