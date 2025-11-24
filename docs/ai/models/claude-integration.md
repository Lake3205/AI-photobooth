# Claude integration

This document provides an overview of the integration of Anthropic's Claude AI model into our system. It covers the setup process, API usage, and specific considerations for working with Claude.

## Setup

To integrate Claude into our system, follow these steps:

1. **API Key**: Obtain an API key from Anthropic by [signing up](https://claude.ai/login?returnTo=%2F%3F). 
2. **.env Configuration**: Add the API key to your `.env` file in the backend directory:
   ```
   CLAUDE_API_KEY=your_api_key_here
   ```
3. **Install Dependencies**: Ensure that the `anthropic` Python package is installed. You can install it via the requirements file:
   ```
   pip install -r requirements.txt
   ```

## Usage

The Claude client is implemented in `backend/clients/claude.py`. It uses the Anthropic SDK to communicate with the Claude API. The main method for generating responses is `generate_response`, which takes an image and a model version as input and returns a structured JSON response based on our standardized return format.

### Controller

The responses can be accessed through the controller endpoint defined in `backend/controllers/assumptions_controller.py`. The endpoint used for all AI models, including Claude, is:

```
POST /assumptions/generate
```

The endpoint accepts an image file and an ai model as its parameters. To access Claude specifically, make sure the `ai_model` parameter is set as `"claude"`.

## Considerations

Unlike the other AI models integrated into our system, Claude does not have a free tier. Ensure that you monitor your usage and costs. 
