"""
LLM abstraction layer supporting Ollama (local) and Gemini API (cloud).
Provides caching, retry with exponential backoff, rate-limiting, and call counting.
"""

import json
import re
import time
from typing import Any, Dict, Optional
import ollama

from rag import cache, config

_LLM_CALL_COUNT = 0
_LAST_CALL_TIME = 0.0


def get_call_count() -> int:
    global _LLM_CALL_COUNT
    return _LLM_CALL_COUNT


def reset_call_count() -> None:
    global _LLM_CALL_COUNT
    _LLM_CALL_COUNT = 0


def _rate_limit_gemini():
    global _LAST_CALL_TIME
    if config.GEMINI_RPM > 0:
        min_interval = 60.0 / config.GEMINI_RPM
        elapsed = time.time() - _LAST_CALL_TIME
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        _LAST_CALL_TIME = time.time()


def generate(
    prompt: str,
    system_prompt: str = "",
    model_override: Optional[str] = None,
    temperature: Optional[float] = None,
) -> str:
    """Generates plain text using the configured LLM provider with caching."""
    global _LLM_CALL_COUNT
    provider = config.LLM_PROVIDER.lower()
    temp = config.LLM_TEMPERATURE if temperature is None else temperature

    if provider == "gemini" and config.GEMINI_API_KEY:
        model = model_override or config.GEMINI_MODEL
    else:
        provider = "ollama"
        model = model_override or config.LLM_MODEL

    cache_key = cache.hash_key(
        {
            "provider": provider,
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "temp": temp,
        }
    )
    cached = cache.get("llm_text", cache_key)
    if cached is not None:
        return cached

    _LLM_CALL_COUNT += 1

    if provider == "gemini" and config.GEMINI_API_KEY:
        from google import genai
        from google.genai import types

        _rate_limit_gemini()
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        for attempt in range(5):
            try:
                resp = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt or None,
                        temperature=temp,
                    ),
                )
                text = resp.text or ""
                cache.set("llm_text", cache_key, text)
                return text
            except Exception as e:
                if attempt == 4:
                    raise
                time.sleep(2**attempt)
        return ""
    else:
        # Ollama local generation
        client = ollama.Client(host=config.OLLAMA_HOST)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(3):
            try:
                resp = client.chat(
                    model=model,
                    messages=messages,
                    options={"temperature": temp, "num_predict": 96},
                )
                text = resp["message"]["content"]
                cache.set("llm_text", cache_key, text)
                return text
            except Exception as e:
                if attempt == 2:
                    raise
                time.sleep(1.0)
        return ""


def generate_json(
    prompt: str,
    system_prompt: str = "",
    schema: Optional[Dict[str, Any]] = None,
    model_override: Optional[str] = None,
) -> Dict[str, Any]:
    """Generates structured JSON using the configured LLM provider with caching."""
    global _LLM_CALL_COUNT
    provider = config.LLM_PROVIDER.lower()
    temp = 0.0

    if provider == "gemini" and config.GEMINI_API_KEY:
        model = model_override or config.GEMINI_MODEL_FAST
    else:
        provider = "ollama"
        model = model_override or config.LLM_MODEL

    cache_key = cache.hash_key(
        {
            "provider": provider,
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "schema": schema,
            "json": True,
        }
    )
    cached = cache.get("llm_json", cache_key)
    if cached is not None:
        return json.loads(cached)

    _LLM_CALL_COUNT += 1

    if provider == "gemini" and config.GEMINI_API_KEY:
        from google import genai
        from google.genai import types

        _rate_limit_gemini()
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        for attempt in range(5):
            try:
                gen_cfg = types.GenerateContentConfig(
                    system_instruction=system_prompt or None,
                    temperature=0.0,
                    response_mime_type="application/json",
                )
                resp = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=gen_cfg,
                )
                raw_text = resp.text or "{}"
                parsed = json.loads(raw_text)
                cache.set("llm_json", cache_key, json.dumps(parsed))
                return parsed
            except Exception as e:
                if attempt == 4:
                    raise
                time.sleep(2**attempt)
        return {}
    else:
        client = ollama.Client(host=config.OLLAMA_HOST)
        instruction = "Respond ONLY with valid JSON conforming to the requested schema. No prose."
        full_system = f"{system_prompt}\n{instruction}".strip()
        messages = [
            {"role": "system", "content": full_system},
            {"role": "user", "content": prompt},
        ]
        for attempt in range(3):
            try:
                resp = client.chat(
                    model=model,
                    messages=messages,
                    format="json",
                    options={"temperature": 0.0},
                )
                raw_text = resp["message"]["content"]
                parsed = json.loads(raw_text)
                cache.set("llm_json", cache_key, json.dumps(parsed))
                return parsed
            except Exception:
                if attempt == 2:
                    # Fallback extraction from markdown code block
                    m = re.search(r"\{.*\}", raw_text, re.DOTALL)
                    if m:
                        return json.loads(m.group(0))
                    return {}
                time.sleep(1.0)
        return {}
