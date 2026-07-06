#!/usr/bin/env python3
"""
Download a GGUF model for Medusa.
Example:
    python download_model.py phi-3-mini-4k-instruct-Q4_K_M
    python download_model.py tinyllama-1.1b-Q4_K_M
"""

import os
import requests
import shutil
from pathlib import Path


def get_model_url(model_name: str) -> str:
    """Get the Hugging Face URL for a GGUF model."""
    # Use direct links to avoid auth issues
    model_map = {
        "phi-3-mini-4k-instruct-Q4_K_M": (
            "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-Q4_K_M.gguf",
        ),
        "phi-3-mini-4k-instruct-Q8_0": (
            "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-Q8_0.gguf",
        ),
        "tinyllama-1.1b-Q4_K_M": (
            "https://huggingface.co/TheBloke/TinyLlama-1.1B-GGUF/resolve/main/tinyllama-1.1b.Q4_K_M.gguf",
        ),
        "tinyllama-1.1b-Q8_0": (
            "https://huggingface.co/TheBloke/TinyLlama-1.1B-GGUF/resolve/main/tinyllama-1.1b.Q8_0.gguf",
        ),
        "llama-2-7b-chat-Q4_K_M": (
            "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf",
        ),
        "mistral-7b-instruct-Q4_K_M": (
            "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        ),
        # Fallback: Use a small test model (if available)
        "test-tiny": (
            "https://github.com/ggerganov/llama.cpp/releases/download/b2660/ggml-vocab-en.b20660.bin",
        ),
    }
    
    if model_name in model_map:
        return model_map[model_name]
    
    # Try to guess the URL
    return f"https://huggingface.co/TheBloke/{model_name}/resolve/main/{model_name}.gguf"


def download_with_retry(url: str, output_path: Path, max_retries: int = 3) -> bool:
    """Download a file with retries and proper headers."""
    headers = {
        "User-Agent": "MedusaAI/1.0 (compatible; python-requests/2.0)",
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True, headers=headers, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0
            
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\rDownloaded: {downloaded / (1024 * 1024):.1f} MB / {total_size / (1024 * 1024):.1f} MB ({percent:.1f}%)", end="")
            
            print(f"\nDownloaded {output_path.name} successfully!")
            return True
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print(f"\nAuthentication required for {url}")
                print("Try logging in to Hugging Face first:")
                print("  huggingface-cli login")
                print("Or use a different model.")
                return False
            elif e.response.status_code == 404:
                print(f"\nModel not found: {url}")
                return False
            else:
                print(f"\nHTTP Error: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying ({attempt + 1}/{max_retries})...")
                else:
                    return False
        except Exception as e:
            print(f"\nError: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying ({attempt + 1}/{max_retries})...")
            else:
                return False
    
    return False


def download_model(model_name: str, output_dir: str = "~/models") -> str:
    """Download a GGUF model from Hugging Face."""
    output_dir = Path(output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    url = get_model_url(model_name)
    output_path = output_dir / f"{model_name}.gguf"
    
    print(f"Downloading {model_name}...")
    print(f"URL: {url}")
    print(f"Saving to: {output_path}")
    
    if download_with_retry(url, output_path):
        return str(output_path)
    else:
        if output_path.exists():
            output_path.unlink()
        raise RuntimeError(f"Failed to download {model_name}")


def list_available_models() -> list:
    """List commonly available GGUF models."""
    return [
        "phi-3-mini-4k-instruct-Q4_K_M",
        "phi-3-mini-4k-instruct-Q8_0",
        "tinyllama-1.1b-Q4_K_M",
        "tinyllama-1.1b-Q8_0",
        "llama-2-7b-chat-Q4_K_M",
        "llama-2-7b-chat-Q8_0",
        "mistral-7b-instruct-Q4_K_M",
        "mistral-7b-instruct-Q8_0",
    ]


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Download GGUF models for Medusa")
    parser.add_argument("model", nargs="?", default=None, help="Model name (e.g., phi-3-mini-4k-instruct-Q4_K_M)")
    parser.add_argument("--list", action="store_true", help="List available models")
    parser.add_argument("--output", default="~/models", help="Output directory")
    args = parser.parse_args()
    
    if args.list:
        print("Available GGUF models:")
        for model in list_available_models():
            print(f"  - {model}")
        print("\nExample usage:")
        print(f"  python download_model.py phi-3-mini-4k-instruct-Q4_K_M")
        print("\nNote: Some models require Hugging Face authentication.")
        print("Run 'huggingface-cli login' to authenticate.")
        return
    
    if not args.model:
        print("Please specify a model name or use --list to see available models.")
        return
    
    try:
        download_model(args.model, args.output)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
