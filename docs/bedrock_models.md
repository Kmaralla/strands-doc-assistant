# Amazon Bedrock Models for Strands

This guide provides information about using Amazon Bedrock models with Strands agents.

## Available Models

Amazon Bedrock provides access to various foundation models from leading AI companies. Here are some of the models you can use with Strands:

### Anthropic Claude Models

- **anthropic.claude-3-sonnet-20240229-v1:0**
  - General purpose model with strong reasoning capabilities
  - Good for complex tasks and conversations
  - Supports up to 200K tokens context

- **anthropic.claude-3-haiku-20240307-v1:0**
  - Faster, more efficient model
  - Good for simpler tasks and quick responses
  - Supports up to 200K tokens context

- **anthropic.claude-instant-v1**
  - Fastest Claude model
  - Good for high-throughput applications
  - Lower cost than other Claude models

### Amazon Titan Models

- **amazon.titan-text-express-v1**
  - General purpose text model
  - Good balance of performance and cost
  - Supports up to 8K tokens context

- **amazon.titan-text-lite-v1**
  - Lightweight text model
  - Good for simple text generation tasks
  - Lower cost than Express

### AI21 Jurassic Models

- **ai21.j2-ultra-v1**
  - General purpose text model
  - Good for complex reasoning tasks
  - Supports up to 8K tokens context

- **ai21.j2-mid-v1**
  - Mid-tier text model
  - Good balance of performance and cost

## Using Bedrock Models with Strands

To use a Bedrock model with Strands, you need to initialize a `BedrockLanguageModel` with the appropriate model ID:

```python
from strands.language_model import BedrockLanguageModel

# Initialize the Bedrock language model
llm = BedrockLanguageModel(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    region_name="us-east-1",
    profile_name="default"  # Optional
)
```

## Model Selection Guidelines

When choosing a model for your Strands agent, consider the following factors:

1. **Task Complexity**: More complex tasks require more capable models
2. **Response Speed**: Simpler models generally respond faster
3. **Cost**: More capable models typically cost more
4. **Context Length**: Some tasks require longer context windows
5. **Specific Capabilities**: Some models excel at specific tasks

## Model Parameters

You can customize the behavior of Bedrock models by adjusting parameters:

```python
from strands.language_model import BedrockLanguageModel

# Initialize with custom parameters
llm = BedrockLanguageModel(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    region_name="us-east-1",
    model_kwargs={
        "temperature": 0.7,  # Controls randomness (0.0 to 1.0)
        "top_p": 0.9,        # Controls diversity
        "max_tokens": 1000   # Maximum response length
    }
)
```

## AWS Permissions

To use Bedrock models, your AWS credentials must have the following permissions:

- `bedrock:InvokeModel`
- `bedrock:ListFoundationModels`

You can create an IAM policy with these permissions and attach it to your user or role.

## Cost Management

To manage costs when using Bedrock models:

1. Choose the appropriate model for your task
2. Set reasonable `max_tokens` limits
3. Monitor usage with AWS Cost Explorer
4. Consider using model throughput optimization techniques
5. Use caching for repeated queries

## Best Practices

1. **Error Handling**: Implement robust error handling for model invocations
2. **Retries**: Use exponential backoff for retries on transient errors
3. **Prompt Engineering**: Craft effective prompts to get the best results
4. **Validation**: Validate model outputs before using them
5. **Monitoring**: Monitor model performance and costs
