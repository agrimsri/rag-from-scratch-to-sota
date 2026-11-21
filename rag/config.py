"""
Configuration management for RAG pipelines.
Loads settings from .env and defines hyper-parameters and feature toggles.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

# LLM Provider Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # "ollama" or "gemini"
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))

# Gemini API Configuration (used if LLM_PROVIDER="gemini")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_MODEL_FAST = os.getenv("GEMINI_MODEL_FAST", "gemini-2.5-flash-lite")
GEMINI_RPM = int(os.getenv("GEMINI_RPM", "10"))

# Ollama Embedding Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
EMBED_NUM_CTX = int(os.getenv("EMBED_NUM_CTX", "2048"))
EMBED_DOC_PREFIX = os.getenv("EMBED_DOC_PREFIX", "search_document: ")
EMBED_QUERY_PREFIX = os.getenv("EMBED_QUERY_PREFIX", "search_query: ")

# Chunking Hyperparameters (branch 02)
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Pipeline Hyperparameters
TOP_K = int(os.getenv("TOP_K", "5"))
MIN_SCORE = float(os.getenv("MIN_SCORE", "0.35"))

# Technique Toggles for ablations and step-by-step progression
USE_HYBRID = True
USE_MULTI_QUERY = True
USE_HYDE = True
USE_RERANK = True
USE_CONTEXTUAL = True
USE_SMALL_TO_BIG = True
USE_AGENT = True
USE_CONTEXTUAL = False
USE_SMALL_TO_BIG = False
USE_AGENT = False
