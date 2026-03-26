"""
reasoning.py — Calls LLM for legal clause analysis.
Primary: AWS Bedrock (Mistral Large)
Fallback: Mistral API direct
"""
import os
import json
import logging
from vector_pipeline.config.settings import (
    LLM_PROVIDER, MISTRAL_API_KEY, MISTRAL_MODEL, MISTRAL_TEMPERATURE,
    AWS_REGION, BEDROCK_MODEL
)

logger = logging.getLogger(__name__)


def _call_bedrock(prompt: str) -> str:
    """Call Mistral via AWS Bedrock."""
    import boto3, os
    client = boto3.client(
        "bedrock-runtime",
        region_name=AWS_REGION,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    )
    body = json.dumps({
        "prompt": f"<s>[INST] {prompt} [/INST]",
        "max_tokens": 1024,
        "temperature": MISTRAL_TEMPERATURE,
    })
    response = client.invoke_model(
        modelId=BEDROCK_MODEL,
        body=body,
        contentType="application/json",
        accept="application/json"
    )
    result = json.loads(response["body"].read())
    return result["outputs"][0]["text"]


def _call_mistral(prompt: str) -> str:
    """Call Mistral API directly (fallback)."""
    from mistralai import Mistral
    client = Mistral(api_key=MISTRAL_API_KEY)
    res = client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content


def _call_llm(prompt: str) -> str:
    """Call LLM with Bedrock primary, Mistral fallback."""
    if LLM_PROVIDER == "bedrock":
        try:
            return _call_bedrock(prompt)
        except Exception as e:
            logger.warning(f"Bedrock failed, falling back to Mistral: {e}")
            if MISTRAL_API_KEY:
                return _call_mistral(prompt)
            raise
    elif MISTRAL_API_KEY:
        return _call_mistral(prompt)
    else:
        raise RuntimeError("No LLM provider configured (set LLM_PROVIDER=bedrock or MISTRAL_API)")


def run_llm_reasoning(item: dict) -> str:
    """Legacy function: called during background pipeline for high-risk clauses."""
    try:
        prompt = f"""You are a legal contract analyst. Analyze this clause briefly.

Clause Type: {item.get('clause', 'Unknown')}
Risk Level: {item.get('final_risk', 'Unknown')}
Clause Text: {item.get('content', '')[:800]}

Give:
1. Why it is risky (2-3 sentences)
2. One clear suggestion to improve it

Be concise and professional."""
        return _call_llm(prompt)
    except Exception as e:
        logger.error(f"LLM reasoning failed: {e}")
        return f"Analysis unavailable: {str(e)}"


def compare_clauses(client_clause: str, standard_clause: str, clause_type: str, risk: str) -> str:
    """Compares client clause vs standard clause and gives reasoning + suggestions."""
    try:
        has_standard = bool(standard_clause and standard_clause.strip())

        if has_standard:
            prompt = f"""You are a legal contract analyst. Compare these two clauses and give a concise review.

Clause Type: {clause_type}
Risk Level: {risk}

CLIENT CLAUSE (uploaded contract):
{client_clause[:1000]}

STANDARD CLAUSE (reference template):
{standard_clause[:800]}

Provide:
1. **Key Differences** — What is different between the two?
2. **Risk Reasoning** — Why is the client clause risky or acceptable?
3. **Suggestion** — One clear, specific improvement to the client clause.

Keep it brief and professional. No bullet sub-points, no headers beyond the 3 above."""
        else:
            prompt = f"""You are a legal contract analyst. Review this clause.

Clause Type: {clause_type}
Risk Level: {risk}

CLIENT CLAUSE:
{client_clause[:1000]}

Provide:
1. **Risk Reasoning** — Why is this clause risky or acceptable?
2. **Suggestion** — One specific improvement.

Keep it brief and professional."""

        return _call_llm(prompt)
    except Exception as e:
        logger.error(f"LLM comparison failed: {e}")
        return f"Analysis unavailable: {str(e)}"
