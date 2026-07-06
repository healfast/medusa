"""
Local LLM inference using llama-cpp-python.
Supports GGUF models (Llama, Mistral, Phi, etc.) without API keys.
"""

import os
import threading
from typing import Optional, List, Dict, Any

# Global LLM instance (lazy-loaded)
_llm_instance = None
_llm_lock = threading.Lock()


def get_default_model_path() -> str:
    """Return the default GGUF model path."""
    # Check common locations
    candidates = [
        os.path.expanduser("~/models/phi-3-mini-4k-instruct-Q4_K_M.gguf"),
        os.path.expanduser("~/models/tinyllama-1.1b-Q4_K_M.gguf"),
        os.path.expanduser("~/models/llama-2-7b-chat-Q4_K_M.gguf"),
        os.path.join(os.path.dirname(__file__), "models", "phi-3-mini-4k-instruct-Q4_K_M.gguf"),
        os.path.join(os.path.dirname(__file__), "models", "tinyllama-1.1b-Q4_K_M.gguf"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return ""  # No default model found


def load_llm(model_path: Optional[str] = None, **kwargs) -> Any:
    """
    Load a GGUF model using llama-cpp-python.
    Args:
        model_path: Path to the GGUF file. If None, uses default.
        **kwargs: Additional args for Llama (e.g., n_ctx, n_threads).
    Returns:
        Loaded Llama instance.
    """
    global _llm_instance
    
    if model_path is None:
        model_path = get_default_model_path()
    
    if not model_path:
        raise ValueError(
            "No GGUF model found. Please specify a model path or download one. "
            "Example models: Phi-3-mini-4k-instruct, TinyLlama-1.1B, Llama-2-7B. "
            "Download from: https://huggingface.co/models?library=gguf"
        )
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    with _llm_lock:
        if _llm_instance is None:
            try:
                from llama_cpp import Llama
                
                # Default kwargs for better performance
                default_kwargs = {
                    "n_ctx": 2048,  # Context window
                    "n_threads": max(1, os.cpu_count() // 2),  # Use half CPU threads
                    "n_gpu_layers": 0,  # Disable GPU by default (set to -1 for auto)
                    "verbose": False,
                }
                default_kwargs.update(kwargs)
                
                _llm_instance = Llama(model_path, **default_kwargs)
                print(f"[Medusa] Loaded local LLM: {model_path}")
            except ImportError:
                raise ImportError(
                    "llama-cpp-python is not installed. Run: pip install llama-cpp-python"
                )
        return _llm_instance


def generate_local_reply(
    prompt: str,
    model_path: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 512,
    system_prompt: Optional[str] = None,
    **kwargs,
) -> str:
    """
    Generate a reply using the local LLM.
    Args:
        prompt: User prompt.
        model_path: Path to GGUF model (optional).
        temperature: Sampling temperature (0.0-1.0).
        max_tokens: Maximum tokens to generate.
        system_prompt: Optional system prompt.
        **kwargs: Additional args for Llama.
    Returns:
        Generated text.
    """
    try:
        llm = load_llm(model_path, **kwargs)
    except Exception as e:
        return f"Failed to load local LLM: {e}"
    
    try:
        # Build the prompt
        if system_prompt:
            full_prompt = f"<s>[INST] {system_prompt} [/INST]\n{prompt}</s>"
        else:
            full_prompt = prompt
        
        # Generate response
        response = llm(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=["</s>"],
            echo=False,
        )
        
        # Extract text from response
        if isinstance(response, dict):
            return response.get("choices", [{}])[0].get("text", "").strip()
        else:
            return str(response).strip()
    except Exception as e:
        return f"Local LLM generation failed: {e}"


def unload_llm() -> None:
    """Unload the LLM to free memory."""
    global _llm_instance
    with _llm_lock:
        _llm_instance = None
        print("[Medusa] Unloaded local LLM")


def list_available_models() -> List[str]:
    """List GGUF models in common directories."""
    search_dirs = [
        os.path.expanduser("~/models"),
        os.path.join(os.path.dirname(__file__), "models"),
    ]
    models = []
    for dir_path in search_dirs:
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                if file.endswith(".gguf"):
                    models.append(os.path.join(dir_path, file))
    return models
