# Backend UML 

This contains UML diagrams (class and sequence) describing the structure and runtime flow of our backend.

## Class diagram

```mermaid
classDiagram

    %% Models
    class AssumptionsResponse {
      +ethnicity: Enum
      +religion: Enum
      +political_opinion: Enum
      +theft_risk: float
      +age: int
      +weight: int
      +school_level: Enum
      +salary: int
      +debt: int
    }

    class AssumptionsModel {
      -model: str
      -version: str
      -assumptions: dict
      +to_dict(): dict
      +set_assumption_value(key, value)
    }

    %% Services & clients
    class AssumptionsService {
      +get_assumptions(ai_model: str, image) : dict
    }

    class ImageService {
      +resize_image(image_bytes) : bytes
    }

    class ClaudeClient {
      -api_key: str
      -model: str
      +generate_response(image_bytes, mime_type) : dict
    }

    %% Controllers
    class AssumptionsController {
      +generate_assumptions(image: UploadFile, ai_model: str)
    }

    class main {
      +app: FastAPI
      +include_routers()
    }


    AssumptionsController --> AssumptionsService
    AssumptionsService --> ClaudeClient
    AssumptionsService --> ImageService 
  AssumptionsController --> AssumptionsModel : creates
  AssumptionsService --> AssumptionsModel : updates
    ClaudeClient --> AssumptionsResponse 
    main --> AssumptionsController 


```

## Sequence diagram (POST /assumptions/generate)

```mermaid
sequenceDiagram
    participant Client
    participant Controller as AssumptionsController
    participant Service as AssumptionsService
    participant ImageSvc as ImageService
    participant Claude as ClaudeClient
    participant Anthropic

    Client->>Controller: POST /assumptions/generate (image, ai_model)
    Controller->>Service: get_assumptions(ai_model, image)
    Service->>ImageSvc: read image bytes
    ImageSvc-->>Service: resized image bytes
    Service->>Claude: generate_response(image_bytes, mime_type)
    Claude->>Anthropic: messages.create(... tool_input ...)
    Anthropic-->>Claude: tool output (analysis dict)
    Claude-->>Service: analysis dict
    Service-->>Controller: assumptions dict
    Controller-->>Client: 200 OK (assumptions)

```

## Notes

- The diagrams reflect the current implementation where `AssumptionsService` reads the incoming `UploadFile`, optionally resizes the image via `ImageService`, encodes the image and passes it to `ClaudeClient.generate_response`.
- `ClaudeClient` constructs a tool input (base64 + mime type) for Anthropic and returns the tool output as a dict to the service.