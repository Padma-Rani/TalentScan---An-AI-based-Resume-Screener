"""
app/ai/model_manager.py

Shared AI Model Manager.

Loads the LLM (Qwen2.5-1.5B-Instruct) and the sentence-transformer
embedding model exactly once per process, and hands out the same
instances to every part of the application. Nothing else in the
codebase should call `from_pretrained(...)` or `SentenceTransformer(...)`
directly - always go through `ModelManager.get_instance()`.
"""
from __future__ import annotations

import sys
import threading
from typing import List, Optional

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer

from app.core.config import MODEL_CONFIG


class ModelManager:
    """
    Singleton wrapper around the shared LLM and embedding model.

    Usage:
        manager = ModelManager.get_instance()
        text = manager.generate(prompt, system_prompt="...")
        vectors = manager.embed(["Java", "Python"])
    """

    _instance: Optional["ModelManager"] = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        if ModelManager._instance is not None:
            raise RuntimeError(
                "ModelManager is a singleton. Use ModelManager.get_instance() "
                "instead of constructing it directly."
            )

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print("Loading shared AI model...")
        print(f"  LLM: {MODEL_CONFIG.LLM_MODEL_NAME}")
        print(f"  Device: {self.device}")
        print("Downloading/loading model (first run may take a while)...")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_CONFIG.LLM_MODEL_NAME)
            self.llm = AutoModelForCausalLM.from_pretrained(
                MODEL_CONFIG.LLM_MODEL_NAME,
                torch_dtype=torch.float32 if self.device == "cpu" else torch.float16,
            ).to(self.device)
            self.llm.eval()
        except Exception as exc:  # pragma: no cover - environment dependent
            print(
                f"[FATAL] Could not load LLM '{MODEL_CONFIG.LLM_MODEL_NAME}': {exc}\n"
                "Check your internet connection (the first run downloads the "
                "model from Hugging Face, ~3 GB) and available disk space.",
                file=sys.stderr,
            )
            raise

        try:
            print(f"  Embedding model: {MODEL_CONFIG.EMBEDDING_MODEL_NAME}")
            self.embedding_model = SentenceTransformer(
                MODEL_CONFIG.EMBEDDING_MODEL_NAME, device=self.device
            )
        except Exception as exc:  # pragma: no cover - environment dependent
            print(
                f"[FATAL] Could not load embedding model "
                f"'{MODEL_CONFIG.EMBEDDING_MODEL_NAME}': {exc}",
                file=sys.stderr,
            )
            raise

        print("AI model loaded successfully.")

    @classmethod
    def get_instance(cls) -> "ModelManager":
        """Return the single shared ModelManager, creating it on first call."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance_for_testing(cls) -> None:
        """Only used by tests that need a clean singleton state."""
        cls._instance = None

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Run one chat-style generation and return the raw decoded text."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        chat_text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer(chat_text, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output_ids = self.llm.generate(
                **inputs,
                max_new_tokens=MODEL_CONFIG.LLM_MAX_NEW_TOKENS,
                temperature=MODEL_CONFIG.LLM_TEMPERATURE,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        generated_ids = output_ids[0][inputs["input_ids"].shape[1]:]
        response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        return response.strip()

    def embed(self, texts: List[str]):
        """Return embeddings (numpy array) for a list of short strings."""
        if not texts:
            return []
        return self.embedding_model.encode(texts, convert_to_numpy=True)
