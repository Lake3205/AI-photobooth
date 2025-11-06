# AI solutions

In order to analyse images and extract relevant information, we use AI models. Each model has its own strengths and weaknesses, we will be using various models to compare their performance. They will all be given the same image and roughly the same prompt. We will then be comparing their responses based on various criteria shown in the next sections.

## AI models we use

- [Anthropic's Claude](https://claude.ai/)
- [Google's Gemini](https://gemini.google.com/)
- [OpenAI's GPT-5](https://openai.com/gpt-5)

We tried to be as modular as possible in our implementation, so adding new AI models should be relatively straightforward. Each AI model has its own client in the `backend/clients` folder, which handles the communication with the respective AI API.

## Standardized return format

To ensure consistency across different AI models, we have defined a standardized return format that all AI responses should adhere to. This format includes fields for various assumptions. Each field contains a name, format, and value. The value will be filled in by the AI model based on its analysis of the input image. The full return format can be found in the [General AI return format](/docs/ai/general-ai-return-format.md) documentation.

## Comparison criteria

When comparing the different AI models, we will be looking at the following criteria:

- **Variety of assumptions**: Does the model vary its assumptions based on different images, or does it tend to give similar answers regardless of the input?
- **Accuracy of assumptions**: How accurate are the model's assumptions compared to the actual data (if available)?
- **Response time**: How long does it take for the model to generate a response?
- **Cost**: What is the cost associated with using the model, considering factors like API pricing and token usage?
- **Robustness**: How well does the model handle different types of images, including those with varying quality, lighting, and content?
- **Ethical considerations**: Does the model exhibit any biases in its assumptions? For our project, we want the AI to be biased towards individuals. This will help us highlight the ethical implications of using AI for profiling.

We will be documenting our findings in the [AI model comparison](/docs/ai/ai-model-comparison.md) documentation.

## Documentation

For more detailed information about the integration of the different AI models, please refer to their respective documentations:
- [Claude AI integration](/docs/ai/models/claude-integration.md)
- [Gemini AI integration](/docs/ai/models/gemini-integration.md)
- [GPT-5 integration](/docs/ai/models/gpt5-integration.md)