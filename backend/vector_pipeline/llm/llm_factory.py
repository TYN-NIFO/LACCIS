from langchain_core.language_models.chat_models import BaseChatModel
from vector_pipeline.config.settings import (
    AWS_REGION,
    BEDROCK_MODEL,
    LLM_API_KEY,
    LLM_MODEL,
    LLM_PROVIDER,
    LLM_TEMPERATURE,
)

def get_llm_instance() -> BaseChatModel:
    """
    Factory to return a generic LangChain chat model.
    Initializes dynamically based on abstract .env settings.
    """
    provider = LLM_PROVIDER.strip().lower()

    if provider == "bedrock":
        import os
        import boto3
        from langchain_aws import ChatBedrockConverse

        bedrock_client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        )
        return ChatBedrockConverse(
            model=BEDROCK_MODEL,
            region_name=AWS_REGION,
            temperature=LLM_TEMPERATURE,
            client=bedrock_client,
        )

    if not LLM_API_KEY:
        raise ValueError("LLM_API_KEY is not set in the environment.")

    if provider == "mistral":
        from langchain_mistralai import ChatMistralAI

        return ChatMistralAI(model=LLM_MODEL, mistral_api_key=LLM_API_KEY, temperature=LLM_TEMPERATURE)

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=LLM_MODEL, api_key=LLM_API_KEY, temperature=LLM_TEMPERATURE)

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=LLM_MODEL, api_key=LLM_API_KEY, temperature=LLM_TEMPERATURE)

    if provider == "google" or provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=LLM_API_KEY, temperature=LLM_TEMPERATURE)

    if provider == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(model=LLM_MODEL, api_key=LLM_API_KEY, temperature=LLM_TEMPERATURE)

    raise ValueError(f"Unsupported LLM provider: {provider}")
